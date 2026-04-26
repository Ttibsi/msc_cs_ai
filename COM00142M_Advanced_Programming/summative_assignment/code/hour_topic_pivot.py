"""
Hour-of-day × topic posting pivot (non-bot posts, parseable timestamps only).

When no topic filter is applied, posts with NULL ``topic_id`` are grouped under
``(no topic)``. When a specific topic is selected, only that topic is included
(implicitly excluding NULL-only rows for that filter).
"""
from __future__ import annotations

import sqlite3
from collections import defaultdict

import numpy as np
from matplotlib.figure import Figure

from database import sql_exclude_bot_users

# Sentinel for grouping NULL topic_id in buckets (all-topics mode only).
_NULL_TOPIC_KEY = '__NULL__'


def _hour_expr() -> str:
    return (
        "CAST(strftime('%H', replace(replace(p.timestamp, '/', '-'), 'T', ' ')) AS INTEGER)"
    )


def query_hour_topic_counts(
        conn: sqlite3.Connection,
        *,
        hour_filter: int | None,
        topic_id_filter: str | None,
) -> list[tuple[int, str | None, str | None, int]]:
    """
    Return rows: (hour_0_23, topic_id or None, topic_name or None, count).

    Excludes bot authors. Omits posts whose timestamp does not yield an hour
    (SQLite ``strftime`` NULL). Respects optional hour/topic filters the same way
    as filtered post listings.
    """
    params: list[object] = []
    clauses: list[str] = []
    if hour_filter is not None:
        clauses.append(f'({_hour_expr()} = ?)')
        params.append(hour_filter)
    if topic_id_filter:
        clauses.append('p.topic_id = ?')
        params.append(topic_id_filter)
    where_extra = ' AND '.join(clauses) if clauses else '1 = 1'
    bot_sql = sql_exclude_bot_users(users_table_alias='u')
    hod = _hour_expr()
    sql = f'''
        SELECT
            {hod} AS hod,
            p.topic_id,
            t.topic_name,
            COUNT(*) AS cnt
        FROM posts p
        INNER JOIN users u ON p.user_id = u.user_id
        LEFT JOIN topics t ON p.topic_id = t.topic_id
        WHERE ({where_extra}) AND ({bot_sql})
        AND {hod} IS NOT NULL
        GROUP BY hod, p.topic_id
        ORDER BY hod, p.topic_id
    '''
    cur = conn.execute(sql, params)
    out: list[tuple[int, str | None, str | None, int]] = []
    for row in cur.fetchall():
        h, tid, tname, c = row[0], row[1], row[2], int(row[3] or 0)
        if h is None:
            continue
        hi = int(h)
        if hi < 0 or hi > 23:
            continue
        out.append((hi, tid, tname, c))
    return out


def _bucket_key(topic_id: str | None) -> str:
    if topic_id is None or topic_id == '':
        return _NULL_TOPIC_KEY
    return str(topic_id)


def build_pivot_matrix(
        rows: list[tuple[int, str | None, str | None, int]],
) -> tuple[np.ndarray, list[str], list[str]]:
    """
    Build a (24, n_topics) float matrix, topic column order by descending volume.

    Returns (matrix, topic_column_keys, topic_header_labels).
    ``topic_column_keys`` match dict keys (_NULL_TOPIC_KEY or real id).
    ``topic_header_labels`` are display strings (IDs; NULL bucket as '(no topic)').
    """
    totals: dict[str, int] = defaultdict(int)
    cell: dict[tuple[int, str], int] = defaultdict(int)

    for hod, tid, _tname, cnt in rows:
        key = _bucket_key(tid)
        totals[key] += cnt
        cell[(hod, key)] += cnt

    if not totals:
        return np.zeros((24, 0)), [], []

    topic_keys = sorted(totals.keys(), key=lambda k: (-totals[k], k))
    n = len(topic_keys)
    mat = np.zeros((24, n), dtype=float)
    labels: list[str] = []
    for j, key in enumerate(topic_keys):
        for i in range(24):
            mat[i, j] = float(cell.get((i, key), 0))
        if key == _NULL_TOPIC_KEY:
            labels.append('(no topic)')
        else:
            labels.append(key)

    return mat, topic_keys, labels


def build_hour_topic_pivot_figure(
        matrix: np.ndarray,
        topic_labels: list[str],
        *,
        title: str = 'Post counts by hour × topic (non-bot, parseable time only)',
) -> Figure:
    """Heatmap: rows = hours 0–23, columns = topics (volume-sorted)."""
    fig = Figure(figsize=(max(8, 0.45 * max(1, matrix.shape[1])), 7), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    if matrix.size == 0:
        ax.text(0.5, 0.5, 'No data for pivot', ha='center', va='center', transform=ax.transAxes)
        ax.set_axis_off()
        return fig

    im = ax.imshow(matrix, aspect='auto', cmap='Blues', origin='upper')
    ax.set_yticks(range(24))
    ax.set_yticklabels([str(h) for h in range(24)], fontsize=7)
    ax.set_xticks(range(matrix.shape[1]))
    ax.set_xticklabels(topic_labels, rotation=45, ha='right', fontsize=8)
    ax.set_xlabel('Topic (id; volume-sorted)')
    ax.set_ylabel('Hour of day (0–23)')
    ax.set_title(title)
    fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02, label='Post count')
    fig.subplots_adjust(left=0.07, right=0.98, bottom=0.18, top=0.92)
    return fig
