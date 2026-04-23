# Policy summary (cleanup behaviour):
# - Numeric zero is always a valid value; other cell values are invalid if they do not match
#   the expected type for that column (invalid optional fields become SQL NULL).
# - Optional foreign keys: invalid or missing parents are stored as NULL (never invent ids).
# - Required foreign keys: rows that reference a missing user (posts) or missing post/user
#   (interactions) are deleted from the database; dependent interaction rows are removed first.
# - After a CSV import, cleanup runs automatically on every row in the replaced table.
# - Duplicate usernames: for each username, the row with the smallest user_id (lexicographic)
#   is kept; other user rows with the same username are deleted when selected for cleanup,
#   including cascading deletes of their posts and related interactions.
# - Duplicate post content is not deduplicated; leave those rows as-is.
# - Date/datetime columns are canonicalised to calendar dates as YYYY-MM-DD (time discarded).
# - Destructive updates apply to the SQLite database only; CSV files on disk are never modified.
# - The UI shows a summary of cleanup results after import (no separate cleanup step).
# - Text encoding: rows are handled as Python str (Unicode). Cleanup does not re-read CSV files;
#   optional NFC normalisation is applied to normalise composed characters in text fields.
#
# Column rename utility: migrate_text_preview_to_content_preview (re-exported from database)
# renames posts.text_preview -> posts.content_preview on existing SQLite databases.

from __future__ import annotations

import re
import sqlite3
import unicodedata
from dataclasses import dataclass
from dataclasses import field
from datetime import date
from datetime import datetime

from audit_log import get_audit_logger
from database import migrate_posts_content_preview as migrate_text_preview_to_content_preview

TABLE_PRIMARY_KEY: dict[str, str] = {
    'topics': 'topic_id',
    'users': 'user_id',
    'posts': 'post_id',
    'interactions': 'interaction_id',
}

KNOWN_TABLES = frozenset(TABLE_PRIMARY_KEY.keys())


@dataclass
class CleanupReport:
    """Human-readable log lines plus coarse counts for dialogs."""

    lines: list[str] = field(default_factory=list)
    updates: int = 0
    deletes: int = 0

    def append(self, text: str) -> None:
        self.lines.append(text)


def _nfc_optional(value: str | None) -> str | None:
    if value is None:
        return None
    s = unicodedata.normalize('NFC', value.strip())
    return s or None


def _cell_str(row: dict[str, object], key: str) -> str:
    v = row.get(key)
    if v is None:
        return ''
    return str(v)


def _parse_date_yyyy_mm_dd(raw: str | None) -> str | None:
    """Return YYYY-MM-DD or None if empty/invalid."""
    s = _nfc_optional(raw)
    if s is None:
        return None
    # ISO date prefix
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})', s)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3))).isoformat()
        except ValueError:
            pass
    m = re.match(r'^(\d{4})/(\d{2})/(\d{2})', s)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3))).isoformat()
        except ValueError:
            pass
    # Slash day/month/year (common in sample CSVs)
    for fmt in ('%d/%m/%Y', '%m/%d/%Y'):
        try:
            return datetime.strptime(s[:10], fmt).date().isoformat()
        except ValueError:
            continue
    for fmt in ('%d-%m-%Y', '%m-%d-%Y', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S'):
        try:
            dt = datetime.strptime(s[:19], fmt) if len(s) >= 19 else datetime.strptime(s, fmt)
            return dt.date().isoformat()
        except ValueError:
            continue
    # Trailing time only
    for fmt in ('%Y-%m-%d %H:%M', '%d/%m/%Y %H:%M:%S', '%Y/%m/%d %H:%M'):
        try:
            return datetime.strptime(s[:16], fmt).date().isoformat()
        except ValueError:
            continue
    return None


def _normalise_bool_flag(raw: str | None) -> str | None:
    s = _nfc_optional(raw)
    if s is None:
        return None
    u = s.upper()
    if u == 'TRUE':
        return 'TRUE'
    if u == 'FALSE':
        return 'FALSE'
    return None


def _normalise_optional_int(raw: str | None) -> int | None:
    """0 is valid; empty -> None; non-numeric -> None."""
    s = _nfc_optional(raw)
    if s is None:
        return None
    try:
        return int(s, 10)
    except ValueError:
        return None


def _fetch_one(
        conn: sqlite3.Connection,
        table: str,
        pk_col: str,
        pk: str,
) -> dict[str, object] | None:
    row = conn.execute(
        f'SELECT * FROM {table} WHERE {_quote_ident(pk_col)} = ?',
        (pk,),
    ).fetchone()
    if row is None:
        return None
    cols = [d[1] for d in conn.execute(f'PRAGMA table_info({table})').fetchall()]
    return dict(zip(cols, row, strict=True))


def _quote_ident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _delete_post_cascade(conn: sqlite3.Connection, post_id: str) -> None:
    conn.execute('DELETE FROM interactions WHERE post_id = ?', (post_id,))
    conn.execute('DELETE FROM posts WHERE post_id = ?', (post_id,))


def _delete_user_cascade(conn: sqlite3.Connection, user_id: str) -> None:
    conn.execute(
        'DELETE FROM interactions WHERE user_id = ? OR post_id IN '
        '(SELECT post_id FROM posts WHERE user_id = ?)',
        (user_id, user_id),
    )
    conn.execute('DELETE FROM posts WHERE user_id = ?', (user_id,))
    conn.execute('DELETE FROM users WHERE user_id = ?', (user_id,))


def _user_ids_for_username(conn: sqlite3.Connection, username: str) -> list[str]:
    rows = conn.execute(
        'SELECT user_id FROM users WHERE username = ? ORDER BY user_id',
        (username,),
    ).fetchall()
    return [r[0] for r in rows]


def _cleanup_topics(
        conn: sqlite3.Connection,
        topic_ids: list[str],
        *,
        apply: bool,
        report: CleanupReport,
) -> None:
    for tid in topic_ids:
        row = _fetch_one(conn, 'topics', 'topic_id', tid)
        if row is None:
            report.append(f'topics: skip {tid!r} (not found)')
            continue
        name = _nfc_optional(_cell_str(row, 'topic_name'))
        if name is None:
            if apply:
                conn.execute(
                    'UPDATE posts SET topic_id = NULL WHERE topic_id = ?',
                    (tid,),
                )
                conn.execute('DELETE FROM topics WHERE topic_id = ?', (tid,))
                report.deletes += 1
            else:
                report.deletes += 1
            report.append(
                f'topics: delete topic_id={tid!r} (empty topic_name); '
                f'posts.topic_id references cleared first',
            )
            continue
        cat = _nfc_optional(_cell_str(row, 'category'))
        mod = _nfc_optional(_cell_str(row, 'moderation_level'))
        desc = _nfc_optional(_cell_str(row, 'description'))
        new_vals = {
            'topic_name': name,
            'category': cat,
            'moderation_level': mod,
            'description': desc,
        }
        old_vals = {k: row[k] for k in new_vals}
        changed = any(
            (old_vals[k] != new_vals[k])
            and not (old_vals[k] is None and new_vals[k] is None)
            for k in new_vals
        )
        if changed:
            if apply:
                conn.execute(
                    'UPDATE topics SET topic_name = ?, category = ?, '
                    'moderation_level = ?, description = ? WHERE topic_id = ?',
                    (
                        new_vals['topic_name'],
                        new_vals['category'],
                        new_vals['moderation_level'],
                        new_vals['description'],
                        tid,
                    ),
                )
                report.updates += 1
            else:
                report.updates += 1
            report.append(f'topics: update topic_id={tid!r} (normalised text / NULL optional fields)')


def _cleanup_users(
        conn: sqlite3.Connection,
        user_ids: list[str],
        *,
        apply: bool,
        report: CleanupReport,
) -> None:
    for uid in user_ids:
        row = _fetch_one(conn, 'users', 'user_id', uid)
        if row is None:
            report.append(f'users: skip {uid!r} (not found)')
            continue
        username = _nfc_optional(_cell_str(row, 'username'))
        if username is None:
            report.append(f'users: skip {uid!r} (empty username)')
            continue
        peers = _user_ids_for_username(conn, username)
        keeper = peers[0] if peers else uid
        if uid != keeper:
            report.append(
                f'users: delete user_id={uid!r} (duplicate username={username!r}; '
                f'keeping {keeper!r})',
            )
            if apply:
                _delete_user_cascade(conn, uid)
                report.deletes += 1
            else:
                report.deletes += 1
            continue

        jd = _parse_date_yyyy_mm_dd(_cell_str(row, 'join_date'))
        loc = _nfc_optional(_cell_str(row, 'location'))
        acct = _nfc_optional(_cell_str(row, 'account_type'))
        ver = _normalise_bool_flag(_cell_str(row, 'verified'))
        fc = _normalise_optional_int(_cell_str(row, 'followers_count'))

        new_vals = {
            'username': username,
            'join_date': jd,
            'location': loc,
            'account_type': acct,
            'verified': ver,
            'followers_count': fc,
        }
        old_vals = {k: row[k] for k in new_vals}
        changed = False
        for k in new_vals:
            ov, nv = old_vals[k], new_vals[k]
            if ov != nv and not (ov is None and nv is None):
                changed = True
        if changed:
            if apply:
                conn.execute(
                    'UPDATE users SET username = ?, join_date = ?, location = ?, '
                    'account_type = ?, verified = ?, followers_count = ? WHERE user_id = ?',
                    (
                        new_vals['username'],
                        new_vals['join_date'],
                        new_vals['location'],
                        new_vals['account_type'],
                        new_vals['verified'],
                        new_vals['followers_count'],
                        uid,
                    ),
                )
                report.updates += 1
            else:
                report.updates += 1
            report.append(f'users: update user_id={uid!r} (dates, flags, optional ints)')


def _cleanup_posts(
        conn: sqlite3.Connection,
        post_ids: list[str],
        *,
        apply: bool,
        report: CleanupReport,
) -> None:
    valid_users = {r[0] for r in conn.execute('SELECT user_id FROM users').fetchall()}
    valid_topics = {r[0] for r in conn.execute('SELECT topic_id FROM topics').fetchall()}

    for pid in post_ids:
        row = _fetch_one(conn, 'posts', 'post_id', pid)
        if row is None:
            report.append(f'posts: skip {pid!r} (not found)')
            continue
        uid = _nfc_optional(_cell_str(row, 'user_id'))
        if uid is None or uid not in valid_users:
            report.append(
                f'posts: delete post_id={pid!r} (missing or unknown user_id={uid!r})',
            )
            if apply:
                _delete_post_cascade(conn, pid)
                report.deletes += 1
            else:
                report.deletes += 1
            continue

        tid_raw = _cell_str(row, 'topic_id')
        topic_key = _nfc_optional(tid_raw)
        if topic_key is not None and topic_key not in valid_topics:
            topic_key = None
            report.append(f'posts: post_id={pid!r} set topic_id NULL (invalid reference)')

        ts = _parse_date_yyyy_mm_dd(_cell_str(row, 'timestamp'))
        ct = _nfc_optional(_cell_str(row, 'content_type'))
        tp = _nfc_optional(_cell_str(row, 'content_preview'))
        hm = _normalise_bool_flag(_cell_str(row, 'has_media'))
        lang = _nfc_optional(_cell_str(row, 'language'))

        new_vals = {
            'user_id': uid,
            'timestamp': ts,
            'content_type': ct,
            'content_preview': tp,
            'has_media': hm,
            'topic_id': topic_key,
            'language': lang,
        }
        old_vals = {k: row[k] for k in new_vals}
        changed = False
        for k in new_vals:
            ov, nv = old_vals[k], new_vals[k]
            if ov != nv and not (ov is None and nv is None):
                changed = True
        if changed:
            if apply:
                conn.execute(
                    'UPDATE posts SET user_id = ?, timestamp = ?, content_type = ?, '
                    'content_preview = ?, has_media = ?, topic_id = ?, language = ? '
                    'WHERE post_id = ?',
                    (
                        new_vals['user_id'],
                        new_vals['timestamp'],
                        new_vals['content_type'],
                        new_vals['content_preview'],
                        new_vals['has_media'],
                        new_vals['topic_id'],
                        new_vals['language'],
                        pid,
                    ),
                )
                report.updates += 1
            else:
                report.updates += 1
            report.append(f'posts: update post_id={pid!r}')


def _cleanup_interactions(
        conn: sqlite3.Connection,
        interaction_ids: list[str],
        *,
        apply: bool,
        report: CleanupReport,
) -> None:
    valid_users = {r[0] for r in conn.execute('SELECT user_id FROM users').fetchall()}
    valid_posts = {r[0] for r in conn.execute('SELECT post_id FROM posts').fetchall()}

    for iid in interaction_ids:
        row = _fetch_one(conn, 'interactions', 'interaction_id', iid)
        if row is None:
            report.append(f'interactions: skip {iid!r} (not found)')
            continue
        pid = _nfc_optional(_cell_str(row, 'post_id'))
        uid = _nfc_optional(_cell_str(row, 'user_id'))
        bad = pid is None or uid is None or pid not in valid_posts or uid not in valid_users
        if bad:
            report.append(
                f'interactions: delete interaction_id={iid!r} '
                f'(invalid post_id or user_id)',
            )
            if apply:
                conn.execute(
                    'DELETE FROM interactions WHERE interaction_id = ?',
                    (iid,),
                )
                report.deletes += 1
            else:
                report.deletes += 1
            continue

        ts = _parse_date_yyyy_mm_dd(_cell_str(row, 'timestamp'))
        itype = _nfc_optional(_cell_str(row, 'interaction_type'))
        rt = _nfc_optional(_cell_str(row, 'reaction_type'))

        new_vals = {
            'post_id': pid,
            'user_id': uid,
            'timestamp': ts,
            'interaction_type': itype,
            'reaction_type': rt,
        }
        old_vals = {k: row[k] for k in new_vals}
        changed = any(
            old_vals[k] != new_vals[k]
            and not (old_vals[k] is None and new_vals[k] is None)
            for k in new_vals
        )
        if changed:
            if apply:
                conn.execute(
                    'UPDATE interactions SET post_id = ?, user_id = ?, timestamp = ?, '
                    'interaction_type = ?, reaction_type = ? WHERE interaction_id = ?',
                    (
                        new_vals['post_id'],
                        new_vals['user_id'],
                        new_vals['timestamp'],
                        new_vals['interaction_type'],
                        new_vals['reaction_type'],
                        iid,
                    ),
                )
                report.updates += 1
            else:
                report.updates += 1
            report.append(f'interactions: update interaction_id={iid!r}')


def cleanup_selection(
        conn: sqlite3.Connection,
        table_name: str,
        selected_primary_keys: list[str],
        *,
        apply: bool,
) -> CleanupReport:
    """
    Run cleanup rules on the given primary keys for one table.

    If apply is False, the database is not modified (dry run for preview).
    If apply is True, changes are executed in a single transaction (commit on success).

    For a full-table pass (e.g. after import), use :func:`cleanup_entire_table`.
    """
    if table_name not in KNOWN_TABLES:
        raise ValueError(f'unsupported table: {table_name!r}')
    keys = [_nfc_optional(k) for k in selected_primary_keys]
    keys = [k for k in keys if k is not None]
    report = CleanupReport()
    if not keys:
        report.append('No primary keys to process.')
        return report

    report.append(f'Table {table_name!r}, {len(keys)} row(s), apply={apply}')

    if apply:
        conn.execute('BEGIN')

    try:
        if table_name == 'topics':
            _cleanup_topics(conn, keys, apply=apply, report=report)
        elif table_name == 'users':
            _cleanup_users(conn, keys, apply=apply, report=report)
        elif table_name == 'posts':
            _cleanup_posts(conn, keys, apply=apply, report=report)
        elif table_name == 'interactions':
            _cleanup_interactions(conn, keys, apply=apply, report=report)
        if apply:
            conn.commit()
    except Exception:
        if apply:
            conn.rollback()
        raise

    report.append(
        f'Summary: {report.updates} update(s), {report.deletes} delete(s)',
    )
    if apply:
        get_audit_logger().info(
            'Cleanup applied: table=%s rows_processed=%d updates=%d deletes=%d',
            table_name,
            len(keys),
            report.updates,
            report.deletes,
        )
    return report


def cleanup_entire_table(
        conn: sqlite3.Connection,
        table_name: str,
        *,
        apply: bool,
) -> CleanupReport:
    """
    Run :func:`cleanup_selection` for every primary key currently in ``table_name``.

    Used after CSV import so normalisation and FK rules apply to the whole table
    that was just loaded.
    """
    if table_name not in KNOWN_TABLES:
        raise ValueError(f'unsupported table: {table_name!r}')
    pk_col = TABLE_PRIMARY_KEY[table_name]
    cur = conn.execute(
        f'SELECT {_quote_ident(pk_col)} FROM {_quote_ident(table_name)}',
    )
    pks = [str(row[0]) for row in cur.fetchall() if row[0] is not None]
    return cleanup_selection(conn, table_name, pks, apply=apply)


def format_report_for_dialog(report: CleanupReport, *, max_lines: int = 80) -> str:
    lines = report.lines
    if len(lines) <= max_lines:
        return '\n'.join(lines)
    head = lines[: max_lines - 1]
    head.append(f'… ({len(lines) - len(head)} more lines omitted)')
    return '\n'.join(head)
