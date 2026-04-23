from __future__ import annotations

import os
import sqlite3
import statistics
import tkinter as tk
from typing import cast
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from audit_log import LOG_FILE
from audit_log import get_audit_logger
from categorical_analysis import INTERPRETATION_TEXT
from categorical_analysis import build_categorical_analysis_figure
from categorical_analysis import query_three_way_distribution
from database import database_exists
from database import ensure_relational_schema
from hour_topic_pivot import build_hour_topic_pivot_figure
from hour_topic_pivot import build_pivot_matrix
from hour_topic_pivot import query_hour_topic_counts
from database import read_csv_rows
from database import replace_table_data_from_csv
from database import sql_exclude_bot_users
from database import table_name_for_csv
from moderation_effectiveness import DEFINITIONS_TEXT
from moderation_effectiveness import PLACEHOLDER_REPORTER_USER_ID
from moderation_effectiveness import build_moderation_correlation_figure
from moderation_effectiveness import build_moderation_effectiveness_figure
from moderation_effectiveness import run_moderation_effectiveness_analysis
from utilities import cleanup_entire_table
from utilities import format_report_for_dialog


TABLE_NAMES = (
    'users',
    'posts',
    'topics',
    'interactions',
)
DB_PATH = 'app.db'


def _log_error(context: str, exc: BaseException) -> None:
    """Record failures to log.txt and emit ERROR (and traceback) on stderr only."""
    get_audit_logger().error('%s: %s', context, exc, exc_info=True)


# Numeric columns that support mean / median / mode in Calculate Stats (per table).
ENGAGEMENT_NUMERIC_COLUMNS: dict[str, frozenset[str]] = {
    'users': frozenset({'followers_count'}),
}


def _ensure_database() -> None:
    if not database_exists(DB_PATH):
        open(DB_PATH, 'a').close()

    ensure_relational_schema(DB_PATH)


def _get_table_columns(conn: sqlite3.Connection, table_name: str) -> list[str]:
    rows = conn.execute(f'PRAGMA table_info({table_name})').fetchall()
    return [row[1] for row in rows]


def _fetch_table_rows_for_treeview(
        conn: sqlite3.Connection,
        table_name: str,
        *,
        human_only: bool,
) -> list[sqlite3.Row | tuple]:
    if not human_only or table_name == 'topics':
        return conn.execute(f'SELECT * FROM {table_name}').fetchall()
    u_pred = sql_exclude_bot_users(users_table_alias='u')
    if table_name == 'users':
        bare = sql_exclude_bot_users(users_table_alias=None)
        return conn.execute(f'SELECT * FROM users WHERE {bare}').fetchall()
    if table_name == 'posts':
        return conn.execute(
            f'SELECT p.* FROM posts p '
            f'INNER JOIN users u ON p.user_id = u.user_id '
            f'WHERE {u_pred}',
        ).fetchall()
    if table_name == 'interactions':
        return conn.execute(
            f'SELECT i.* FROM interactions i '
            f'INNER JOIN users u ON i.user_id = u.user_id '
            f'WHERE {u_pred}',
        ).fetchall()
    return conn.execute(f'SELECT * FROM {table_name}').fetchall()


def _human_only_from_state(state: dict[str, object]) -> bool:
    v = state.get('human_only_var')
    if isinstance(v, tk.BooleanVar):
        return bool(v.get())
    return False


_HUMAN_ONLY_CHECKBOX_BASE = 'Human only (hide bot rows)'


def _count_bot_hidden_rows(conn: sqlite3.Connection) -> int:
    """Total rows omitted from Users, Posts, and Interactions tabs when Human only is on."""
    bare = sql_exclude_bot_users(users_table_alias=None)
    u_pred = sql_exclude_bot_users(users_table_alias='u')
    n_u = conn.execute(
        f'SELECT COUNT(*) FROM users WHERE NOT ({bare})',
    ).fetchone()[0]
    n_p = conn.execute(
        f'SELECT COUNT(*) FROM posts p INNER JOIN users u ON p.user_id = u.user_id '
        f'WHERE NOT ({u_pred})',
    ).fetchone()[0]
    n_i = conn.execute(
        f'SELECT COUNT(*) FROM interactions i INNER JOIN users u ON i.user_id = u.user_id '
        f'WHERE NOT ({u_pred})',
    ).fetchone()[0]
    return int(n_u) + int(n_p) + int(n_i)


def _human_only_checkbox_label(conn: sqlite3.Connection, checked: bool) -> str:
    if not checked:
        return _HUMAN_ONLY_CHECKBOX_BASE
    n = _count_bot_hidden_rows(conn)
    return f'{_HUMAN_ONLY_CHECKBOX_BASE} ({n} hidden)'


def _populate_treeview(
        *,
        conn: sqlite3.Connection,
        table_name: str,
        treeview: ttk.Treeview,
        human_only: bool = False,
) -> None:
    columns = _get_table_columns(conn, table_name)

    treeview.delete(*treeview.get_children())
    treeview['columns'] = columns
    treeview['show'] = 'headings'

    for column in columns:
        treeview.heading(column, text=column)
        treeview.column(column, width=150, anchor=tk.W, stretch=True)

    rows = _fetch_table_rows_for_treeview(
        conn, table_name, human_only=human_only,
    )
    for row in rows:
        treeview.insert('', tk.END, values=row)


def _refresh_all_treeviews(
        *,
        conn: sqlite3.Connection,
        treeviews: dict[str, ttk.Treeview],
        human_only: bool = False,
) -> None:
    for table_name, treeview in treeviews.items():
        _populate_treeview(
            conn=conn,
            table_name=table_name,
            treeview=treeview,
            human_only=human_only,
        )


def _selected_rows(treeview: ttk.Treeview) -> list[tuple[str, ...]]:
    rows = []
    for item_id in treeview.selection():
        values = treeview.item(item_id, 'values')
        rows.append(tuple(str(value) for value in values))
    return rows


def _upload_csv(
        *,
        conn: sqlite3.Connection,
        state: dict[str, object],
        treeviews: dict[str, ttk.Treeview],
        human_only: bool,
) -> None:
    filename = filedialog.askopenfilename(
        filetypes=(('CSV files', '*.csv'), ('All files', '*.*')),
    )
    if not filename:
        return

    if not filename.lower().endswith('.csv'):
        get_audit_logger().warning('Upload rejected: file is not .csv: %s', filename)
        messagebox.showerror('Upload error', 'Selected file must have a .csv extension.')
        return

    table_name = table_name_for_csv(filename)
    if table_name not in TABLE_NAMES:
        allowed = ', '.join(name.upper() for name in TABLE_NAMES)
        get_audit_logger().warning(
            'Upload rejected: unknown table for file=%s',
            os.path.basename(filename),
        )
        messagebox.showerror(
            'Upload error',
            (
                'Selected CSV does not map to a known table.\n'
                f'Expected files for: {allowed}'
            ),
        )
        return

    try:
        headers, data_rows = read_csv_rows(filename)
    except ValueError as e:
        get_audit_logger().warning('Upload failed reading CSV (ValueError): %s', e)
        messagebox.showerror('Upload error', str(e))
        return
    except OSError as e:
        get_audit_logger().warning('Upload failed reading CSV (OSError): %s', e)
        messagebox.showerror('Upload error', f'Could not read file: {e}')
        return

    confirmed = messagebox.askyesno(
        'Confirm upload',
        (
            f'Replace the {table_name} table with {len(data_rows)} '
            f'data rows from:\n{os.path.basename(filename)}'
        ),
    )
    if not confirmed:
        get_audit_logger().info(
            'Upload cancelled by user table=%s file=%s',
            table_name,
            os.path.basename(filename),
        )
        messagebox.showinfo('Upload cancelled', 'CSV upload was cancelled.')
        return

    try:
        imported_table_name, headers, data_rows = replace_table_data_from_csv(
            DB_PATH,
            csv_path=filename,
            table_name=table_name,
            preloaded=(headers, data_rows),
        )
    except ValueError as e:
        get_audit_logger().warning('Upload failed during DB replace (ValueError): %s', e)
        messagebox.showerror('Upload error', str(e))
        return
    except OSError as e:
        get_audit_logger().warning('Upload failed during DB replace (OSError): %s', e)
        messagebox.showerror('Upload error', f'Could not read file: {e}')
        return
    except sqlite3.DatabaseError as e:
        _log_error('Upload CSV / replace_table_data_from_csv', e)
        messagebox.showerror('Upload error', f'Database update failed: {e}')
        return

    conn.close()
    conn = sqlite3.connect(DB_PATH)
    state['conn'] = conn
    state['uploaded_rows'] = [headers, *data_rows]
    state['uploaded_table'] = imported_table_name
    _refresh_all_treeviews(conn=conn, treeviews=treeviews, human_only=human_only)
    sync = state.get('sync_human_only_label')
    if callable(sync):
        sync()

    try:
        cleanup_report = cleanup_entire_table(conn, imported_table_name, apply=True)
    except Exception as e:
        _log_error('Upload CSV / cleanup after import', e)
        messagebox.showerror(
            'Cleanup error',
            (
                f'Data was loaded into {imported_table_name}, but automatic cleanup failed:\n{e}\n\n'
                'The imported CSV data is still in the database; cleanup was rolled back.'
            ),
        )
        return

    _refresh_all_treeviews(conn=conn, treeviews=treeviews, human_only=human_only)
    if callable(sync):
        sync()

    cleanup_text = format_report_for_dialog(cleanup_report, max_lines=45)
    get_audit_logger().info(
        'Upload finished: table=%s rows=%d file=%s cleanup_updates=%d cleanup_deletes=%d',
        imported_table_name,
        len(data_rows),
        os.path.basename(filename),
        cleanup_report.updates,
        cleanup_report.deletes,
    )
    messagebox.showinfo(
        'Upload complete',
        (
            f'Loaded {len(data_rows)} data rows into the {imported_table_name} table.\n\n'
            f'Automatic cleanup:\n{cleanup_text}'
        ),
    )


_FILTER_PAGE_SIZE = 50


def _close_filter_results_window(state: dict[str, object]) -> None:
    win = state.get('filter_results_window')
    if win is not None and isinstance(win, tk.Toplevel):
        try:
            if win.winfo_exists():
                win.destroy()
        except tk.TclError:
            pass
    state['filter_results_window'] = None


def _close_filter_pivot_window(state: dict[str, object]) -> None:
    win = state.get('filter_pivot_window')
    if win is not None and isinstance(win, tk.Toplevel):
        try:
            if win.winfo_exists():
                win.destroy()
        except tk.TclError:
            pass
    state['filter_pivot_window'] = None


def _filtered_posts_where_and_params(
        *,
        hour: int | None,
        topic_id: str | None,
) -> tuple[str, list[object]]:
    """Shared WHERE clause (non-bot posts) and positional parameters."""
    params: list[object] = []
    clauses: list[str] = []
    if hour is not None:
        clauses.append(
            '(CAST(strftime(\'%H\', replace(replace(p.timestamp, \'/\', \'-\'), \'T\', \' \')) AS INTEGER) = ?)',
        )
        params.append(hour)
    if topic_id:
        clauses.append('p.topic_id = ?')
        params.append(topic_id)
    where_sql = ' AND '.join(clauses) if clauses else '1 = 1'
    bot_sql = sql_exclude_bot_users(users_table_alias='u')
    full_where = f'({where_sql}) AND ({bot_sql})'
    return full_where, params


def _build_filtered_posts_count_sql(
        *,
        hour: int | None,
        topic_id: str | None,
) -> tuple[str, list[object]]:
    full_where, params = _filtered_posts_where_and_params(hour=hour, topic_id=topic_id)
    sql = f'''
        SELECT COUNT(*)
        FROM posts p
        INNER JOIN users u ON p.user_id = u.user_id
        WHERE {full_where}
    '''
    return sql, params


def _build_filtered_posts_select_sql(
        *,
        hour: int | None,
        topic_id: str | None,
        limit: int,
        offset: int,
) -> tuple[str, list[object]]:
    """Posts + topic columns; paginated with LIMIT / OFFSET."""
    full_where, params = _filtered_posts_where_and_params(hour=hour, topic_id=topic_id)
    sql = f'''
        SELECT
            p.post_id,
            p.user_id,
            p.timestamp,
            p.content_type,
            p.content_preview,
            p.has_media,
            p.topic_id,
            p.language,
            t.topic_name,
            t.category,
            t.moderation_level
        FROM posts p
        LEFT JOIN topics t ON p.topic_id = t.topic_id
        INNER JOIN users u ON p.user_id = u.user_id
        WHERE {full_where}
        ORDER BY p.timestamp, p.post_id
        LIMIT ? OFFSET ?
    '''
    return sql, [*params, limit, offset]


def _show_filtered_posts_window(
        *,
        parent: tk.Tk,
        state: dict[str, object],
        conn: sqlite3.Connection,
        column_names: list[str],
        hour: int | None,
        topic_id: str | None,
        total_count: int,
        page_size: int,
) -> None:
    win = tk.Toplevel(parent)
    win.title(f'Filtered posts ({total_count} match{"es" if total_count != 1 else ""})')
    win.transient(parent)
    win.geometry('1100x480')

    outer = ttk.Frame(win, padding=8)
    outer.grid(row=0, column=0, sticky='nsew')
    win.columnconfigure(0, weight=1)
    win.rowconfigure(0, weight=1)

    tree = ttk.Treeview(outer, columns=column_names, show='headings', selectmode='browse')
    vsb = ttk.Scrollbar(outer, orient='vertical', command=tree.yview)
    hsb = ttk.Scrollbar(outer, orient='horizontal', command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    for col in column_names:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor=tk.W, stretch=True)

    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')
    outer.columnconfigure(0, weight=1)
    outer.rowconfigure(0, weight=1)

    footer = ttk.Frame(win, padding=(8, 4, 8, 8))
    footer.grid(row=1, column=0, sticky='ew')
    nav = ttk.Frame(footer)
    nav.pack(side=tk.LEFT)
    status_var = tk.StringVar(value='')

    page: dict[str, int] = {'i': 0}

    def sync_nav_buttons() -> None:
        idx = page['i']
        if idx <= 0:
            btn_prev.state(['disabled'])
        else:
            btn_prev.state(['!disabled'])
        if total_count == 0 or (idx + 1) * page_size >= total_count:
            btn_next.state(['disabled'])
        else:
            btn_next.state(['!disabled'])

    def load_page() -> None:
        offset = page['i'] * page_size
        sql, params = _build_filtered_posts_select_sql(
            hour=hour,
            topic_id=topic_id,
            limit=page_size,
            offset=offset,
        )
        try:
            cur = conn.execute(sql, params)
            rows = cur.fetchall()
        except sqlite3.Error as e:
            _log_error('Filtered posts pagination', e)
            status_var.set(f'Load error: {e}')
            return

        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert('', tk.END, values=tuple('' if v is None else str(v) for v in row))

        n = len(rows)
        if total_count == 0:
            status_var.set('No rows match this filter.')
        else:
            start_i = offset + 1
            end_i = offset + n
            remaining_after = max(0, total_count - end_i)
            parts = [
                f'Rows {start_i}–{end_i} of {total_count}',
                f'{remaining_after} more row(s) to show (use >)',
            ]
            if offset > 0:
                parts.append(f'{offset} row(s) on earlier pages (<)')
            status_var.set(' · '.join(parts))
        sync_nav_buttons()

    def go_prev() -> None:
        if page['i'] > 0:
            page['i'] -= 1
            load_page()

    def go_next() -> None:
        if (page['i'] + 1) * page_size < total_count:
            page['i'] += 1
            load_page()

    btn_prev = ttk.Button(nav, text='<', width=3, command=go_prev)
    btn_next = ttk.Button(nav, text='>', width=3, command=go_next)
    btn_prev.pack(side=tk.LEFT)
    btn_next.pack(side=tk.LEFT, padx=(4, 0))
    ttk.Label(footer, textvariable=status_var, wraplength=620).pack(side=tk.LEFT, padx=(12, 0))
    ttk.Button(footer, text='Close', command=win.destroy).pack(side=tk.RIGHT)

    load_page()

    def on_win_destroy(event: tk.Event) -> None:
        if event.widget == win:
            state['filter_results_window'] = None

    win.bind('<Destroy>', on_win_destroy)
    state['filter_results_window'] = win


def _show_hour_topic_pivot_window(
        *,
        parent: tk.Tk,
        state: dict[str, object],
        conn: sqlite3.Connection,
        hour_filter: int | None,
        topic_id_filter: str | None,
) -> None:
    """Second window: heatmap + numeric grid; same filter population as post list (no row cap)."""
    _close_filter_pivot_window(state)

    try:
        raw_rows = query_hour_topic_counts(
            conn,
            hour_filter=hour_filter,
            topic_id_filter=topic_id_filter,
        )
    except sqlite3.Error as e:
        _log_error('Apply filters / hour-topic pivot query', e)
        messagebox.showerror('Pivot error', f'Could not build hour × topic pivot: {e}', parent=parent)
        return

    matrix, _topic_keys, topic_labels = build_pivot_matrix(raw_rows)
    filt_bits: list[str] = []
    if hour_filter is not None:
        filt_bits.append(f'hour={hour_filter}')
    if topic_id_filter:
        filt_bits.append(f'topic_id={topic_id_filter!r}')
    else:
        filt_bits.append('all topics (includes (no topic) where applicable)')
    subtitle = 'Filters: ' + ', '.join(filt_bits)

    win = tk.Toplevel(parent)
    win.title('Posting activity: hour × topic (pivot)')
    win.transient(parent)
    win.geometry('1000x720')
    win.columnconfigure(0, weight=1)
    win.rowconfigure(0, weight=2)
    win.rowconfigure(1, weight=1)

    chart_frame = ttk.Frame(win, padding=4)
    chart_frame.grid(row=0, column=0, sticky='nsew')
    table_frame = ttk.Frame(win, padding=4)
    table_frame.grid(row=1, column=0, sticky='nsew')
    table_frame.columnconfigure(0, weight=1)
    table_frame.rowconfigure(0, weight=1)

    footer = ttk.Frame(win, padding=(8, 4))
    footer.grid(row=2, column=0, sticky='ew')
    ttk.Label(
        footer,
        text=(
            f'{subtitle}. Non-bot posts only; rows with unparseable timestamps are omitted. '
            'Topic columns are sorted by total post volume (desc).'
        ),
        wraplength=960,
    ).pack(side=tk.LEFT)
    ttk.Button(footer, text='Close', command=win.destroy).pack(side=tk.RIGHT)

    try:
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        fig = build_hour_topic_pivot_figure(matrix, topic_labels)
        canvas_mpl = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas_mpl.draw()
        canvas_mpl.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    except ImportError as e:
        ttk.Label(
            chart_frame,
            text=f'Heatmap requires matplotlib. pip install -r requirements.txt\n{e}',
        ).pack(anchor='w')
    except Exception as e:
        _log_error('Hour-topic pivot / chart', e)
        ttk.Label(chart_frame, text=f'Could not draw heatmap: {e}').pack(anchor='w')

    cols = ['hour'] + topic_labels
    tree = ttk.Treeview(table_frame, columns=cols, show='headings', height=10)
    vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.heading('hour', text='Hour')
    tree.column('hour', width=50, anchor=tk.CENTER, stretch=False)
    for lab in topic_labels:
        tree.heading(lab, text=lab)
        tree.column(lab, width=72, anchor=tk.E, stretch=True)

    n_topics = int(matrix.shape[1]) if matrix.size else 0
    for h in range(24):
        vals: list[str] = [str(h)]
        for j in range(n_topics):
            vals.append(str(int(matrix[h, j])))
        tree.insert('', tk.END, values=tuple(vals))

    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')

    def on_win_destroy(event: tk.Event) -> None:
        if event.widget == win:
            state['filter_pivot_window'] = None

    win.bind('<Destroy>', on_win_destroy)
    state['filter_pivot_window'] = win

    get_audit_logger().info(
        'Hour-topic pivot opened: raw_cells=%d topic_columns=%d hour_filter=%s topic_filter=%s',
        len(raw_rows),
        n_topics,
        hour_filter,
        topic_id_filter,
    )


def _open_filters_dialog(*, parent: tk.Tk, state: dict[str, object]) -> None:
    conn = cast(sqlite3.Connection, state['conn'])
    get_audit_logger().info('Filter dialog opened')
    dialog = tk.Toplevel(parent)
    dialog.title('Apply filters')
    dialog.transient(parent)
    dialog.resizable(False, False)

    hour_var = tk.StringVar()

    frame = ttk.Frame(dialog, padding=16)
    frame.grid(sticky='nsew')

    ttk.Label(
        frame,
        text='Hour of day (0-23), optional — leave empty for no hour filter',
    ).grid(row=0, column=0, sticky='w')
    hour_entry = ttk.Entry(frame, textvariable=hour_var, width=20)
    hour_entry.grid(row=1, column=0, sticky='ew', pady=(4, 12))

    ttk.Label(
        frame,
        text='Topic (from topics table), optional — "(no topic filter)" for all topics',
    ).grid(row=2, column=0, sticky='w')
    topic_rows = conn.execute(
        'SELECT topic_id, topic_name FROM topics ORDER BY topic_id',
    ).fetchall()
    topic_labels = ['(no topic filter)'] + [
        f'{tid} — {name}' for tid, name in topic_rows
    ]
    topic_combo = ttk.Combobox(
        frame,
        state='readonly',
        values=topic_labels,
        width=48,
    )
    topic_combo.grid(row=3, column=0, sticky='ew', pady=(4, 12))

    prev = cast(dict[str, object], state.get('filters') or {})
    if prev.get('hour_of_day') is not None:
        hour_var.set(str(prev['hour_of_day']))
    tid_prev = prev.get('topic_id')
    if tid_prev:
        for i, (row_id, _name) in enumerate(topic_rows, start=1):
            if row_id == tid_prev:
                topic_combo.current(i)
                break
        else:
            topic_combo.current(0)
    else:
        topic_combo.current(0)

    def submit() -> None:
        hour_text = hour_var.get().strip()
        hour: int | None = None
        if hour_text:
            try:
                hour = int(hour_text)
            except ValueError:
                get_audit_logger().warning('Filter apply failed: hour not an integer')
                messagebox.showerror(
                    'Filter error',
                    'Hour of day must be an integer between 0 and 23.',
                    parent=dialog,
                )
                return
            if hour < 0 or hour > 23:
                get_audit_logger().warning('Filter apply failed: hour out of range %s', hour)
                messagebox.showerror(
                    'Filter error',
                    'Hour of day must be between 0 and 23.',
                    parent=dialog,
                )
                return

        sel = topic_combo.get()
        topic_id: str | None = None
        if sel and not sel.startswith('(no topic filter)'):
            topic_id = sel.split(' — ', 1)[0].strip()

        state['filters'] = {'hour_of_day': hour, 'topic_id': topic_id}

        _close_filter_results_window(state)
        _close_filter_pivot_window(state)

        count_sql, count_params = _build_filtered_posts_count_sql(hour=hour, topic_id=topic_id)
        meta_sql, meta_params = _build_filtered_posts_select_sql(
            hour=hour,
            topic_id=topic_id,
            limit=0,
            offset=0,
        )
        try:
            total_count = int(conn.execute(count_sql, count_params).fetchone()[0])
            cur = conn.execute(meta_sql, meta_params)
            colnames = [d[0] for d in cur.description] if cur.description else []
        except sqlite3.Error as e:
            _log_error('Apply filters / filtered posts query', e)
            messagebox.showerror('Filter error', f'Query failed: {e}', parent=dialog)
            return

        _show_filtered_posts_window(
            parent=parent,
            state=state,
            conn=conn,
            column_names=colnames,
            hour=hour,
            topic_id=topic_id,
            total_count=total_count,
            page_size=_FILTER_PAGE_SIZE,
        )
        _show_hour_topic_pivot_window(
            parent=parent,
            state=state,
            conn=conn,
            hour_filter=hour,
            topic_id_filter=topic_id,
        )
        get_audit_logger().info(
            'Filters applied: hour_of_day=%s topic_id=%s total_matches=%d page_size=%d',
            hour,
            topic_id,
            total_count,
            _FILTER_PAGE_SIZE,
        )

    button_frame = ttk.Frame(frame)
    button_frame.grid(row=4, column=0, sticky='e')

    ttk.Button(button_frame, text='Cancel', command=dialog.destroy).grid(
        row=0, column=0, padx=(0, 8),
    )
    ttk.Button(button_frame, text='Apply', command=submit).grid(row=0, column=1)

    dialog.columnconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    hour_entry.focus()


def _account_type_is_bot(account_type: str | None) -> bool:
    if account_type is None:
        return False
    return str(account_type).strip().lower() == 'bot'


def _user_id_is_bot(
        conn: sqlite3.Connection,
        user_id: str,
        *,
        cache: dict[str, bool],
) -> bool:
    if user_id in cache:
        return cache[user_id]
    row = conn.execute(
        'SELECT account_type FROM users WHERE user_id = ?',
        (user_id,),
    ).fetchone()
    if row is None:
        cache[user_id] = False
        return False
    cache[user_id] = _account_type_is_bot(row[0])
    return cache[user_id]


def _record_is_bot_excluded(
        conn: sqlite3.Connection,
        table_name: str,
        record: dict[str, str],
        *,
        cache: dict[str, bool],
) -> bool:
    """True if this row should be excluded from human engagement stats (bot)."""
    if table_name == 'users':
        return _account_type_is_bot(record.get('account_type'))
    if table_name == 'posts':
        uid = (record.get('user_id') or '').strip()
        if not uid:
            return False
        return _user_id_is_bot(conn, uid, cache=cache)
    if table_name == 'interactions':
        uid = (record.get('user_id') or '').strip()
        if not uid:
            return False
        return _user_id_is_bot(conn, uid, cache=cache)
    return False


def _parse_engagement_value(column: str, raw: str) -> float | None:
    s = (raw or '').strip()
    if not s:
        return None
    try:
        if column == 'followers_count':
            return float(int(s, 10))
        return float(s)
    except ValueError:
        return None


def _format_mode_list(modes: list[float]) -> str:
    if not modes:
        return 'n/a'
    as_int = all(m == int(m) for m in modes)
    shown = [int(m) if as_int else m for m in modes]
    if len(shown) <= 5:
        return ', '.join(str(x) for x in sorted(shown, key=lambda x: (str(type(x)), x)))
    return f'{len(shown)} distinct modes'


def _show_selected_row_stats(
        *,
        parent: tk.Tk,
        conn: sqlite3.Connection,
        notebook: ttk.Notebook,
        treeviews: dict[str, ttk.Treeview],
) -> None:
    index = notebook.index(notebook.select())
    table_name = TABLE_NAMES[index]
    treeview = treeviews[table_name]

    rows = _selected_rows(treeview)
    if not rows:
        get_audit_logger().warning('Statistics requested with no row selection')
        messagebox.showerror(
            'Statistics error',
            'Select one or more rows in the current table first.',
            parent=parent,
        )
        return

    confirmed = messagebox.askyesno(
        'Confirm statistics',
        f'Calculate engagement statistics for {len(rows)} selected row(s)?',
        parent=parent,
    )
    if not confirmed:
        get_audit_logger().info('Statistics calculation cancelled by user')
        messagebox.showinfo(
            'Statistics cancelled',
            'Statistics calculation was cancelled.',
            parent=parent,
        )
        return

    columns = _get_table_columns(conn, table_name)
    records: list[dict[str, str]] = []
    for row in rows:
        rec: dict[str, str] = {}
        for i, col in enumerate(columns):
            rec[col] = str(row[i]) if i < len(row) else ''
        records.append(rec)

    bot_cache: dict[str, bool] = {}
    usable = [
        r for r in records
        if not _record_is_bot_excluded(conn, table_name, r, cache=bot_cache)
    ]
    skipped_bots = len(records) - len(usable)

    engagement_cols = ENGAGEMENT_NUMERIC_COLUMNS.get(table_name, frozenset())

    lines = [
        f'Table: {table_name}',
        f'Rows selected: {len(rows)} ({len(usable)} non-bot, {skipped_bots} bot skipped)',
    ]

    if not engagement_cols:
        lines.append('No engagement numeric columns defined for this table.')
        get_audit_logger().info(
            'Statistics: no engagement columns for table=%s selected_rows=%d',
            table_name,
            len(rows),
        )
        messagebox.showinfo('Statistics', '\n'.join(lines), parent=parent)
        return

    if not usable:
        lines.append('All selected rows were skipped (bots or missing user link).')
        get_audit_logger().info(
            'Statistics: all rows skipped (bots) table=%s selected_rows=%d',
            table_name,
            len(rows),
        )
        messagebox.showinfo('Statistics', '\n'.join(lines), parent=parent)
        return

    for col in sorted(engagement_cols):
        if col not in columns:
            lines.append(f'{col}: (column not in current table view)')
            continue
        vals: list[float] = []
        for rec in usable:
            v = _parse_engagement_value(col, rec.get(col, ''))
            if v is not None:
                vals.append(v)
        if not vals:
            lines.append(f'{col}: no numeric values in non-bot selection')
            continue
        mean_v = statistics.fmean(vals)
        median_v = statistics.median(vals)
        modes = statistics.multimode(vals)
        lines.append(
            f'{col}: n={len(vals)}  mean={mean_v:.4g}  median={median_v:.4g}  '
            f'mode={_format_mode_list(modes)}',
        )

    get_audit_logger().info(
        'Statistics calculated: table=%s selected=%d non_bot=%d bot_skipped=%d',
        table_name,
        len(rows),
        len(usable),
        skipped_bots,
    )
    messagebox.showinfo('Statistics', '\n'.join(lines), parent=parent)


def _open_moderation_effectiveness_dialog(
        *,
        parent: tk.Tk,
        conn: sqlite3.Connection,
) -> None:
    try:
        result = run_moderation_effectiveness_analysis(conn)
    except sqlite3.Error as e:
        _log_error('Moderation effectiveness analysis', e)
        messagebox.showerror(
            'Moderation effectiveness',
            f'Query failed: {e}',
            parent=parent,
        )
        return

    win = tk.Toplevel(parent)
    win.title('Moderation effectiveness')
    win.transient(parent)
    win.minsize(880, 640)
    win.geometry('1024x820')

    footer = ttk.Frame(win, padding=(8, 6))
    footer.pack(side=tk.BOTTOM, fill=tk.X)
    ttk.Label(
        footer,
        text=(
            'Footnote: reports are human-only; interaction_type = report (case-insensitive). '
            f'Ignored {result.ignored_placeholder_reports} report interaction(s) linked to '
            f'placeholder user {PLACEHOLDER_REPORTER_USER_ID}.'
        ),
        wraplength=960,
    ).pack(side=tk.LEFT)
    ttk.Button(footer, text='Close', command=win.destroy).pack(side=tk.RIGHT)

    main = ttk.Frame(win)
    main.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main, highlightthickness=0)
    vsb = ttk.Scrollbar(main, orient=tk.VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    body = ttk.Frame(canvas, padding=8)
    body_win = canvas.create_window((0, 0), window=body, anchor='nw')

    def _sync_scroll(_event: object | None = None) -> None:
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'))

    def _on_canvas_configure(event: tk.Event) -> None:
        canvas.itemconfigure(body_win, width=event.width)

    body.bind('<Configure>', lambda _e: _sync_scroll())
    canvas.bind('<Configure>', _on_canvas_configure)

    def _wheel_mouse(event: tk.Event) -> None:
        if event.delta:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

    win.bind('<MouseWheel>', _wheel_mouse)
    win.bind('<Button-4>', lambda _e: canvas.yview_scroll(-1, 'units'))
    win.bind('<Button-5>', lambda _e: canvas.yview_scroll(1, 'units'))

    body.columnconfigure(0, weight=1)
    r = 0
    ttk.Label(body, text='Definitions', font=('TkDefaultFont', 10, 'bold')).grid(
        row=r, column=0, sticky='w',
    )
    r += 1
    def_box = tk.Text(body, height=5, wrap='word', width=110, font=('TkDefaultFont', 9))
    def_box.insert('1.0', DEFINITIONS_TEXT)
    def_box.configure(state='disabled')
    def_box.grid(row=r, column=0, sticky='ew', pady=(0, 8))
    r += 1

    ttk.Label(body, text='Summary statistics', font=('TkDefaultFont', 10, 'bold')).grid(
        row=r, column=0, sticky='w',
    )
    r += 1
    stats_box = tk.Text(body, height=7, wrap='word', width=110, font=('TkDefaultFont', 9))
    stats_box.insert('1.0', '\n'.join(result.summary_stats_lines))
    stats_box.configure(state='disabled')
    stats_box.grid(row=r, column=0, sticky='ew', pady=(0, 8))
    r += 1

    ttk.Label(body, text='Visualisations', font=('TkDefaultFont', 10, 'bold')).grid(
        row=r, column=0, sticky='w',
    )
    r += 1
    chart_frame = ttk.Frame(body)
    chart_frame.grid(row=r, column=0, sticky='ew', pady=(0, 8))
    r += 1
    try:
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        fig = build_moderation_effectiveness_figure(result)
        mpl_canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        mpl_canvas.draw()
        mpl_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    except ImportError as e:
        ttk.Label(
            chart_frame,
            text=(
                'Charts require matplotlib. Install with: pip install -r requirements.txt\n'
                f'Detail: {e}'
            ),
        ).pack(anchor='w')
    except Exception as e:
        _log_error('Moderation effectiveness / charts', e)
        ttk.Label(chart_frame, text=f'Could not build charts: {e}').pack(anchor='w')

    ttk.Label(
        body,
        text='Correlation (moderation level vs reporting)',
        font=('TkDefaultFont', 10, 'bold'),
    ).grid(row=r, column=0, sticky='w')
    r += 1
    ttk.Label(
        body,
        text=(
            'Left: each point is one topic — x = moderation label as ordinal (low=0, medium=1, high=2), '
            'y = human reports per in-scope post; point size scales with topic post volume; dashed line = OLS. '
            'Right: mean topic reports/post within each label, error bars = sample s.d. across topics.'
        ),
        wraplength=960,
        font=('TkDefaultFont', 9),
    ).grid(row=r, column=0, sticky='w', pady=(0, 4))
    r += 1
    corr_frame = ttk.Frame(body)
    corr_frame.grid(row=r, column=0, sticky='ew', pady=(0, 8))
    r += 1
    try:
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        fig_corr, r_pearson = build_moderation_correlation_figure(result)
        corr_canvas = FigureCanvasTkAgg(fig_corr, master=corr_frame)
        corr_canvas.draw()
        corr_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        if r_pearson is not None:
            get_audit_logger().info(
                'Moderation correlation figure: Pearson r (ordinal moderation vs topic report rate) = %.4f',
                r_pearson,
            )
        else:
            get_audit_logger().info(
                'Moderation correlation figure: Pearson r not defined (insufficient variation or data)',
            )
    except ImportError as e:
        ttk.Label(
            corr_frame,
            text=f'Correlation charts need matplotlib.\n{e}',
        ).pack(anchor='w')
    except Exception as e:
        _log_error('Moderation effectiveness / correlation charts', e)
        ttk.Label(corr_frame, text=f'Could not build correlation charts: {e}').pack(anchor='w')

    ttk.Label(body, text='Pattern detection', font=('TkDefaultFont', 10, 'bold')).grid(
        row=r, column=0, sticky='w',
    )
    r += 1
    pat_h = min(18, max(8, len(result.pattern_messages) * 2 + 2))
    pat_box = tk.Text(body, height=pat_h, wrap='word', width=110, font=('TkDefaultFont', 9))
    pat_box.insert('1.0', '\n\n'.join(result.pattern_messages))
    pat_box.configure(state='disabled')
    pat_box.grid(row=r, column=0, sticky='ew', pady=(0, 8))
    r += 1

    ttk.Label(body, text='Aggregate table (category × moderation level)', font=('TkDefaultFont', 10, 'bold')).grid(
        row=r, column=0, sticky='w',
    )
    r += 1
    table_frame = ttk.Frame(body)
    table_frame.grid(row=r, column=0, sticky='nsew', pady=(0, 4))
    table_frame.columnconfigure(0, weight=1)
    table_frame.rowconfigure(0, weight=1)

    colnames = result.summary_colnames
    tree = ttk.Treeview(
        table_frame,
        columns=colnames,
        show='headings',
        selectmode='browse',
        height=8,
    )
    tr_vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    tr_hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(yscrollcommand=tr_vsb.set, xscrollcommand=tr_hsb.set)

    for col in colnames:
        tree.heading(col, text=col.replace('_', ' '))
        tree.column(col, width=120, anchor=tk.W, stretch=True)

    for row in result.summary_rows:
        display: list[str] = []
        for v in row:
            if v is None:
                display.append('')
            elif isinstance(v, float):
                display.append(f'{v:.4f}')
            else:
                display.append(str(v))
        tree.insert('', tk.END, values=tuple(display))

    tree.grid(row=0, column=0, sticky='nsew')
    tr_vsb.grid(row=0, column=1, sticky='ns')
    tr_hsb.grid(row=1, column=0, sticky='ew')

    get_audit_logger().info(
        'Moderation effectiveness opened: summary_buckets=%d topics=%d ignored_reports=%d patterns=%d',
        len(result.summary_rows),
        len(result.topic_rows),
        result.ignored_placeholder_reports,
        len(result.pattern_messages),
    )
    for msg in result.pattern_messages:
        get_audit_logger().info('Moderation pattern: %s', msg)


def _close_analysis_charts_window(state: dict[str, object]) -> None:
    win = state.get('analysis_charts_window')
    if win is not None and isinstance(win, tk.Toplevel):
        try:
            if win.winfo_exists():
                win.destroy()
        except tk.TclError:
            pass
    state['analysis_charts_window'] = None


def _open_analysis_charts_window(
        *,
        parent: tk.Tk,
        conn: sqlite3.Connection,
        human_only: bool,
        state: dict[str, object],
) -> None:
    try:
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
    except ImportError as e:
        get_audit_logger().warning('Analysis charts unavailable (missing dependency): %s', e)
        messagebox.showerror(
            'Analysis charts',
            (
                'Matplotlib (and friends) are not installed. '
                'Install dependencies from requirements.txt, e.g. '
                '`pip install -r requirements.txt`.\n\n'
                f'Detail: {e}'
            ),
            parent=parent,
        )
        return

    _close_analysis_charts_window(state)

    try:
        from analysis import build_analysis_figure

        fig = build_analysis_figure(conn, human_only=human_only)
    except Exception as e:
        _log_error('Analysis charts / build_analysis_figure', e)
        messagebox.showerror(
            'Analysis charts',
            f'Could not build charts: {e}',
            parent=parent,
        )
        return

    win = tk.Toplevel(parent)
    win.title('Data analysis (time series)')
    win.transient(parent)
    win.geometry('1000x750')

    outer = ttk.Frame(win, padding=8)
    outer.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    canvas = FigureCanvasTkAgg(fig, master=outer)
    canvas.draw()
    toolbar = NavigationToolbar2Tk(canvas, outer, pack_toolbar=False)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    footer = ttk.Frame(win, padding=(8, 0, 8, 8))
    footer.pack(side=tk.BOTTOM, fill=tk.X)
    ttk.Label(
        footer,
        text='Series use the same Human only rule as the table tabs (bot rows excluded when checked).',
        wraplength=720,
    ).pack(side=tk.LEFT)
    ttk.Button(footer, text='Close', command=win.destroy).pack(side=tk.RIGHT)

    def on_win_destroy(event: tk.Event) -> None:
        if event.widget == win:
            state['analysis_charts_window'] = None

    win.bind('<Destroy>', on_win_destroy)
    state['analysis_charts_window'] = win
    get_audit_logger().info('Analysis charts window opened human_only=%s', human_only)


def _open_categorical_analysis_dialog(
        *,
        parent: tk.Tk,
        conn: sqlite3.Connection,
        human_only: bool,
) -> None:
    """Three-way breakdown: category × moderation_level × content_type."""
    try:
        rows = query_three_way_distribution(conn, human_only=human_only)
    except sqlite3.Error as e:
        _log_error('Categorical analysis query', e)
        messagebox.showerror('Categorical analysis', f'Query failed: {e}', parent=parent)
        return

    total_posts = sum(r[3] for r in rows)
    win = tk.Toplevel(parent)
    win.title('Categorical analysis (3 dimensions)')
    win.transient(parent)
    win.geometry('960x780')

    footer = ttk.Frame(win, padding=(8, 6))
    footer.pack(side=tk.BOTTOM, fill=tk.X)
    ttk.Label(
        footer,
        text=(
            f'Total posts counted (sum of cells): {total_posts}. '
            f'Distinct (category, moderation_level, content_type) cells: {len(rows)}. '
            f'Human only (exclude bots): {human_only}.'
        ),
        wraplength=900,
    ).pack(side=tk.LEFT)
    ttk.Button(footer, text='Close', command=win.destroy).pack(side=tk.RIGHT)

    main = ttk.Frame(win)
    main.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main, highlightthickness=0)
    vsb = ttk.Scrollbar(main, orient=tk.VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    body = ttk.Frame(canvas, padding=8)
    body_win = canvas.create_window((0, 0), window=body, anchor='nw')

    def _sync_scroll(_event: object | None = None) -> None:
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'))

    def _on_canvas_configure(event: tk.Event) -> None:
        canvas.itemconfigure(body_win, width=event.width)

    body.bind('<Configure>', lambda _e: _sync_scroll())
    canvas.bind('<Configure>', _on_canvas_configure)

    def _wheel_mouse(event: tk.Event) -> None:
        if event.delta:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

    win.bind('<MouseWheel>', _wheel_mouse)
    win.bind('<Button-4>', lambda _e: canvas.yview_scroll(-1, 'units'))
    win.bind('<Button-5>', lambda _e: canvas.yview_scroll(1, 'units'))

    body.columnconfigure(0, weight=1)
    r = 0
    ttk.Label(body, text='What this shows', font=('TkDefaultFont', 10, 'bold')).grid(
        row=r, column=0, sticky='w',
    )
    r += 1
    intro = tk.Text(body, height=6, wrap='word', width=105, font=('TkDefaultFont', 9))
    intro.insert('1.0', INTERPRETATION_TEXT)
    intro.configure(state='disabled')
    intro.grid(row=r, column=0, sticky='ew', pady=(0, 8))
    r += 1

    ttk.Label(body, text='Charts', font=('TkDefaultFont', 10, 'bold')).grid(row=r, column=0, sticky='w')
    r += 1
    chart_frame = ttk.Frame(body)
    chart_frame.grid(row=r, column=0, sticky='ew', pady=(0, 8))
    r += 1
    try:
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        fig = build_categorical_analysis_figure(rows)
        mpl_canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        mpl_canvas.draw()
        mpl_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    except ImportError as e:
        ttk.Label(
            chart_frame,
            text=f'Charts require matplotlib.\n{e}',
        ).pack(anchor='w')
    except Exception as e:
        _log_error('Categorical analysis / charts', e)
        ttk.Label(chart_frame, text=f'Could not build charts: {e}').pack(anchor='w')

    ttk.Label(body, text='Full cell listing (sorted by count)', font=('TkDefaultFont', 10, 'bold')).grid(
        row=r, column=0, sticky='w',
    )
    r += 1
    table_frame = ttk.Frame(body)
    table_frame.grid(row=r, column=0, sticky='nsew', pady=(0, 4))
    table_frame.columnconfigure(0, weight=1)
    table_frame.rowconfigure(0, weight=1)

    cols = ('category', 'moderation_level', 'content_type', 'count')
    tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show='headings',
        selectmode='browse',
        height=12,
    )
    tr_vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    tr_hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(yscrollcommand=tr_vsb.set, xscrollcommand=tr_hsb.set)
    tree.heading('category', text='category')
    tree.heading('moderation_level', text='moderation_level')
    tree.heading('content_type', text='content_type')
    tree.heading('count', text='count')
    tree.column('category', width=140, anchor=tk.W, stretch=True)
    tree.column('moderation_level', width=110, anchor=tk.W, stretch=True)
    tree.column('content_type', width=100, anchor=tk.W, stretch=True)
    tree.column('count', width=70, anchor=tk.E, stretch=False)

    for cat, mod, ctype, cnt in rows:
        tree.insert('', tk.END, values=(cat, mod, ctype or '(empty)', str(cnt)))

    tree.grid(row=0, column=0, sticky='nsew')
    tr_vsb.grid(row=0, column=1, sticky='ns')
    tr_hsb.grid(row=1, column=0, sticky='ew')

    get_audit_logger().info(
        'Categorical analysis opened: human_only=%s cells=%d total_posts=%d',
        human_only,
        len(rows),
        total_posts,
    )


def _make_table_tab(
        *,
        notebook: ttk.Notebook,
        conn: sqlite3.Connection,
        table_name: str,
        human_only: bool,
) -> ttk.Treeview:
    frame = ttk.Frame(notebook, padding=8)
    notebook.add(frame, text=table_name.replace('_', ' ').title())

    treeview = ttk.Treeview(frame, selectmode='extended')
    treeview.grid(row=0, column=0, sticky='nsew')

    scrollbar = ttk.Scrollbar(frame, orient='vertical', command=treeview.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    treeview.configure(yscrollcommand=scrollbar.set)

    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    _populate_treeview(
        conn=conn,
        table_name=table_name,
        treeview=treeview,
        human_only=human_only,
    )
    return treeview


def start_gui() -> None:
    get_audit_logger().info('GUI starting database_path=%s log_file=%s', DB_PATH, LOG_FILE)
    _ensure_database()
    conn = sqlite3.connect(DB_PATH)
    state: dict[str, object] = {
        'conn': conn,
        'uploaded_rows': [],
        'uploaded_table': None,
        'filters': {},
        'filter_results_window': None,
        'filter_pivot_window': None,
        'analysis_charts_window': None,
    }

    root = tk.Tk()
    root.title('Data Review Tool')
    root.geometry('1120x600')

    human_only_var = tk.BooleanVar(value=False)
    state['human_only_var'] = human_only_var

    outer = ttk.Frame(root, padding=12)
    outer.grid(sticky='nsew')

    controls = ttk.Frame(outer)
    controls.grid(row=0, column=0, sticky='ew', pady=(0, 12))

    notebook = ttk.Notebook(outer)
    notebook.grid(row=1, column=0, sticky='nsew')

    treeviews: dict[str, ttk.Treeview] = {}
    for table_name in TABLE_NAMES:
        treeviews[table_name] = _make_table_tab(
            notebook=notebook,
            conn=conn,
            table_name=table_name,
            human_only=human_only_var.get(),
        )

    bottom_bar = ttk.Frame(outer)
    bottom_bar.grid(row=2, column=0, sticky='ew', pady=(8, 0))

    def sync_human_only_label() -> None:
        c = cast(sqlite3.Connection, state['conn'])
        human_only_check.configure(
            text=_human_only_checkbox_label(c, human_only_var.get()),
        )

    state['sync_human_only_label'] = sync_human_only_label

    def _on_human_only_toggle() -> None:
        _refresh_all_treeviews(
            conn=cast(sqlite3.Connection, state['conn']),
            treeviews=treeviews,
            human_only=human_only_var.get(),
        )
        sync_human_only_label()
        get_audit_logger().info(
            'Human only filter toggled: %s',
            human_only_var.get(),
        )

    human_only_check = ttk.Checkbutton(
        bottom_bar,
        text=_HUMAN_ONLY_CHECKBOX_BASE,
        variable=human_only_var,
        command=_on_human_only_toggle,
    )
    human_only_check.pack(side=tk.LEFT)

    ttk.Button(
        controls,
        text='Upload CSV',
        command=lambda: _upload_csv(
            conn=state['conn'],
            state=state,
            treeviews=treeviews,
            human_only=_human_only_from_state(state),
        ),
    ).grid(row=0, column=0, padx=(0, 8))
    ttk.Button(
        controls,
        text='Apply Filters',
        command=lambda: _open_filters_dialog(parent=root, state=state),
    ).grid(row=0, column=1, padx=(0, 8))
    ttk.Button(
        controls,
        text='Calculate Stats',
        command=lambda: _show_selected_row_stats(
            parent=root,
            conn=state['conn'],
            notebook=notebook,
            treeviews=treeviews,
        ),
    ).grid(row=0, column=2, padx=(0, 8))
    ttk.Button(
        controls,
        text='Moderation effectiveness',
        command=lambda: _open_moderation_effectiveness_dialog(
            parent=root,
            conn=cast(sqlite3.Connection, state['conn']),
        ),
    ).grid(row=0, column=3, padx=(0, 8))
    ttk.Button(
        controls,
        text='Analysis charts',
        command=lambda: _open_analysis_charts_window(
            parent=root,
            conn=cast(sqlite3.Connection, state['conn']),
            human_only=_human_only_from_state(state),
            state=state,
        ),
    ).grid(row=0, column=4, padx=(0, 8))
    ttk.Button(
        controls,
        text='Categorical analysis',
        command=lambda: _open_categorical_analysis_dialog(
            parent=root,
            conn=cast(sqlite3.Connection, state['conn']),
            human_only=_human_only_from_state(state),
        ),
    ).grid(row=0, column=5)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    outer.columnconfigure(0, weight=1)
    outer.rowconfigure(1, weight=1)

    def on_close() -> None:
        if messagebox.askokcancel('Quit', 'Close the application?'):
            get_audit_logger().info('Application shutdown confirmed by user')
            _close_filter_results_window(state)
            _close_filter_pivot_window(state)
            _close_analysis_charts_window(state)
            state['conn'].close()
            root.destroy()

    root.protocol('WM_DELETE_WINDOW', on_close)
    root.mainloop()
