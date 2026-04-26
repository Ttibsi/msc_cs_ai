from __future__ import annotations

import csv
import logging
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest import mock

import numpy as np
import pandas as pd
from matplotlib.figure import Figure

import analysis
import audit_log
import categorical_analysis
import database
import hour_topic_pivot
import moderation_effectiveness
import ui
import utilities


class _FakeVar:
    def __init__(self, value=None):
        self.value = value

    def get(self):
        return self.value

    def set(self, value) -> None:
        self.value = value


class _FakeWidget:
    instances: list['_FakeWidget'] = []

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.exists = True
        self.config = {}
        self.bound = {}
        self.children = []
        self.text = kwargs.get('text')
        self.command = kwargs.get('command')
        self.value = kwargs.get('value', '')
        self._selection = []
        self._items = {}
        type(self).instances.append(self)

    @classmethod
    def reset(cls) -> None:
        cls.instances = []

    def grid(self, *args, **kwargs) -> None:
        pass

    def pack(self, *args, **kwargs) -> None:
        pass

    def columnconfigure(self, *args, **kwargs) -> None:
        pass

    def rowconfigure(self, *args, **kwargs) -> None:
        pass

    def configure(self, **kwargs) -> None:
        self.config.update(kwargs)

    def bind(self, event, callback) -> None:
        self.bound[event] = callback

    def destroy(self) -> None:
        self.exists = False

    def winfo_exists(self):
        return self.exists

    def title(self, *args, **kwargs) -> None:
        pass

    def transient(self, *args, **kwargs) -> None:
        pass

    def geometry(self, *args, **kwargs) -> None:
        pass

    def minsize(self, *args, **kwargs) -> None:
        pass

    def resizable(self, *args, **kwargs) -> None:
        pass

    def protocol(self, name, callback) -> None:
        self.bound[name] = callback

    def mainloop(self) -> None:
        self.mainloop_called = True

    def create_window(self, *args, **kwargs):
        return 1

    def update_idletasks(self) -> None:
        pass

    def bbox(self, *args, **kwargs):
        return (0, 0, 100, 100)

    def itemconfigure(self, *args, **kwargs) -> None:
        pass

    def yview_scroll(self, *args, **kwargs) -> None:
        pass

    def yview(self, *args, **kwargs) -> None:
        pass

    def xview(self, *args, **kwargs) -> None:
        pass

    def set(self, *args, **kwargs) -> None:
        pass

    def heading(self, *args, **kwargs) -> None:
        pass

    def column(self, *args, **kwargs) -> None:
        pass

    def insert(self, parent, index, values=()):
        item_id = f'i{len(self._items) + 1}'
        self._items[item_id] = tuple(values)
        self.children.append(item_id)
        return item_id

    def delete(self, *item_ids) -> None:
        if not item_ids:
            return
        for item_id in item_ids:
            self._items.pop(item_id, None)
            if item_id in self.children:
                self.children.remove(item_id)

    def get_children(self):
        return tuple(self.children)

    def selection(self):
        return tuple(self._selection)

    def item(self, item_id, option=None):
        values = self._items.get(item_id, ())
        if option == 'values':
            return values
        return {'values': values}

    def state(self, *args, **kwargs) -> None:
        self.last_state = args

    def focus(self) -> None:
        self.focused = True

    def current(self, idx) -> None:
        vals = self.kwargs.get('values', [])
        self.value = vals[idx]

    def get(self):
        return self.value


class _FakeTreeview(_FakeWidget):
    def __setitem__(self, key, value) -> None:
        self.config[key] = value

    def __getitem__(self, key):
        return self.config[key]


class _FakeNotebook(_FakeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabs = []
        self.selected = 0

    def add(self, frame, text='') -> None:
        self.tabs.append((frame, text))

    def select(self):
        return self.selected

    def index(self, idx):
        return idx


class _FakeText(_FakeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contents = ''

    def insert(self, index, text) -> None:
        self.contents += text


class _FakeMplCanvas:
    def __init__(self, fig, master=None):
        self.fig = fig
        self.master = master
        self.widget = _FakeWidget()

    def draw(self) -> None:
        pass

    def get_tk_widget(self):
        return self.widget


class _FakeToolbar:
    def __init__(self, canvas, master, pack_toolbar=False):
        self.canvas = canvas
        self.master = master

    def update(self) -> None:
        pass

    def pack(self, *args, **kwargs) -> None:
        pass


class TestAnalysis(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = sqlite3.connect(':memory:')
        self.conn.executescript(
            '''
            CREATE TABLE users (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                account_type TEXT
            );
            CREATE TABLE posts (
                post_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                timestamp TEXT
            );
            CREATE TABLE interactions (
                interaction_id TEXT PRIMARY KEY,
                post_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                interaction_type TEXT,
                timestamp TEXT
            );
            INSERT INTO users (user_id, username, account_type) VALUES
                ('u1', 'alice', 'human'),
                ('u2', 'botty', 'bot');
            INSERT INTO posts (post_id, user_id, timestamp) VALUES
                ('p1', 'u1', '2024-01-01 09:00:00'),
                ('p2', 'u1', '2024/01/01 10:00:00'),
                ('p3', 'u2', '2024-01-02 11:00:00');
            INSERT INTO interactions (interaction_id, post_id, user_id, interaction_type, timestamp) VALUES
                ('i1', 'p1', 'u1', 'Like', '2024-01-01 12:00:00'),
                ('i2', 'p2', 'u1', '', '2024/01/02 13:00:00'),
                ('i3', 'p3', 'u2', 'Share', '2024-01-03 14:00:00');
            ''',
        )

    def tearDown(self) -> None:
        self.conn.close()

    def test__posts_timebase_sql(self) -> None:
        self.assertEqual(
            analysis._posts_timebase_sql(human_only=False),
            'SELECT post_id, timestamp FROM posts',
        )
        sql = analysis._posts_timebase_sql(human_only=True)
        self.assertIn('INNER JOIN users u ON p.user_id = u.user_id', sql)
        self.assertIn("lower(trim(coalesce(u.account_type, ''))) != 'bot'", sql)

    def test_fetch_posts_timestamps_df(self) -> None:
        all_rows = analysis.fetch_posts_timestamps_df(self.conn, human_only=False)
        human_rows = analysis.fetch_posts_timestamps_df(self.conn, human_only=True)
        self.assertEqual(list(all_rows['post_id']), ['p1', 'p2', 'p3'])
        self.assertEqual(list(human_rows['post_id']), ['p1', 'p2'])

    def test_normalize_sqlite_timestamp_series(self) -> None:
        raw = pd.Series(['2024/01/01 09:00:00', '2024-01-02 10:00:00', '', 'bad'])
        got = analysis.normalize_sqlite_timestamp_series(raw)
        self.assertEqual(got.dt.strftime('%Y-%m-%d %H:%M:%S').tolist()[:2], [
            '2024-01-01 09:00:00',
            '2024-01-02 10:00:00',
        ])
        self.assertTrue(pd.isna(got.iloc[2]))
        self.assertTrue(pd.isna(got.iloc[3]))

    def test__plot_daily_post_counts(self) -> None:
        fig = Figure()
        ax = fig.add_subplot(1, 1, 1)
        df = pd.DataFrame({'timestamp': ['2024-01-01 09:00:00', '2024/01/01 10:00:00']})
        analysis._plot_daily_post_counts(ax, df)
        self.assertEqual(ax.get_title(), 'Posts per calendar day')
        self.assertEqual(len(ax.lines), 1)

    def test__interactions_timebase_sql(self) -> None:
        self.assertIn('FROM interactions', analysis._interactions_timebase_sql(human_only=False))
        sql = analysis._interactions_timebase_sql(human_only=True)
        self.assertIn('INNER JOIN users u ON i.user_id = u.user_id', sql)
        self.assertIn("lower(trim(coalesce(u.account_type, ''))) != 'bot'", sql)

    def test_fetch_interactions_timestamps_df(self) -> None:
        all_rows = analysis.fetch_interactions_timestamps_df(self.conn, human_only=False)
        human_rows = analysis.fetch_interactions_timestamps_df(self.conn, human_only=True)
        self.assertEqual(list(all_rows['interaction_id']), ['i1', 'i2', 'i3'])
        self.assertEqual(list(human_rows['interaction_id']), ['i1', 'i2'])

    def test__normalize_interaction_type_labels(self) -> None:
        got = analysis._normalize_interaction_type_labels(pd.Series([' Like ', '', 'None']))
        self.assertEqual(got.tolist(), ['like', '(none)', '(none)'])

    def test__plot_daily_interactions(self) -> None:
        fig = Figure()
        ax = fig.add_subplot(1, 1, 1)
        df = pd.DataFrame({
            'timestamp': ['2024-01-01 12:00:00', '2024/01/02 13:00:00'],
            'interaction_type': ['Like', 'Share'],
        })
        analysis._plot_daily_interactions(ax, df)
        self.assertEqual(ax.get_title(), 'Interactions per calendar day by type (stacked)')
        self.assertGreater(len(ax.collections), 0)

    def test_build_analysis_figure(self) -> None:
        fig = analysis.build_analysis_figure(self.conn, human_only=True)
        self.assertIsInstance(fig, Figure)
        self.assertEqual(len(fig.axes), 2)
        self.assertEqual(fig.axes[0].get_title(), 'Posts per calendar day')


class TestAuditLog(unittest.TestCase):
    def setUp(self) -> None:
        self.orig_configured = audit_log._CONFIGURED
        self.orig_handlers = list(audit_log._LOG.handlers)
        self.orig_level = audit_log._LOG.level
        self.orig_propagate = audit_log._LOG.propagate
        self.orig_log_file = audit_log.LOG_FILE
        audit_log._CONFIGURED = False
        audit_log._LOG.handlers.clear()
        self.tmpdir = tempfile.TemporaryDirectory()
        audit_log.LOG_FILE = Path(self.tmpdir.name) / 'log.txt'

    def tearDown(self) -> None:
        for handler in list(audit_log._LOG.handlers):
            handler.close()
        audit_log._LOG.handlers.clear()
        audit_log._LOG.handlers.extend(self.orig_handlers)
        audit_log._LOG.setLevel(self.orig_level)
        audit_log._LOG.propagate = self.orig_propagate
        audit_log.LOG_FILE = self.orig_log_file
        audit_log._CONFIGURED = self.orig_configured
        self.tmpdir.cleanup()

    def test_configure_audit_logging(self) -> None:
        audit_log.configure_audit_logging()
        self.assertTrue(audit_log._CONFIGURED)
        self.assertEqual(len(audit_log._LOG.handlers), 2)
        self.assertEqual([h.level for h in audit_log._LOG.handlers], [logging.INFO, logging.ERROR])
        audit_log.configure_audit_logging()
        self.assertEqual(len(audit_log._LOG.handlers), 2)

    def test_get_audit_logger(self) -> None:
        logger = audit_log.get_audit_logger()
        self.assertIs(logger, audit_log._LOG)
        self.assertFalse(logger.propagate)
        self.assertTrue(audit_log.LOG_FILE.exists())


class TestCategoricalAnalysis(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = sqlite3.connect(':memory:')
        self.conn.executescript(
            '''
            CREATE TABLE users (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                account_type TEXT
            );
            CREATE TABLE topics (
                topic_id TEXT PRIMARY KEY,
                topic_name TEXT NOT NULL,
                category TEXT,
                moderation_level TEXT,
                description TEXT
            );
            CREATE TABLE posts (
                post_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                timestamp TEXT,
                content_type TEXT,
                topic_id TEXT
            );
            INSERT INTO users (user_id, username, account_type) VALUES
                ('u1', 'alice', 'human'),
                ('u2', 'botty', 'bot');
            INSERT INTO topics (topic_id, topic_name, category, moderation_level, description) VALUES
                ('t1', 'Topic 1', 'Safety', 'low', ''),
                ('t2', 'Topic 2', 'Policy', 'high', '');
            INSERT INTO posts (post_id, user_id, timestamp, content_type, topic_id) VALUES
                ('p1', 'u1', '2024-01-01 09:00:00', 'text', 't1'),
                ('p2', 'u1', '2024-01-01 10:00:00', 'image', 't2'),
                ('p3', 'u2', '2024-01-01 11:00:00', 'text', 't1'),
                ('p4', 'u1', '2024-01-01 12:00:00', NULL, 't1'),
                ('p5', 'u1', '2024-01-01 13:00:00', 'text', NULL);
            ''',
        )

    def tearDown(self) -> None:
        self.conn.close()

    def test__mod_sort_key(self) -> None:
        self.assertEqual(categorical_analysis._mod_sort_key('low'), 0)
        self.assertEqual(categorical_analysis._mod_sort_key(' Medium '), 1)
        self.assertEqual(categorical_analysis._mod_sort_key('unknown'), 99)

    def test_query_three_way_distribution(self) -> None:
        all_rows = categorical_analysis.query_three_way_distribution(self.conn, human_only=False)
        human_rows = categorical_analysis.query_three_way_distribution(self.conn, human_only=True)
        self.assertEqual(all_rows[0], ('Safety', 'low', 'text', 2))
        self.assertEqual(human_rows, [
            ('Policy', 'high', 'image', 1),
            ('Safety', 'low', '', 1),
            ('Safety', 'low', 'text', 1),
        ])

    def test_build_categorical_analysis_figure(self) -> None:
        rows = [('Safety', 'low', 'text', 2), ('Policy', 'high', 'image', 1)]
        fig = categorical_analysis.build_categorical_analysis_figure(rows, top_n_bars=1)
        self.assertIsInstance(fig, Figure)
        self.assertEqual(len(fig.axes), 3)
        self.assertEqual(fig.axes[0].get_title(), 'Post volume by category × moderation level (all content types combined)')
        self.assertEqual(fig.axes[1].get_title(), 'Top 1 (category | moderation_level | content_type) cells')


class TestDatabase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmp = Path(self.tmpdir.name)
        self.db_path = self.tmp / 'test.db'

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def _write_csv(self, name: str, rows: list[list[str]]) -> Path:
        path = self.tmp / name
        with path.open('w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows(rows)
        return path

    def _seed_relational_db(self) -> None:
        database.ensure_relational_schema(str(self.db_path))
        with closing(database._connect(str(self.db_path))) as conn, conn:
            conn.execute(
                "INSERT INTO topics VALUES ('t1', 'Topic 1', 'Safety', 'low', NULL)",
            )
            conn.executemany(
                'INSERT INTO users VALUES (?, ?, NULL, NULL, ?, NULL, NULL)',
                [('u1', 'alice', 'human'), ('u2', 'botty', 'bot')],
            )
            conn.executemany(
                'INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                [
                    ('p1', 'u1', '2024-01-01', 'text', 'a', 'FALSE', 't1', 'en'),
                    ('p2', 'u2', '2024-01-02', 'image', 'b', 'TRUE', 't1', 'en'),
                ],
            )
            conn.executemany(
                'INSERT INTO interactions VALUES (?, ?, ?, ?, ?, ?)',
                [
                    ('i1', 'p1', 'u1', 'like', '2024-01-03', None),
                    ('i2', 'p2', 'u2', 'share', '2024-01-04', None),
                ],
            )

    def test__connect(self) -> None:
        with closing(database._connect(str(self.db_path))) as conn, conn:
            self.assertEqual(conn.execute('PRAGMA foreign_keys').fetchone()[0], 1)

    def test_sql_exclude_bot_users(self) -> None:
        self.assertEqual(
            database.sql_exclude_bot_users(users_table_alias=None),
            "lower(trim(coalesce(account_type, ''))) != 'bot'",
        )
        self.assertIn('u.account_type', database.sql_exclude_bot_users(users_table_alias='u'))

    def test_database_exists(self) -> None:
        missing = self.tmp / 'missing.db'
        bad = self.tmp / 'bad.db'
        bad.write_text('not sqlite', encoding='utf-8')
        with closing(database._connect(str(self.db_path))) as conn, conn:
            conn.execute('CREATE TABLE x (id TEXT)')
        self.assertFalse(database.database_exists(str(missing)))
        self.assertFalse(database.database_exists(str(bad)))
        self.assertTrue(database.database_exists(str(self.db_path)))

    def test_tidy_header_name(self) -> None:
        self.assertEqual(database.tidy_header_name('  Display Name  '), 'display_name')
        self.assertEqual(database.tidy_header_name('123 value'), 'column_123_value')
        self.assertEqual(database.tidy_header_name('!!!'), 'column')

    def test_tidy_user_header_name(self) -> None:
        self.assertEqual(database.tidy_user_header_name('User Name'), 'user_name')

    def test_tidy_header_names(self) -> None:
        self.assertEqual(
            database.tidy_header_names(['User Name', 'User Name', 'Topic']),
            ['user_name', 'user_name_2', 'topic'],
        )

    def test_tidy_user_header_names(self) -> None:
        self.assertEqual(database.tidy_user_header_names(['A', 'A']), ['a', 'a_2'])

    def test__normalize_posts_csv_headers(self) -> None:
        self.assertEqual(
            database._normalize_posts_csv_headers(['post_id', 'text_preview']),
            ['post_id', 'content_preview'],
        )

    def test_prepare_csv_headers_for_import(self) -> None:
        self.assertEqual(
            database.prepare_csv_headers_for_import('posts', ['Post ID', 'Text Preview']),
            ['post_id', 'content_preview'],
        )
        self.assertEqual(
            database.prepare_csv_headers_for_import('users', ['User ID']),
            ['user_id'],
        )

    def test_table_name_for_csv(self) -> None:
        self.assertEqual(database.table_name_for_csv('/tmp/User Data.csv'), 'user_data')

    def test__quoted_identifier(self) -> None:
        self.assertEqual(database._quoted_identifier('a"b'), '"a""b"')

    def test_read_csv_rows(self) -> None:
        path = self._write_csv('users.csv', [['User ID', 'Name'], ['u1', 'Alice']])
        headers, rows = database.read_csv_rows(str(path))
        self.assertEqual(headers, ['user_id', 'name'])
        self.assertEqual(rows, [('u1', 'Alice')])

    def test__read_csv_rows(self) -> None:
        path = self._write_csv('empty.csv', [])
        with self.assertRaisesRegex(ValueError, 'empty'):
            database._read_csv_rows(str(path))

    def test__is_relational_table(self) -> None:
        self.assertTrue(database._is_relational_table('users'))
        self.assertFalse(database._is_relational_table('notes'))

    def test__relational_schema_matches(self) -> None:
        with closing(sqlite3.connect(':memory:')) as conn:
            self.assertFalse(database._relational_schema_matches(conn))
            conn.executescript(database._RELATIONAL_DDL['users'])
            self.assertTrue(database._relational_schema_matches(conn))

    def test__drop_all_relational_tables(self) -> None:
        with closing(sqlite3.connect(':memory:')) as conn:
            database._create_empty_relational_tables(conn)
            database._drop_all_relational_tables(conn)
            self.assertEqual(conn.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('topics','users','posts','interactions')",
            ).fetchone()[0], 0)

    def test__create_empty_relational_tables(self) -> None:
        with closing(sqlite3.connect(':memory:')) as conn:
            database._create_empty_relational_tables(conn)
            self.assertEqual(conn.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('topics','users','posts','interactions')",
            ).fetchone()[0], 4)

    def test_migrate_posts_content_preview(self) -> None:
        with closing(sqlite3.connect(':memory:')) as conn:
            conn.execute('CREATE TABLE posts (post_id TEXT, text_preview TEXT)')
            self.assertTrue(database.migrate_posts_content_preview(conn))
            cols = [r[1] for r in conn.execute('PRAGMA table_info(posts)')]
            self.assertIn('content_preview', cols)
            self.assertFalse(database.migrate_posts_content_preview(conn))

    def test_ensure_relational_schema(self) -> None:
        database.ensure_relational_schema(str(self.db_path))
        with closing(database._connect(str(self.db_path))) as conn, conn:
            count = conn.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('topics','users','posts','interactions')",
            ).fetchone()[0]
        self.assertEqual(count, 4)

    def test__parse_optional_int(self) -> None:
        self.assertEqual(database._parse_optional_int(' 7 '), 7)
        self.assertIsNone(database._parse_optional_int(''))
        self.assertIsNone(database._parse_optional_int('x'))

    def test__empty_to_none(self) -> None:
        self.assertIsNone(database._empty_to_none(' '))
        self.assertIsNone(database._empty_to_none(None))
        self.assertEqual(database._empty_to_none('x'), 'x')

    def test__validate_relational_headers(self) -> None:
        database._validate_relational_headers('users', list(database._RELATIONAL_INSERT_COLUMNS['users']))
        with self.assertRaisesRegex(ValueError, 'missing columns'):
            database._validate_relational_headers('users', ['user_id'])

    def test__row_dict(self) -> None:
        self.assertEqual(
            database._row_dict(['a', 'b', 'c'], (' 1 ', '',)),
            {'a': '1', 'b': '', 'c': ''},
        )

    def test__relational_insert_tuple(self) -> None:
        got = database._relational_insert_tuple(
            'posts',
            list(database._RELATIONAL_INSERT_COLUMNS['posts']),
            ('p1', 'u1', '', 'text', '', 'TRUE', 't1', 'en'),
        )
        self.assertEqual(got, ('p1', 'u1', None, 'text', None, 'TRUE', 't1', 'en'))

    def test__create_table(self) -> None:
        with closing(sqlite3.connect(':memory:')) as conn:
            database._create_table(conn, table_name='notes', headers=['id', 'body'])
            self.assertEqual([r[1] for r in conn.execute('PRAGMA table_info("notes")')], ['id', 'body'])

    def test__insert_rows(self) -> None:
        with closing(sqlite3.connect(':memory:')) as conn:
            database._create_table(conn, table_name='notes', headers=['id'])
            database._insert_rows(conn, table_name='notes', headers=['id'], rows=[('a',), ('b',)])
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM notes').fetchone()[0], 2)

    def test__validate_relational_import_fk(self) -> None:
        with closing(sqlite3.connect(':memory:')) as conn:
            database._create_empty_relational_tables(conn)
            conn.execute("INSERT INTO users VALUES ('u1', 'alice', NULL, NULL, NULL, NULL, NULL)")
            conn.execute("INSERT INTO topics VALUES ('t1', 'Topic 1', NULL, NULL, NULL)")
            with self.assertRaisesRegex(ValueError, 'foreign keys failed validation'):
                database._validate_relational_import_fk(
                    conn,
                    'posts',
                    [('p1', 'missing', None, None, None, None, 't1', None)],
                )

    def test__insert_relational_rows(self) -> None:
        with closing(sqlite3.connect(':memory:')) as conn:
            database._create_empty_relational_tables(conn)
            conn.execute("INSERT INTO users VALUES ('u1', 'alice', NULL, NULL, NULL, NULL, NULL)")
            conn.execute("INSERT INTO topics VALUES ('t1', 'Topic 1', NULL, NULL, NULL)")
            database._insert_relational_rows(
                conn,
                table_name='posts',
                headers=list(database._RELATIONAL_INSERT_COLUMNS['posts']),
                rows=[('p1', 'u1', '', 'text', '', '', 't1', 'en')],
            )
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM posts').fetchone()[0], 1)

    def test__replace_relational_table(self) -> None:
        with closing(sqlite3.connect(':memory:')) as conn:
            database._create_empty_relational_tables(conn)
            database._replace_relational_table(
                conn,
                table_name='users',
                headers=list(database._RELATIONAL_INSERT_COLUMNS['users']),
                rows=[('u1', 'alice', '', '', 'human', '', '5')],
            )
            self.assertEqual(conn.execute('SELECT username FROM users').fetchone()[0], 'alice')

    def test__sort_csv_paths_for_fk(self) -> None:
        got = database._sort_csv_paths_for_fk([
            '/tmp/posts.csv',
            '/tmp/z_misc.csv',
            '/tmp/topics.csv',
            '/tmp/users.csv',
        ])
        self.assertEqual(got[:3], ['/tmp/topics.csv', '/tmp/users.csv', '/tmp/posts.csv'])

    def test_create_database(self) -> None:
        topics = self._write_csv('topics.csv', [
            ['topic_id', 'topic_name', 'category', 'moderation_level', 'description'],
            ['t1', 'Topic 1', 'Safety', 'low', ''],
        ])
        users = self._write_csv('users.csv', [
            ['user_id', 'username', 'join_date', 'location', 'account_type', 'verified', 'followers_count'],
            ['u1', 'alice', '', '', 'human', '', '3'],
        ])
        posts = self._write_csv('posts.csv', [
            ['post_id', 'user_id', 'timestamp', 'content_type', 'content_preview', 'has_media', 'topic_id', 'language'],
            ['p1', 'u1', '2024-01-01', 'text', 'hello', 'FALSE', 't1', 'en'],
        ])
        notes = self._write_csv('notes.csv', [['id', 'body'], ['1', 'hello']])
        database.create_database(str(self.db_path), [str(posts), str(notes), str(users), str(topics)])
        with closing(database._connect(str(self.db_path))) as conn, conn:
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM posts').fetchone()[0], 1)
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM notes').fetchone()[0], 1)

    def test_replace_table_data(self) -> None:
        database.ensure_relational_schema(str(self.db_path))
        database.replace_table_data(
            str(self.db_path),
            table_name='notes',
            headers=['ID', 'Body'],
            rows=[['1', 'hello']],
        )
        database.replace_table_data(
            str(self.db_path),
            table_name='users',
            headers=database._RELATIONAL_INSERT_COLUMNS['users'],
            rows=[['u1', 'alice', '', '', 'human', '', '2']],
        )
        with closing(database._connect(str(self.db_path))) as conn, conn:
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM notes').fetchone()[0], 1)
            self.assertEqual(conn.execute('SELECT COUNT(*) FROM users').fetchone()[0], 1)

    def test_replace_table_data_from_csv(self) -> None:
        path = self._write_csv('notes.csv', [['ID', 'Body'], ['1', 'hello']])
        table_name, headers, rows = database.replace_table_data_from_csv(str(self.db_path), csv_path=str(path))
        self.assertEqual(table_name, 'notes')
        self.assertEqual(headers, ['id', 'body'])
        self.assertEqual(rows, [('1', 'hello')])

    def test_get_table_columns(self) -> None:
        database.replace_table_data(
            str(self.db_path),
            table_name='notes',
            headers=['ID', 'Body'],
            rows=[['1', 'hello']],
        )
        self.assertEqual(database.get_table_columns(str(self.db_path), 'notes'), ['id', 'body'])

    def test_resolve_user_headers(self) -> None:
        database.replace_table_data(
            str(self.db_path),
            table_name='notes',
            headers=['ID', 'Body'],
            rows=[['1', 'hello']],
        )
        self.assertEqual(
            database.resolve_user_headers(str(self.db_path), table_name='notes', headers=['ID', 'Body']),
            {'ID': 'id', 'Body': 'body'},
        )

    def test_query_rows(self) -> None:
        self._seed_relational_db()
        notes = [['ID', 'Body'], ['1', 'hello']]
        database.replace_table_data(str(self.db_path), table_name='notes', headers=notes[0], rows=notes[1:])
        self.assertEqual(
            [r['post_id'] for r in database.query_rows(str(self.db_path), table_name='posts', filters={}, limit=10)],
            ['p1'],
        )
        self.assertEqual(
            [r['user_id'] for r in database.query_rows(str(self.db_path), table_name='users', filters={}, limit=10)],
            ['u1'],
        )
        self.assertEqual(
            database.query_rows(str(self.db_path), table_name='notes', filters={'ID': '1'}, limit=10)[0]['body'],
            'hello',
        )

    def test_query_row_numbers(self) -> None:
        self._seed_relational_db()
        posts = database.query_row_numbers(str(self.db_path), table_name='posts', row_numbers=[1, 2])
        users = database.query_row_numbers(str(self.db_path), table_name='users', row_numbers=[1, 2])
        self.assertEqual([r['post_id'] for r in posts], ['p1'])
        self.assertEqual([r['user_id'] for r in users], ['u1'])


class TestHourTopicPivot(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = sqlite3.connect(':memory:')
        self.conn.executescript(
            '''
            CREATE TABLE users (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                account_type TEXT
            );
            CREATE TABLE topics (
                topic_id TEXT PRIMARY KEY,
                topic_name TEXT NOT NULL
            );
            CREATE TABLE posts (
                post_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                timestamp TEXT,
                topic_id TEXT
            );
            INSERT INTO users (user_id, username, account_type) VALUES
                ('u1', 'alice', 'human'),
                ('u2', 'botty', 'bot');
            INSERT INTO topics (topic_id, topic_name) VALUES
                ('t1', 'Topic 1'),
                ('t2', 'Topic 2');
            INSERT INTO posts (post_id, user_id, timestamp, topic_id) VALUES
                ('p1', 'u1', '2024-01-01 09:15:00', 't1'),
                ('p2', 'u1', '2024/01/01 09:45:00', 't1'),
                ('p3', 'u1', '2024-01-01T10:00:00', NULL),
                ('p4', 'u1', 'bad', 't2'),
                ('p5', 'u2', '2024-01-01 09:30:00', 't2');
            ''',
        )

    def tearDown(self) -> None:
        self.conn.close()

    def test__hour_expr(self) -> None:
        expr = hour_topic_pivot._hour_expr()
        self.assertIn("strftime('%H'", expr)
        self.assertIn("replace(replace(p.timestamp, '/', '-'), 'T', ' ')", expr)

    def test_query_hour_topic_counts(self) -> None:
        rows = hour_topic_pivot.query_hour_topic_counts(
            self.conn,
            hour_filter=None,
            topic_id_filter=None,
        )
        filtered = hour_topic_pivot.query_hour_topic_counts(
            self.conn,
            hour_filter=9,
            topic_id_filter='t1',
        )
        self.assertEqual(rows, [(9, 't1', 'Topic 1', 2), (10, None, None, 1)])
        self.assertEqual(filtered, [(9, 't1', 'Topic 1', 2)])

    def test__bucket_key(self) -> None:
        self.assertEqual(hour_topic_pivot._bucket_key(None), '__NULL__')
        self.assertEqual(hour_topic_pivot._bucket_key(''), '__NULL__')
        self.assertEqual(hour_topic_pivot._bucket_key('t1'), 't1')

    def test_build_pivot_matrix(self) -> None:
        matrix, keys, labels = hour_topic_pivot.build_pivot_matrix([
            (9, 't1', 'Topic 1', 2),
            (10, None, None, 1),
        ])
        self.assertEqual(matrix.shape, (24, 2))
        self.assertEqual(keys, ['t1', '__NULL__'])
        self.assertEqual(labels, ['t1', '(no topic)'])
        self.assertEqual(matrix[9, 0], 2.0)
        self.assertEqual(matrix[10, 1], 1.0)

    def test_build_hour_topic_pivot_figure(self) -> None:
        fig = hour_topic_pivot.build_hour_topic_pivot_figure(
            np.array([[1.0], [0.0]]),
            ['t1'],
            title='Pivot',
        )
        self.assertIsInstance(fig, Figure)
        self.assertEqual(len(fig.axes), 2)
        self.assertEqual(fig.axes[0].get_title(), 'Pivot')


class TestModerationEffectiveness(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = sqlite3.connect(':memory:')
        self.conn.executescript(
            '''
            CREATE TABLE users (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                account_type TEXT
            );
            CREATE TABLE topics (
                topic_id TEXT PRIMARY KEY,
                topic_name TEXT NOT NULL,
                category TEXT,
                moderation_level TEXT,
                description TEXT
            );
            CREATE TABLE posts (
                post_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                timestamp TEXT,
                content_type TEXT,
                content_preview TEXT,
                has_media TEXT,
                topic_id TEXT,
                language TEXT
            );
            CREATE TABLE interactions (
                interaction_id TEXT PRIMARY KEY,
                post_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                interaction_type TEXT,
                timestamp TEXT,
                reaction_type TEXT
            );
            INSERT INTO users (user_id, username, account_type) VALUES
                ('u1', 'alice', 'human'),
                ('u2', 'bob', 'human'),
                ('u3', 'botty', 'bot'),
                ('r1', 'rep1', 'human'),
                ('r2', 'rep2', 'human'),
                ('rb', 'repbot', 'bot');
            INSERT INTO topics (topic_id, topic_name, category, moderation_level, description) VALUES
                ('t1', 'Topic 1', 'Safety', 'low', ''),
                ('t2', 'Topic 2', 'Safety', 'high', ''),
                ('t3', 'Topic 3', 'Policy', 'medium', '');
            INSERT INTO posts (post_id, user_id, timestamp, content_type, content_preview, has_media, topic_id, language) VALUES
                ('p1', 'u1', '2024-01-01', 'text', '', 'FALSE', 't1', 'en'),
                ('p2', 'u1', '2024-01-02', 'text', '', 'FALSE', 't1', 'en'),
                ('p3', 'u2', '2024-01-03', 'text', '', 'FALSE', 't2', 'en'),
                ('p4', 'u2', '2024-01-04', 'text', '', 'FALSE', 't2', 'en'),
                ('p5', 'u1', '2024-01-05', 'text', '', 'FALSE', 't3', 'en'),
                ('p6', 'u3', '2024-01-06', 'text', '', 'FALSE', 't1', 'en'),
                ('p7', 'u1', '2024-01-07', 'text', '', 'FALSE', NULL, 'en');
            INSERT INTO interactions (interaction_id, post_id, user_id, interaction_type, timestamp, reaction_type) VALUES
                ('i1', 'p1', 'r1', 'report', '2024-01-10', NULL),
                ('i2', 'p1', 'r2', 'REPORT', '2024-01-10', NULL),
                ('i3', 'p3', 'r1', 'report', '2024-01-10', NULL),
                ('i4', 'p3', 'U9999', 'report', '2024-01-10', NULL),
                ('i5', 'p4', 'rb', 'report', '2024-01-10', NULL),
                ('i6', 'p2', 'r1', 'like', '2024-01-10', NULL);
            ''',
        )

    def tearDown(self) -> None:
        self.conn.close()

    def test__mod_rank(self) -> None:
        self.assertEqual(moderation_effectiveness._mod_rank('low'), 0)
        self.assertEqual(moderation_effectiveness._mod_rank('HIGH'), 2)
        self.assertEqual(moderation_effectiveness._mod_rank(None), 1)

    def test__effectiveness_ctes(self) -> None:
        sql = moderation_effectiveness._effectiveness_ctes(ua='ua_pred', ur='ur_pred', ph='U9999')
        self.assertIn('WITH in_scope_posts AS', sql)
        self.assertIn('WHERE ua_pred AND p.topic_id IS NOT NULL', sql)
        self.assertIn("AND i.user_id != 'U9999'", sql)

    def test_run_moderation_effectiveness_analysis(self) -> None:
        result = moderation_effectiveness.run_moderation_effectiveness_analysis(self.conn)
        self.assertEqual(result.ignored_placeholder_reports, 1)
        self.assertEqual(result.summary_colnames[:2], ['category', 'moderation_level'])
        self.assertEqual(
            {(r[0], r[1], int(r[2]), int(r[3])) for r in result.summary_rows},
            {('Policy', 'medium', 1, 0), ('Safety', 'high', 2, 1), ('Safety', 'low', 2, 2)},
        )

    def test__col_index(self) -> None:
        self.assertEqual(moderation_effectiveness._col_index(['a', 'b'], 'b'), 1)
        self.assertEqual(moderation_effectiveness._col_index(['a', 'b'], 'x'), -1)

    def test__summary_stat_lines(self) -> None:
        lines = moderation_effectiveness._summary_stat_lines(
            [('Safety', 'low', 2, 2, 1.0, 50.0)],
            ['category', 'moderation_level', 'posts_in_group', 'reports_in_group', 'reports_per_post', 'pct_posts_with_reports'],
            [('t1', 'Topic 1', 'Safety', 'low', 2, 2)],
            1,
        )
        self.assertIn('Total in-scope posts (aggregate buckets): 2', lines)
        self.assertIn("Placeholder ('U9999') report interactions excluded from numerators: 1", lines)

    def test__detect_patterns(self) -> None:
        patterns = moderation_effectiveness._detect_patterns(
            [
                ('Safety', 'low', 10, 1, 0.1, 10.0),
                ('Safety', 'high', 10, 4, 0.4, 30.0),
            ],
            ['category', 'moderation_level', 'posts_in_group', 'reports_in_group', 'reports_per_post', 'pct_posts_with_reports'],
            [
                ('t1', 'Topic 1', 'Safety', 'low', 5, 5),
                ('t2', 'Topic 2', 'Safety', 'low', 4, 1),
                ('t3', 'Topic 3', 'Safety', 'high', 3, 0),
                ('t4', 'Topic 4', 'Safety', 'high', 3, 9),
            ],
        )
        self.assertTrue(any('Concentration:' in p for p in patterns))
        self.assertTrue(any('Mismatch (aggregate):' in p for p in patterns))
        self.assertTrue(any('Outlier topic:' in p for p in patterns))

    def test_build_moderation_effectiveness_figure(self) -> None:
        result = moderation_effectiveness.run_moderation_effectiveness_analysis(self.conn)
        fig = moderation_effectiveness.build_moderation_effectiveness_figure(result)
        self.assertIsInstance(fig, Figure)
        self.assertEqual(len(fig.axes), 4)
        self.assertEqual(fig.axes[0].get_title(), 'Report intensity by moderation level')

    def test_build_moderation_correlation_figure(self) -> None:
        result = moderation_effectiveness.run_moderation_effectiveness_analysis(self.conn)
        fig, corr = moderation_effectiveness.build_moderation_correlation_figure(result)
        self.assertIsInstance(fig, Figure)
        self.assertEqual(len(fig.axes), 2)
        self.assertIsNotNone(corr)

    def test_moderation_effectiveness_summary(self) -> None:
        result = moderation_effectiveness.run_moderation_effectiveness_analysis(self.conn)
        summary = moderation_effectiveness.moderation_effectiveness_summary(self.conn)
        self.assertEqual(summary, (result.summary_colnames, result.summary_rows, result.ignored_placeholder_reports))


class TestUi(unittest.TestCase):
    def setUp(self) -> None:
        _FakeWidget.reset()
        _FakeTreeview.reset()
        _FakeNotebook.reset()
        _FakeText.reset()
        self.conn = sqlite3.connect(':memory:')
        self.conn.executescript(
            '''
            CREATE TABLE users (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                join_date TEXT,
                location TEXT,
                account_type TEXT,
                verified TEXT,
                followers_count INTEGER
            );
            CREATE TABLE topics (
                topic_id TEXT PRIMARY KEY,
                topic_name TEXT NOT NULL,
                category TEXT,
                moderation_level TEXT,
                description TEXT
            );
            CREATE TABLE posts (
                post_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                timestamp TEXT,
                content_type TEXT,
                content_preview TEXT,
                has_media TEXT,
                topic_id TEXT,
                language TEXT
            );
            CREATE TABLE interactions (
                interaction_id TEXT PRIMARY KEY,
                post_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                interaction_type TEXT,
                timestamp TEXT,
                reaction_type TEXT
            );
            INSERT INTO users VALUES
                ('u1', 'alice', NULL, NULL, 'human', NULL, 10),
                ('u2', 'botty', NULL, NULL, 'bot', NULL, 20);
            INSERT INTO topics VALUES
                ('t1', 'Topic 1', 'Safety', 'low', NULL);
            INSERT INTO posts VALUES
                ('p1', 'u1', '2024-01-01 09:00:00', 'text', 'a', 'FALSE', 't1', 'en'),
                ('p2', 'u2', '2024-01-02 10:00:00', 'text', 'b', 'FALSE', 't1', 'en');
            INSERT INTO interactions VALUES
                ('i1', 'p1', 'u1', 'like', '2024-01-03', NULL),
                ('i2', 'p2', 'u2', 'report', '2024-01-04', NULL);
            ''',
        )

    def tearDown(self) -> None:
        self.conn.close()

    def test__log_error(self) -> None:
        logger = mock.Mock()
        with mock.patch.object(ui, 'get_audit_logger', return_value=logger):
            ui._log_error('ctx', ValueError('bad'))
        logger.error.assert_called_once()

    def test__ensure_database(self) -> None:
        with mock.patch.object(ui, 'database_exists', return_value=False), \
                mock.patch('builtins.open', mock.mock_open()), \
                mock.patch.object(ui, 'ensure_relational_schema') as ensure:
            ui._ensure_database()
        ensure.assert_called_once_with(ui.DB_PATH)

    def test__get_table_columns(self) -> None:
        self.assertEqual(
            ui._get_table_columns(self.conn, 'users')[:3],
            ['user_id', 'username', 'join_date'],
        )

    def test__fetch_table_rows_for_treeview(self) -> None:
        self.assertEqual(len(ui._fetch_table_rows_for_treeview(self.conn, 'users', human_only=False)), 2)
        self.assertEqual(len(ui._fetch_table_rows_for_treeview(self.conn, 'users', human_only=True)), 1)
        self.assertEqual(len(ui._fetch_table_rows_for_treeview(self.conn, 'posts', human_only=True)), 1)
        self.assertEqual(len(ui._fetch_table_rows_for_treeview(self.conn, 'topics', human_only=True)), 1)

    def test__human_only_from_state(self) -> None:
        with mock.patch.object(ui.tk, 'BooleanVar', _FakeVar):
            self.assertTrue(ui._human_only_from_state({'human_only_var': _FakeVar(True)}))
        self.assertFalse(ui._human_only_from_state({}))

    def test__count_bot_hidden_rows(self) -> None:
        self.assertEqual(ui._count_bot_hidden_rows(self.conn), 3)

    def test__human_only_checkbox_label(self) -> None:
        self.assertEqual(ui._human_only_checkbox_label(self.conn, False), 'Human only (hide bot rows)')
        self.assertEqual(ui._human_only_checkbox_label(self.conn, True), 'Human only (hide bot rows) (3 hidden)')

    def test__populate_treeview(self) -> None:
        tree = _FakeTreeview()
        ui._populate_treeview(conn=self.conn, table_name='users', treeview=tree, human_only=True)
        self.assertEqual(tree.config['columns'][0], 'user_id')
        self.assertEqual(len(tree.get_children()), 1)

    def test__refresh_all_treeviews(self) -> None:
        with mock.patch.object(ui, '_populate_treeview') as pop:
            ui._refresh_all_treeviews(
                conn=self.conn,
                treeviews={'users': _FakeTreeview(), 'posts': _FakeTreeview()},
                human_only=True,
            )
        self.assertEqual(pop.call_count, 2)

    def test__selected_rows(self) -> None:
        tree = _FakeTreeview()
        item = tree.insert('', 'end', values=('a', 2))
        tree._selection = [item]
        self.assertEqual(ui._selected_rows(tree), [('a', '2')])

    def test__upload_csv(self) -> None:
        new_conn = sqlite3.connect(':memory:')
        self.addCleanup(new_conn.close)
        report = mock.Mock(updates=1, deletes=0)
        state = {'sync_human_only_label': mock.Mock()}
        with mock.patch.object(ui.filedialog, 'askopenfilename', return_value='users.csv'), \
                mock.patch.object(ui, 'read_csv_rows', return_value=(['user_id'], [('u1',)])), \
                mock.patch.object(ui.messagebox, 'askyesno', return_value=True), \
                mock.patch.object(ui, 'replace_table_data_from_csv', return_value=('users', ['user_id'], [('u1',)])), \
                mock.patch.object(ui.sqlite3, 'connect', return_value=new_conn), \
                mock.patch.object(ui, '_refresh_all_treeviews') as refresh, \
                mock.patch.object(ui, 'cleanup_entire_table', return_value=report), \
                mock.patch.object(ui, 'format_report_for_dialog', return_value='done'), \
                mock.patch.object(ui.messagebox, 'showinfo') as showinfo:
            ui._upload_csv(
                conn=self.conn,
                state=state,
                treeviews={'users': _FakeTreeview()},
                human_only=True,
            )
        self.assertEqual(state['uploaded_table'], 'users')
        self.assertEqual(state['uploaded_rows'], [['user_id'], ('u1',)])
        self.assertEqual(refresh.call_count, 2)
        showinfo.assert_called()

    def test__close_filter_results_window(self) -> None:
        with mock.patch.object(ui.tk, 'Toplevel', _FakeWidget):
            win = _FakeWidget()
            state = {'filter_results_window': win}
            ui._close_filter_results_window(state)
        self.assertIsNone(state['filter_results_window'])
        self.assertFalse(win.exists)

    def test__close_filter_pivot_window(self) -> None:
        with mock.patch.object(ui.tk, 'Toplevel', _FakeWidget):
            win = _FakeWidget()
            state = {'filter_pivot_window': win}
            ui._close_filter_pivot_window(state)
        self.assertIsNone(state['filter_pivot_window'])
        self.assertFalse(win.exists)

    def test__filtered_posts_where_and_params(self) -> None:
        sql, params = ui._filtered_posts_where_and_params(hour=9, topic_id='t1')
        self.assertIn('p.topic_id = ?', sql)
        self.assertEqual(params, [9, 't1'])

    def test__build_filtered_posts_count_sql(self) -> None:
        sql, params = ui._build_filtered_posts_count_sql(hour=9, topic_id=None)
        self.assertIn('SELECT COUNT(*)', sql)
        self.assertEqual(params, [9])

    def test__build_filtered_posts_select_sql(self) -> None:
        sql, params = ui._build_filtered_posts_select_sql(hour=None, topic_id='t1', limit=5, offset=10)
        self.assertIn('LIMIT ? OFFSET ?', sql)
        self.assertEqual(params, ['t1', 5, 10])

    def test__show_filtered_posts_window(self) -> None:
        with mock.patch.object(ui.tk, 'Toplevel', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Frame', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Treeview', _FakeTreeview), \
                mock.patch.object(ui.ttk, 'Scrollbar', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Button', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Label', _FakeWidget), \
                mock.patch.object(ui.tk, 'StringVar', _FakeVar):
            state = {}
            parent = _FakeWidget()
            ui._show_filtered_posts_window(
                parent=parent,
                state=state,
                conn=self.conn,
                column_names=['post_id'],
                hour=None,
                topic_id=None,
                total_count=1,
                page_size=50,
            )
        self.assertIsInstance(state['filter_results_window'], _FakeWidget)

    def test__show_hour_topic_pivot_window(self) -> None:
        fake_backend = mock.Mock(FigureCanvasTkAgg=_FakeMplCanvas)
        with mock.patch.object(ui.tk, 'Toplevel', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Frame', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Treeview', _FakeTreeview), \
                mock.patch.object(ui.ttk, 'Scrollbar', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Button', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Label', _FakeWidget), \
                mock.patch.dict('sys.modules', {'matplotlib.backends.backend_tkagg': fake_backend}):
            state = {}
            ui._show_hour_topic_pivot_window(
                parent=_FakeWidget(),
                state=state,
                conn=self.conn,
                hour_filter=None,
                topic_id_filter=None,
            )
        self.assertIsInstance(state['filter_pivot_window'], _FakeWidget)

    def test__open_filters_dialog(self) -> None:
        buttons = []

        def button_factory(*args, **kwargs):
            btn = _FakeWidget(*args, **kwargs)
            buttons.append(btn)
            return btn

        with mock.patch.object(ui.tk, 'Toplevel', _FakeWidget), \
                mock.patch.object(ui.tk, 'StringVar', side_effect=lambda *a, **k: _FakeVar('')), \
                mock.patch.object(ui.ttk, 'Frame', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Label', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Entry', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Combobox', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Button', side_effect=button_factory), \
                mock.patch.object(ui, '_show_filtered_posts_window') as show_posts, \
                mock.patch.object(ui, '_show_hour_topic_pivot_window') as show_pivot:
            state = {'conn': self.conn, 'filters': {}}
            ui._open_filters_dialog(parent=_FakeWidget(), state=state)
            buttons[-1].command()
        self.assertEqual(state['filters'], {'hour_of_day': None, 'topic_id': None})
        show_posts.assert_called_once()
        show_pivot.assert_called_once()

    def test__account_type_is_bot(self) -> None:
        self.assertTrue(ui._account_type_is_bot(' BOT '))
        self.assertFalse(ui._account_type_is_bot('human'))

    def test__user_id_is_bot(self) -> None:
        cache = {}
        self.assertTrue(ui._user_id_is_bot(self.conn, 'u2', cache=cache))
        self.assertTrue(cache['u2'])

    def test__record_is_bot_excluded(self) -> None:
        self.assertTrue(ui._record_is_bot_excluded(self.conn, 'users', {'account_type': 'bot'}, cache={}))
        self.assertTrue(ui._record_is_bot_excluded(self.conn, 'posts', {'user_id': 'u2'}, cache={}))
        self.assertFalse(ui._record_is_bot_excluded(self.conn, 'topics', {}, cache={}))

    def test__parse_engagement_value(self) -> None:
        self.assertEqual(ui._parse_engagement_value('followers_count', '10'), 10.0)
        self.assertIsNone(ui._parse_engagement_value('followers_count', 'x'))

    def test__format_mode_list(self) -> None:
        self.assertEqual(ui._format_mode_list([]), 'n/a')
        self.assertEqual(ui._format_mode_list([2.0, 1.0]), '1, 2')

    def test__show_selected_row_stats(self) -> None:
        notebook = _FakeNotebook()
        notebook.selected = 0
        tree = _FakeTreeview()
        item = tree.insert('', 'end', values=('u1', 'alice', '', '', 'human', '', '10'))
        tree._selection = [item]
        with mock.patch.object(ui.messagebox, 'askyesno', return_value=True), \
                mock.patch.object(ui.messagebox, 'showinfo') as showinfo:
            ui._show_selected_row_stats(
                parent=_FakeWidget(),
                conn=self.conn,
                notebook=notebook,
                treeviews={'users': tree, 'posts': _FakeTreeview(), 'topics': _FakeTreeview(), 'interactions': _FakeTreeview()},
            )
        self.assertIn('followers_count', showinfo.call_args.args[1])

    def test__open_moderation_effectiveness_dialog(self) -> None:
        result = moderation_effectiveness.run_moderation_effectiveness_analysis(self.conn)
        fake_backend = mock.Mock(FigureCanvasTkAgg=_FakeMplCanvas)
        with mock.patch.object(ui.tk, 'Toplevel', _FakeWidget), \
                mock.patch.object(ui.tk, 'Canvas', _FakeWidget), \
                mock.patch.object(ui.tk, 'Text', _FakeText), \
                mock.patch.object(ui.ttk, 'Frame', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Scrollbar', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Button', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Label', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Treeview', _FakeTreeview), \
                mock.patch.object(ui, 'run_moderation_effectiveness_analysis', return_value=result), \
                mock.patch.dict('sys.modules', {'matplotlib.backends.backend_tkagg': fake_backend}):
            ui._open_moderation_effectiveness_dialog(parent=_FakeWidget(), conn=self.conn)
        self.assertTrue(_FakeWidget.instances)

    def test__close_analysis_charts_window(self) -> None:
        with mock.patch.object(ui.tk, 'Toplevel', _FakeWidget):
            win = _FakeWidget()
            state = {'analysis_charts_window': win}
            ui._close_analysis_charts_window(state)
        self.assertIsNone(state['analysis_charts_window'])

    def test__open_analysis_charts_window(self) -> None:
        fake_backend = mock.Mock(FigureCanvasTkAgg=_FakeMplCanvas, NavigationToolbar2Tk=_FakeToolbar)
        with mock.patch.dict('sys.modules', {'matplotlib.backends.backend_tkagg': fake_backend}), \
                mock.patch.object(ui.tk, 'Toplevel', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Frame', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Button', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Label', _FakeWidget):
            state = {}
            ui._open_analysis_charts_window(
                parent=_FakeWidget(),
                conn=self.conn,
                human_only=True,
                state=state,
            )
        self.assertIsInstance(state['analysis_charts_window'], _FakeWidget)

    def test__open_categorical_analysis_dialog(self) -> None:
        fake_backend = mock.Mock(FigureCanvasTkAgg=_FakeMplCanvas)
        with mock.patch.object(ui.tk, 'Toplevel', _FakeWidget), \
                mock.patch.object(ui.tk, 'Canvas', _FakeWidget), \
                mock.patch.object(ui.tk, 'Text', _FakeText), \
                mock.patch.object(ui.ttk, 'Frame', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Scrollbar', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Button', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Label', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Treeview', _FakeTreeview), \
                mock.patch.dict('sys.modules', {'matplotlib.backends.backend_tkagg': fake_backend}):
            ui._open_categorical_analysis_dialog(parent=_FakeWidget(), conn=self.conn, human_only=True)
        self.assertTrue(_FakeWidget.instances)

    def test__make_table_tab(self) -> None:
        with mock.patch.object(ui.ttk, 'Frame', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Treeview', _FakeTreeview), \
                mock.patch.object(ui.ttk, 'Scrollbar', _FakeWidget):
            notebook = _FakeNotebook()
            tree = ui._make_table_tab(
                notebook=notebook,
                conn=self.conn,
                table_name='users',
                human_only=True,
            )
        self.assertIsInstance(tree, _FakeTreeview)
        self.assertEqual(len(notebook.tabs), 1)

    def test_start_gui(self) -> None:
        root = _FakeWidget()
        root.mainloop_called = False
        with mock.patch.object(ui, '_ensure_database'), \
                mock.patch.object(ui.sqlite3, 'connect', return_value=self.conn), \
                mock.patch.object(ui.tk, 'Tk', return_value=root), \
                mock.patch.object(ui.tk, 'BooleanVar', _FakeVar), \
                mock.patch.object(ui.ttk, 'Frame', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Button', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Checkbutton', _FakeWidget), \
                mock.patch.object(ui.ttk, 'Notebook', _FakeNotebook), \
                mock.patch.object(ui, '_make_table_tab', return_value=_FakeTreeview()), \
                mock.patch.object(ui.messagebox, 'askokcancel', return_value=False):
            ui.start_gui()
        self.assertTrue(root.mainloop_called)


class TestUtilities(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = sqlite3.connect(':memory:')
        self.conn.executescript(
            '''
            CREATE TABLE topics (
                topic_id TEXT PRIMARY KEY,
                topic_name TEXT NOT NULL,
                category TEXT,
                moderation_level TEXT,
                description TEXT
            );
            CREATE TABLE users (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                join_date TEXT,
                location TEXT,
                account_type TEXT,
                verified TEXT,
                followers_count INTEGER
            );
            CREATE TABLE posts (
                post_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                timestamp TEXT,
                content_type TEXT,
                content_preview TEXT,
                has_media TEXT,
                topic_id TEXT,
                language TEXT
            );
            CREATE TABLE interactions (
                interaction_id TEXT PRIMARY KEY,
                post_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                interaction_type TEXT,
                timestamp TEXT,
                reaction_type TEXT
            );
            INSERT INTO topics VALUES
                ('t1', 'Topic 1', 'Safety', 'low', NULL),
                ('t2', '   ', ' Policy ', ' high ', '  desc  ');
            INSERT INTO users VALUES
                ('u1', 'alice', '2024/01/02', ' London ', ' human ', 'true', '10'),
                ('u2', 'alice', 'bad', '', 'bot', 'FALSE', 'x'),
                ('u3', '   ', '', '', '', '', '');
            INSERT INTO posts VALUES
                ('p1', 'u1', '2024/01/03 12:00:00', ' text ', ' hello ', 'true', 't1', ' en '),
                ('p2', 'missing', 'bad', '', '', '', 'missing_topic', ''),
                ('p3', 'u2', '2024-01-04', 'text', 'bye', 'FALSE', 't1', 'en');
            INSERT INTO interactions VALUES
                ('i1', 'p1', 'u1', ' report ', '2024/01/05', ' like '),
                ('i2', 'missing', 'u1', 'like', 'bad', ''),
                ('i3', 'p3', 'u2', 'reply', '2024-01-06', NULL);
            ''',
        )

    def tearDown(self) -> None:
        self.conn.close()

    def test__nfc_optional(self) -> None:
        self.assertEqual(utilities._nfc_optional('  cafe\u0301  '), 'caf\xe9')
        self.assertIsNone(utilities._nfc_optional('   '))

    def test__cell_str(self) -> None:
        self.assertEqual(utilities._cell_str({'a': 3}, 'a'), '3')
        self.assertEqual(utilities._cell_str({}, 'a'), '')

    def test__parse_date_yyyy_mm_dd(self) -> None:
        self.assertEqual(utilities._parse_date_yyyy_mm_dd('2024/01/02 10:00'), '2024-01-02')
        self.assertEqual(utilities._parse_date_yyyy_mm_dd('03/01/2024'), '2024-01-03')
        self.assertIsNone(utilities._parse_date_yyyy_mm_dd('bad'))

    def test__normalise_bool_flag(self) -> None:
        self.assertEqual(utilities._normalise_bool_flag(' true '), 'TRUE')
        self.assertEqual(utilities._normalise_bool_flag('FALSE'), 'FALSE')
        self.assertIsNone(utilities._normalise_bool_flag('x'))

    def test__normalise_optional_int(self) -> None:
        self.assertEqual(utilities._normalise_optional_int(' 0 '), 0)
        self.assertIsNone(utilities._normalise_optional_int(''))
        self.assertIsNone(utilities._normalise_optional_int('x'))

    def test__fetch_one(self) -> None:
        self.assertEqual(
            utilities._fetch_one(self.conn, 'users', 'user_id', 'u1')['username'],
            'alice',
        )
        self.assertIsNone(utilities._fetch_one(self.conn, 'users', 'user_id', 'missing'))

    def test__quote_ident(self) -> None:
        self.assertEqual(utilities._quote_ident('a"b'), '"a""b"')

    def test__delete_post_cascade(self) -> None:
        utilities._delete_post_cascade(self.conn, 'p1')
        self.assertIsNone(self.conn.execute("SELECT 1 FROM posts WHERE post_id = 'p1'").fetchone())
        self.assertIsNone(self.conn.execute("SELECT 1 FROM interactions WHERE interaction_id = 'i1'").fetchone())

    def test__delete_user_cascade(self) -> None:
        utilities._delete_user_cascade(self.conn, 'u2')
        self.assertIsNone(self.conn.execute("SELECT 1 FROM users WHERE user_id = 'u2'").fetchone())
        self.assertIsNone(self.conn.execute("SELECT 1 FROM posts WHERE post_id = 'p3'").fetchone())
        self.assertIsNone(self.conn.execute("SELECT 1 FROM interactions WHERE interaction_id = 'i3'").fetchone())

    def test__user_ids_for_username(self) -> None:
        self.assertEqual(utilities._user_ids_for_username(self.conn, 'alice'), ['u1', 'u2'])

    def test__cleanup_topics(self) -> None:
        report = utilities.CleanupReport()
        utilities._cleanup_topics(self.conn, ['t2'], apply=True, report=report)
        self.assertIsNone(self.conn.execute("SELECT 1 FROM topics WHERE topic_id = 't2'").fetchone())
        self.assertEqual(report.deletes, 1)

    def test__cleanup_users(self) -> None:
        report = utilities.CleanupReport()
        utilities._cleanup_users(self.conn, ['u1', 'u2', 'u3'], apply=True, report=report)
        row = self.conn.execute("SELECT join_date, location, account_type, verified, followers_count FROM users WHERE user_id = 'u1'").fetchone()
        self.assertEqual(row, ('2024-01-02', 'London', 'human', 'TRUE', 10))
        self.assertIsNone(self.conn.execute("SELECT 1 FROM users WHERE user_id = 'u2'").fetchone())
        self.assertEqual(report.updates, 1)
        self.assertEqual(report.deletes, 1)

    def test__cleanup_posts(self) -> None:
        report = utilities.CleanupReport()
        utilities._cleanup_posts(self.conn, ['p1', 'p2'], apply=True, report=report)
        row = self.conn.execute(
            "SELECT timestamp, content_type, content_preview, has_media, topic_id, language FROM posts WHERE post_id = 'p1'",
        ).fetchone()
        self.assertEqual(row, ('2024-01-03', 'text', 'hello', 'TRUE', 't1', 'en'))
        self.assertIsNone(self.conn.execute("SELECT 1 FROM posts WHERE post_id = 'p2'").fetchone())

    def test__cleanup_interactions(self) -> None:
        report = utilities.CleanupReport()
        utilities._cleanup_interactions(self.conn, ['i1', 'i2'], apply=True, report=report)
        row = self.conn.execute(
            "SELECT interaction_type, timestamp, reaction_type FROM interactions WHERE interaction_id = 'i1'",
        ).fetchone()
        self.assertEqual(row, ('report', '2024-01-05', 'like'))
        self.assertIsNone(self.conn.execute("SELECT 1 FROM interactions WHERE interaction_id = 'i2'").fetchone())

    def test_cleanup_selection(self) -> None:
        with mock.patch.object(utilities, 'get_audit_logger', return_value=mock.Mock()):
            report = utilities.cleanup_selection(self.conn, 'posts', ['p1', 'p2'], apply=True)
        self.assertIn("Table 'posts', 2 row(s), apply=True", report.lines[0])
        self.assertTrue(report.lines[-1].startswith('Summary: '))

    def test_cleanup_entire_table(self) -> None:
        report = utilities.cleanup_entire_table(self.conn, 'interactions', apply=False)
        self.assertIn("Table 'interactions', 3 row(s), apply=False", report.lines[0])

    def test_format_report_for_dialog(self) -> None:
        report = utilities.CleanupReport(lines=['a', 'b', 'c'])
        self.assertEqual(utilities.format_report_for_dialog(report, max_lines=5), 'a\nb\nc')
        self.assertIn('more lines omitted', utilities.format_report_for_dialog(report, max_lines=2))


if __name__ == '__main__':
    unittest.main()
