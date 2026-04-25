from __future__ import annotations

import csv
import os
import re
import sqlite3
from collections.abc import Iterable
from collections.abc import Mapping


_IDENTIFIER_RE = re.compile(r'[^a-z0-9_]+')
_LEADING_DIGIT_RE = re.compile(r'^\d')

# Demo CSVs: TOPICS → USERS → POSTS → INTERACTIONS (FK dependency order)
_RELATIONAL_TABLE_ORDER: tuple[str, ...] = (
    'topics',
    'users',
    'posts',
    'interactions',
)

_RELATIONAL_DDL: dict[str, str] = {
    'topics': '''
        CREATE TABLE topics (
            topic_id TEXT PRIMARY KEY,
            topic_name TEXT NOT NULL,
            category TEXT,
            moderation_level TEXT,
            description TEXT
        )
    ''',
    'users': '''
        CREATE TABLE users (
            user_id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            join_date TEXT,
            location TEXT,
            account_type TEXT,
            verified TEXT,
            followers_count INTEGER
        )
    ''',
    'posts': '''
        CREATE TABLE posts (
            post_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL REFERENCES users (user_id),
            timestamp TEXT,
            content_type TEXT,
            content_preview TEXT,
            has_media TEXT,
            topic_id TEXT REFERENCES topics (topic_id),
            language TEXT
        )
    ''',
    'interactions': '''
        CREATE TABLE interactions (
            interaction_id TEXT PRIMARY KEY,
            post_id TEXT NOT NULL REFERENCES posts (post_id),
            user_id TEXT NOT NULL REFERENCES users (user_id),
            interaction_type TEXT,
            timestamp TEXT,
            reaction_type TEXT
        )
    ''',
}

# Column order for INSERT (matches demo CSV headers after tidy_header_names)
_RELATIONAL_INSERT_COLUMNS: dict[str, tuple[str, ...]] = {
    'topics': (
        'topic_id',
        'topic_name',
        'category',
        'moderation_level',
        'description',
    ),
    'users': (
        'user_id',
        'username',
        'join_date',
        'location',
        'account_type',
        'verified',
        'followers_count',
    ),
    'posts': (
        'post_id',
        'user_id',
        'timestamp',
        'content_type',
        'content_preview',
        'has_media',
        'topic_id',
        'language',
    ),
    'interactions': (
        'interaction_id',
        'post_id',
        'user_id',
        'interaction_type',
        'timestamp',
        'reaction_type',
    ),
}


def _connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def sql_exclude_bot_users(*, users_table_alias: str | None) -> str:
    """
    SQL predicate that is true for non-bot accounts (case-insensitive ``account_type``).

    Pass ``users_table_alias`` (e.g. ``'u'``) when qualifying columns from a JOIN;
    pass ``None`` for the bare ``users`` table.
    """
    col = 'account_type' if users_table_alias is None else f'{users_table_alias}.account_type'
    return f"lower(trim(coalesce({col}, ''))) != 'bot'"


def database_exists(db_path: str) -> bool:
    if not os.path.isfile(db_path):
        return False

    try:
        with _connect(db_path) as db:
            db.execute('SELECT name FROM sqlite_master LIMIT 1')
    except sqlite3.DatabaseError:
        return False
    else:
        return True


def tidy_header_name(header: str) -> str:
    header = header.strip().lower()
    header = re.sub(r'\s+', '_', header)
    header = _IDENTIFIER_RE.sub('_', header)
    header = re.sub(r'_+', '_', header)
    header = header.strip('_')

    if not header:
        header = 'column'
    if _LEADING_DIGIT_RE.match(header):
        header = f'column_{header}'

    return header


def tidy_user_header_name(header: str) -> str:
    return tidy_header_name(header)


def tidy_header_names(headers: Iterable[str]) -> list[str]:
    seen: dict[str, int] = {}
    ret = []

    for header in headers:
        normalized = tidy_header_name(header)
        count = seen.get(normalized, 0)
        seen[normalized] = count + 1
        if count:
            normalized = f'{normalized}_{count + 1}'
        ret.append(normalized)

    return ret


def tidy_user_header_names(headers: Iterable[str]) -> list[str]:
    return tidy_header_names(headers)


def _normalize_posts_csv_headers(headers: list[str]) -> list[str]:
    """Map legacy ``text_preview`` column to ``content_preview`` (after tidy_header_names)."""
    return ['content_preview' if h == 'text_preview' else h for h in headers]


def prepare_csv_headers_for_import(
        normalized_table_name: str,
        headers: Iterable[str],
) -> list[str]:
    """
    Apply ``tidy_header_names`` and legacy renames so CSV headers match the DB schema.

    Posts CSVs may still use the old ``text_preview`` header; it is accepted as
    ``content_preview`` for validation and insert.
    """
    h = tidy_header_names(headers)
    if normalized_table_name != 'posts':
        return h
    return _normalize_posts_csv_headers(h)


def table_name_for_csv(csv_path: str) -> str:
    filename = os.path.basename(csv_path)
    stem, _ = os.path.splitext(filename)
    return tidy_header_name(stem)


def _quoted_identifier(identifier: str) -> str:
    escaped = identifier.replace('"', '""')
    return f'"{escaped}"'


def read_csv_rows(
        csv_path: str,
) -> tuple[list[str], list[tuple[str, ...]]]:
    for encoding in ('utf-8', 'utf-8-sig', 'cp1252', 'latin-1'):
        try:
            with open(csv_path, encoding=encoding, newline='') as f:
                rows = list(csv.reader(f))
        except UnicodeDecodeError:
            continue
        else:
            break
    else:
        raise ValueError(f'could not decode {csv_path}')

    if not rows:
        raise ValueError(f'{csv_path} is empty')

    headers = tidy_header_names(rows[0])
    data_rows = [tuple(row) for row in rows[1:]]
    return headers, data_rows


def _is_relational_table(table_name: str) -> bool:
    return table_name in _RELATIONAL_DDL


def _relational_schema_matches(db: sqlite3.Connection) -> bool:
    row = db.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='users'",
    ).fetchone()
    if not row:
        return False
    cols = {r[1] for r in db.execute('PRAGMA table_info(users)')}
    return 'user_id' in cols and 'followers_count' in cols


def _drop_all_relational_tables(db: sqlite3.Connection) -> None:
    db.execute('PRAGMA foreign_keys = OFF')
    for name in reversed(_RELATIONAL_TABLE_ORDER):
        db.execute(f'DROP TABLE IF EXISTS {_quoted_identifier(name)}')
    db.execute('PRAGMA foreign_keys = ON')


def _create_empty_relational_tables(db: sqlite3.Connection) -> None:
    for name in _RELATIONAL_TABLE_ORDER:
        db.executescript(_RELATIONAL_DDL[name])


def migrate_posts_content_preview(conn: sqlite3.Connection) -> bool:
    """
    Rename posts.text_preview -> content_preview if the legacy column exists.
    Idempotent. Returns True if an ALTER TABLE was executed.
    """
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='posts'",
    ).fetchone()
    if not row:
        return False
    cols = {r[1] for r in conn.execute('PRAGMA table_info(posts)').fetchall()}
    if 'text_preview' not in cols:
        return False
    if 'content_preview' in cols:
        return False
    conn.execute('ALTER TABLE posts RENAME COLUMN text_preview TO content_preview')
    return True


def ensure_relational_schema(db_path: str) -> None:
    """Create demo tables with PK/FK definitions, replacing any legacy stub schema."""
    parent = os.path.dirname(db_path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    with _connect(db_path) as db:
        if not _relational_schema_matches(db):
            _drop_all_relational_tables(db)
            _create_empty_relational_tables(db)
        migrate_posts_content_preview(db)


def _parse_optional_int(value: str) -> int | None:
    text = (value or '').strip()
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def _empty_to_none(value: str | None) -> str | None:
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    return value


def _validate_relational_headers(table_name: str, headers: list[str]) -> None:
    expected = frozenset(_RELATIONAL_INSERT_COLUMNS[table_name])
    got = frozenset(headers)
    if got != expected:
        missing = expected - got
        extra = got - expected
        parts = []
        if missing:
            parts.append(f'missing columns: {sorted(missing)}')
        if extra:
            parts.append(f'extra columns: {sorted(extra)}')
        raise ValueError(
            f'{table_name} CSV columns do not match the expected schema ({", ".join(parts)})',
        )


def _row_dict(headers: list[str], row: tuple[str, ...]) -> dict[str, str]:
    values = list(row)
    while len(values) < len(headers):
        values.append('')
    return {h: (values[i] or '').strip() if i < len(values) else '' for i, h in enumerate(headers)}


def _relational_insert_tuple(
        table_name: str,
        headers: list[str],
        row: tuple[str, ...],
) -> tuple:
    d = _row_dict(headers, row)
    if table_name == 'topics':
        return (
            d['topic_id'],
            d['topic_name'],
            _empty_to_none(d.get('category')),
            _empty_to_none(d.get('moderation_level')),
            _empty_to_none(d.get('description')),
        )
    if table_name == 'users':
        return (
            d['user_id'],
            d['username'],
            _empty_to_none(d.get('join_date')),
            _empty_to_none(d.get('location')),
            _empty_to_none(d.get('account_type')),
            _empty_to_none(d.get('verified')),
            _parse_optional_int(d.get('followers_count', '')),
        )
    if table_name == 'posts':
        return (
            d['post_id'],
            d['user_id'],
            _empty_to_none(d.get('timestamp')),
            _empty_to_none(d.get('content_type')),
            _empty_to_none(d.get('content_preview') or d.get('text_preview')),
            _empty_to_none(d.get('has_media')),
            _empty_to_none(d.get('topic_id')),
            _empty_to_none(d.get('language')),
        )
    if table_name == 'interactions':
        return (
            d['interaction_id'],
            d['post_id'],
            d['user_id'],
            _empty_to_none(d.get('interaction_type')),
            _empty_to_none(d.get('timestamp')),
            _empty_to_none(d.get('reaction_type')),
        )
    raise ValueError(f'unknown relational table: {table_name!r}')


def _create_table(
        db: sqlite3.Connection,
        *,
        table_name: str,
        headers: list[str],
        if_not_exists: bool = False,
) -> None:
    if if_not_exists:
        create_table = 'CREATE TABLE IF NOT EXISTS'
    else:
        create_table = 'CREATE TABLE'

    columns_sql = ', '.join(
        f'{_quoted_identifier(header)} TEXT'
        for header in headers
    )
    db.execute(
        f'{create_table} {_quoted_identifier(table_name)} ({columns_sql})',
    )


def _insert_rows(
        db: sqlite3.Connection,
        *,
        table_name: str,
        headers: list[str],
        rows: Iterable[tuple[str, ...]],
) -> None:
    placeholders = ', '.join('?' for _ in headers)
    columns_sql = ', '.join(_quoted_identifier(header) for header in headers)
    db.executemany(
        (
            f'INSERT INTO {_quoted_identifier(table_name)} ({columns_sql}) '
            f'VALUES ({placeholders})'
        ),
        rows,
    )


def _validate_relational_import_fk(
        db: sqlite3.Connection,
        table_name: str,
        typed_rows: list[tuple],
) -> None:
    """Raise ValueError with missing keys before SQLite FK error obscures the cause."""
    if table_name == 'posts':
        cols = _RELATIONAL_INSERT_COLUMNS['posts']
        i_uid = cols.index('user_id')
        i_tid = cols.index('topic_id')
        users = {r[0] for r in db.execute('SELECT user_id FROM users').fetchall()}
        topics = {r[0] for r in db.execute('SELECT topic_id FROM topics').fetchall()}
        bad_u: set[str] = set()
        bad_t: set[str] = set()
        for row in typed_rows:
            uid = row[i_uid]
            if uid is None or str(uid).strip() == '':
                raise ValueError(
                    'posts CSV: row with empty user_id. Every post must reference a user in users.',
                )
            us = str(uid).strip()
            if us not in users:
                bad_u.add(us)
            tid = row[i_tid]
            if tid is not None and str(tid).strip() != '':
                ts = str(tid).strip()
                if ts not in topics:
                    bad_t.add(ts)
        if bad_u or bad_t:
            parts = []
            if bad_u:
                parts.append(
                    f'user_id(s) not in users table: {", ".join(sorted(bad_u)[:40])}'
                    + ('…' if len(bad_u) > 40 else ''),
                )
            if bad_t:
                parts.append(
                    f'topic_id(s) not in topics table: {", ".join(sorted(bad_t)[:40])}'
                    + ('…' if len(bad_t) > 40 else ''),
                )
            raise ValueError(
                'posts CSV foreign keys failed validation: '
                + '; '.join(parts)
                + '. Load topics and users CSVs first (in that order), or add the missing keys.',
            )
    if table_name == 'interactions':
        cols = _RELATIONAL_INSERT_COLUMNS['interactions']
        i_pid = cols.index('post_id')
        i_uid = cols.index('user_id')
        posts = {r[0] for r in db.execute('SELECT post_id FROM posts').fetchall()}
        users = {r[0] for r in db.execute('SELECT user_id FROM users').fetchall()}
        bad_p: set[str] = set()
        bad_u: set[str] = set()
        for row in typed_rows:
            pid = row[i_pid]
            uid = row[i_uid]
            if pid is None or str(pid).strip() == '':
                raise ValueError(
                    'interactions CSV: row with empty post_id.',
                )
            if uid is None or str(uid).strip() == '':
                raise ValueError(
                    'interactions CSV: row with empty user_id.',
                )
            ps = str(pid).strip()
            us = str(uid).strip()
            if ps not in posts:
                bad_p.add(ps)
            if us not in users:
                bad_u.add(us)
        if bad_p or bad_u:
            parts = []
            if bad_p:
                parts.append(
                    f'post_id(s) not in posts: {", ".join(sorted(bad_p)[:40])}'
                    + ('…' if len(bad_p) > 40 else ''),
                )
            if bad_u:
                parts.append(
                    f'user_id(s) not in users: {", ".join(sorted(bad_u)[:40])}'
                    + ('…' if len(bad_u) > 40 else ''),
                )
            raise ValueError(
                'interactions CSV foreign keys failed validation: '
                + '; '.join(parts)
                + '. Load posts and users before interactions.',
            )


def _insert_relational_rows(
        db: sqlite3.Connection,
        *,
        table_name: str,
        headers: list[str],
        rows: Iterable[tuple[str, ...]],
) -> None:
    columns = _RELATIONAL_INSERT_COLUMNS[table_name]
    placeholders = ', '.join('?' for _ in columns)
    columns_sql = ', '.join(_quoted_identifier(c) for c in columns)
    typed_rows = [
        _relational_insert_tuple(table_name, headers, row)
        for row in rows
    ]
    if table_name in ('posts', 'interactions'):
        _validate_relational_import_fk(db, table_name, typed_rows)
    sql = (
        f'INSERT INTO {_quoted_identifier(table_name)} ({columns_sql}) '
        f'VALUES ({placeholders})'
    )
    try:
        db.executemany(sql, typed_rows)
    except sqlite3.IntegrityError as exc:
        hint = (
            f'Foreign key violation while inserting into {table_name!r}: {exc}. '
            'Load CSVs in dependency order: topics → users → posts → interactions. '
            'Each row must use parent keys that already exist in the database '
            '(e.g. posts need user_id in users and topic_id in topics or NULL; '
            'interactions need post_id in posts and user_id in users). '
            'If you replaced a parent table, children may still reference old IDs—'
            'reload children or the full dataset in order.'
        )
        from audit_log import get_audit_logger

        get_audit_logger().error('%s', hint, exc_info=True)
        raise ValueError(hint) from exc


def _replace_relational_table(
        db: sqlite3.Connection,
        *,
        table_name: str,
        headers: list[str],
        rows: Iterable[tuple[str, ...]],
) -> None:
    _validate_relational_headers(table_name, headers)
    db.execute('PRAGMA foreign_keys = OFF')
    db.execute(f'DROP TABLE IF EXISTS {_quoted_identifier(table_name)}')
    db.executescript(_RELATIONAL_DDL[table_name])
    db.execute('PRAGMA foreign_keys = ON')
    _insert_relational_rows(db, table_name=table_name, headers=headers, rows=rows)


def _sort_csv_paths_for_fk(csv_paths: Iterable[str]) -> list[str]:
    rank = {name: i for i, name in enumerate(_RELATIONAL_TABLE_ORDER)}

    def sort_key(path: str) -> tuple[int, str]:
        return (rank.get(table_name_for_csv(path), 99), path)

    return sorted(csv_paths, key=sort_key)


def create_database(
        db_path: str,
        csv_paths: Iterable[str],
) -> None:
    parent = os.path.dirname(db_path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    sorted_paths = _sort_csv_paths_for_fk(csv_paths)
    with _connect(db_path) as db:
        _drop_all_relational_tables(db)
        _create_empty_relational_tables(db)
        for csv_path in sorted_paths:
            table_name = table_name_for_csv(csv_path)
            if not _is_relational_table(table_name):
                headers, rows = _read_csv_rows(csv_path)
                headers = prepare_csv_headers_for_import(table_name, headers)
                _create_table(db, table_name=table_name, headers=headers)
                _insert_rows(db, table_name=table_name, headers=headers, rows=rows)
                continue
            headers, rows = _read_csv_rows(csv_path)
            headers = prepare_csv_headers_for_import(table_name, headers)
            _validate_relational_headers(table_name, headers)
            _insert_relational_rows(
                db,
                table_name=table_name,
                headers=headers,
                rows=rows,
            )


def replace_table_data(
        db_path: str,
        *,
        table_name: str,
        headers: Iterable[str],
        rows: Iterable[Iterable[str]],
) -> None:
    normalized_table_name = tidy_header_name(table_name)
    normalized_headers = prepare_csv_headers_for_import(normalized_table_name, headers)
    normalized_rows = [tuple(row) for row in rows]

    with _connect(db_path) as db:
        if _is_relational_table(normalized_table_name):
            _replace_relational_table(
                db,
                table_name=normalized_table_name,
                headers=normalized_headers,
                rows=normalized_rows,
            )
            return

        db.execute(
            f'DROP TABLE IF EXISTS {_quoted_identifier(normalized_table_name)}',
        )
        _create_table(
            db,
            table_name=normalized_table_name,
            headers=normalized_headers,
        )
        _insert_rows(
            db,
            table_name=normalized_table_name,
            headers=normalized_headers,
            rows=normalized_rows,
        )


def replace_table_data_from_csv(
        db_path: str,
        *,
        csv_path: str,
        table_name: str | None = None,
        preloaded: tuple[list[str], list[tuple[str, ...]]] | None = None,
) -> tuple[str, list[str], list[tuple[str, ...]]]:
    resolved_table_name = (
        table_name_for_csv(csv_path)
        if table_name is None
        else tidy_header_name(table_name)
    )
    if preloaded is not None:
        headers, rows = preloaded
    else:
        headers, rows = _read_csv_rows(csv_path)
    replace_table_data(
        db_path,
        table_name=resolved_table_name,
        headers=headers,
        rows=rows,
    )
    final_headers = prepare_csv_headers_for_import(resolved_table_name, headers)
    from audit_log import get_audit_logger

    get_audit_logger().info(
        'CSV committed to database: table=%s row_count=%d',
        resolved_table_name,
        len(rows),
    )
    return resolved_table_name, final_headers, rows


def get_table_columns(
        db_path: str,
        table_name: str,
) -> list[str]:
    normalized_table_name = tidy_user_header_name(table_name)

    with _connect(db_path) as db:
        table_rows = db.execute(
            f'PRAGMA table_info({_quoted_identifier(normalized_table_name)})',
        ).fetchall()

    if not table_rows:
        raise ValueError(f'unknown table: {table_name!r}')

    return [row[1] for row in table_rows]


def resolve_user_headers(
        db_path: str,
        *,
        table_name: str,
        headers: Iterable[str],
) -> dict[str, str]:
    columns = get_table_columns(db_path, table_name)
    allowed_columns = set(columns)
    ret = {}

    for header in headers:
        normalized = tidy_user_header_name(header)
        if normalized not in allowed_columns:
            raise ValueError(f'unknown column for {table_name!r}: {header!r}')
        ret[header] = normalized

    return ret


def query_rows(
        db_path: str,
        *,
        table_name: str,
        filters: Mapping[str, str],
        limit: int = 100,
) -> list[dict[str, str]]:
    if limit <= 0:
        raise ValueError('limit must be greater than zero')

    normalized_table_name = tidy_user_header_name(table_name)
    columns = get_table_columns(db_path, normalized_table_name)
    allowed_columns = set(columns)

    where = []
    params: list[str] = []
    for key, value in filters.items():
        column = tidy_user_header_name(key)
        if column not in allowed_columns:
            raise ValueError(f'unknown column for {table_name!r}: {key!r}')
        where.append(f'{_quoted_identifier(column)} = ?')
        params.append(value)

    limit_param = str(limit)

    with _connect(db_path) as db:
        db.row_factory = sqlite3.Row
        if normalized_table_name == 'posts':
            bot = sql_exclude_bot_users(users_table_alias='u')
            cond = [bot]
            if where:
                cond.extend(f'p.{clause}' for clause in where)
            wh = ' AND '.join(cond)
            rows = db.execute(
                (
                    'SELECT p.* FROM posts p '
                    'INNER JOIN users u ON p.user_id = u.user_id '
                    f'WHERE {wh} '
                    'LIMIT ?'
                ),
                [*params, limit_param],
            ).fetchall()
        elif normalized_table_name == 'interactions':
            bot = sql_exclude_bot_users(users_table_alias='u')
            cond = [bot]
            if where:
                cond.extend(f'i.{clause}' for clause in where)
            wh = ' AND '.join(cond)
            rows = db.execute(
                (
                    'SELECT i.* FROM interactions i '
                    'INNER JOIN users u ON i.user_id = u.user_id '
                    f'WHERE {wh} '
                    'LIMIT ?'
                ),
                [*params, limit_param],
            ).fetchall()
        elif normalized_table_name == 'users':
            bot = sql_exclude_bot_users(users_table_alias=None)
            cond = [bot]
            if where:
                cond.extend(where)
            wh = ' AND '.join(cond)
            rows = db.execute(
                (
                    f'SELECT * FROM {_quoted_identifier(normalized_table_name)} '
                    f'WHERE {wh} LIMIT ?'
                ),
                [*params, limit_param],
            ).fetchall()
        else:
            query = [f'SELECT * FROM {_quoted_identifier(normalized_table_name)}']
            if where:
                query.append('WHERE ' + ' AND '.join(where))
            query.append('LIMIT ?')
            params.append(limit_param)
            rows = db.execute(' '.join(query), params).fetchall()

    return [dict(row) for row in rows]


def query_row_numbers(
        db_path: str,
        *,
        table_name: str,
        row_numbers: Iterable[int],
) -> list[dict[str, str]]:
    normalized_table_name = tidy_user_header_name(table_name)
    normalized_row_numbers = [row_number for row_number in row_numbers]
    if not normalized_row_numbers:
        return []

    if any(row_number <= 0 for row_number in normalized_row_numbers):
        raise ValueError('row numbers must be positive integers')

    placeholders = ', '.join('?' for _ in normalized_row_numbers)

    with _connect(db_path) as db:
        db.row_factory = sqlite3.Row
        t = normalized_table_name
        if t == 'posts':
            bot = sql_exclude_bot_users(users_table_alias='u')
            rows = db.execute(
                (
                    'SELECT p.rowid AS rowid, p.* FROM posts p '
                    'INNER JOIN users u ON p.user_id = u.user_id '
                    f'WHERE {bot} AND p.rowid IN ({placeholders})'
                ),
                normalized_row_numbers,
            ).fetchall()
        elif t == 'interactions':
            bot = sql_exclude_bot_users(users_table_alias='u')
            rows = db.execute(
                (
                    'SELECT i.rowid AS rowid, i.* FROM interactions i '
                    'INNER JOIN users u ON i.user_id = u.user_id '
                    f'WHERE {bot} AND i.rowid IN ({placeholders})'
                ),
                normalized_row_numbers,
            ).fetchall()
        elif t == 'users':
            bot = sql_exclude_bot_users(users_table_alias=None)
            rows = db.execute(
                (
                    f'SELECT rowid, * FROM {_quoted_identifier(normalized_table_name)} '
                    f'WHERE {bot} AND rowid IN ({placeholders})'
                ),
                normalized_row_numbers,
            ).fetchall()
        else:
            rows = db.execute(
                (
                    f'SELECT rowid, * FROM {_quoted_identifier(normalized_table_name)} '
                    f'WHERE rowid IN ({placeholders})'
                ),
                normalized_row_numbers,
            ).fetchall()

    return [dict(row) for row in rows]
