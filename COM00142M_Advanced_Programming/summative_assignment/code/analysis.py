"""Exploratory aggregations and matplotlib figures for the relational demo database."""

from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from matplotlib.figure import Figure

from database import sql_exclude_bot_users

if TYPE_CHECKING:
    from matplotlib.axes import Axes


def _posts_timebase_sql(*, human_only: bool) -> str:
    if not human_only:
        return 'SELECT post_id, timestamp FROM posts'
    pred = sql_exclude_bot_users(users_table_alias='u')
    return f'''
        SELECT p.post_id, p.timestamp
        FROM posts p
        INNER JOIN users u ON p.user_id = u.user_id
        WHERE {pred}
    '''


def fetch_posts_timestamps_df(
        conn: sqlite3.Connection,
        *,
        human_only: bool,
) -> pd.DataFrame:
    """Posts with raw ``timestamp`` text for time-based charts."""
    return pd.read_sql_query(_posts_timebase_sql(human_only=human_only), conn)


def normalize_sqlite_timestamp_series(raw: pd.Series) -> pd.Series:
    """
    Best-effort parse of stored post/interaction timestamps.

    Demo data mixes ``YYYY/MM/DD`` and ``YYYY-MM-DD`` (see import filters in
    ``ui``); normalise slashes before parsing.

    Pandas 2+ may infer a single datetime format from the first row; a leading
    ``... 00:00`` value can make later ``... HH:MM:SS`` rows parse as NaT without
    ``format='mixed'``.
    """
    s = raw.astype(str).str.strip()
    s = s.replace({'': pd.NA, 'nan': pd.NA, 'None': pd.NA})
    s = s.str.replace('/', '-', regex=False)
    return pd.to_datetime(s, format='mixed', errors='coerce', utc=False)


def _plot_daily_post_counts(ax: Axes, df_posts: pd.DataFrame) -> None:
    """Line plot: number of posts per calendar day."""
    dt = normalize_sqlite_timestamp_series(df_posts['timestamp'])
    valid = dt.dropna()
    if valid.empty:
        ax.text(
            0.5,
            0.5,
            'No parseable post timestamps',
            ha='center',
            va='center',
            transform=ax.transAxes,
        )
        ax.set_axis_off()
        return

    day = valid.dt.normalize()
    counts = day.value_counts().sort_index()
    x = counts.index.to_numpy()
    y = counts.to_numpy(dtype=float)

    ax.plot(x, y, color='tab:blue', linewidth=1.2, marker='o', markersize=3)
    ax.set_title('Posts per calendar day')
    ax.set_xlabel('Date')
    ax.set_ylabel('Post count')
    ax.tick_params(axis='x', rotation=35)
    ax.grid(True, alpha=0.25)

    # Light smoothing for readability on noisy daily counts (optional).
    if len(y) >= 7:
        window = min(7, len(y) // 2 * 2 + 1)
        if window >= 3:
            kernel = np.ones(window) / window
            smooth = np.convolve(y, kernel, mode='valid')
            start = (window - 1) // 2
            ax.plot(
                x[start: start + len(smooth)],
                smooth,
                color='tab:orange',
                linewidth=1.5,
                alpha=0.85,
                label=f'{window}-day moving average',
            )
            ax.legend(loc='upper right', fontsize=8)


def _interactions_timebase_sql(*, human_only: bool) -> str:
    if not human_only:
        return '''
            SELECT interaction_id, interaction_type, timestamp
            FROM interactions
        '''
    pred = sql_exclude_bot_users(users_table_alias='u')
    return f'''
        SELECT i.interaction_id, i.interaction_type, i.timestamp
        FROM interactions i
        INNER JOIN users u ON i.user_id = u.user_id
        WHERE {pred}
    '''


def fetch_interactions_timestamps_df(
        conn: sqlite3.Connection,
        *,
        human_only: bool,
) -> pd.DataFrame:
    """Interactions with types and timestamps for time-series / breakdown charts."""
    return pd.read_sql_query(
        _interactions_timebase_sql(human_only=human_only),
        conn,
    )


def _normalize_interaction_type_labels(raw: pd.Series) -> pd.Series:
    s = raw.astype(str).str.strip().str.lower()
    return s.replace({'': '(none)', 'nan': '(none)', 'none': '(none)'})


def _plot_daily_interactions(ax: Axes, df_interactions: pd.DataFrame) -> None:
    """Stacked area: interaction counts per calendar day by interaction_type (top types + other)."""
    if df_interactions.empty or 'timestamp' not in df_interactions.columns:
        ax.text(
            0.5,
            0.5,
            'No interaction rows',
            ha='center',
            va='center',
            transform=ax.transAxes,
        )
        ax.set_axis_off()
        return

    dt = normalize_sqlite_timestamp_series(df_interactions['timestamp'])
    itype_col = (
        df_interactions['interaction_type']
        if 'interaction_type' in df_interactions.columns
        else pd.Series(['(none)'] * len(df_interactions))
    )
    itype = _normalize_interaction_type_labels(itype_col)
    frame = pd.DataFrame({'day': dt.dt.normalize(), 'itype': itype})
    frame = frame.dropna(subset=['day'])
    if frame.empty:
        ax.text(
            0.5,
            0.5,
            'No parseable interaction timestamps',
            ha='center',
            va='center',
            transform=ax.transAxes,
        )
        ax.set_axis_off()
        return

    counts = frame.groupby(['day', 'itype']).size().unstack(fill_value=0)
    counts = counts.sort_index()
    col_totals = counts.sum(axis=0).sort_values(ascending=False)
    top_n = 6
    top_cols = [c for c in col_totals.head(top_n).index if str(c)]
    rest_cols = [c for c in counts.columns if c not in top_cols]

    plot_mat = counts[top_cols].copy()
    if rest_cols:
        plot_mat['(other types)'] = counts[rest_cols].sum(axis=1)

    days = plot_mat.index.to_numpy()
    series_list = [plot_mat[c].to_numpy(dtype=float) for c in plot_mat.columns]
    labels = [str(c)[:22] + ('…' if len(str(c)) > 22 else '') for c in plot_mat.columns]

    ax.stackplot(days, *series_list, labels=labels, alpha=0.88)
    ax.set_title('Interactions per calendar day by type (stacked)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Interaction count')
    ax.tick_params(axis='x', rotation=35)
    ax.grid(True, axis='y', alpha=0.22)
    ncol = 2 if len(labels) > 5 else 1
    ax.legend(loc='upper left', fontsize=7, ncol=ncol, framealpha=0.9)


def build_analysis_figure(
        conn: sqlite3.Connection,
        *,
        human_only: bool,
) -> Figure:
    """
    Two panels: daily post volume (with optional moving average) and stacked
    daily interaction counts by ``interaction_type``. Timestamps are parsed
    naively (no time-zone offsets).
    """
    fig = Figure(figsize=(10, 7.5), dpi=100)
    ax0 = fig.add_subplot(2, 1, 1)
    df_posts = fetch_posts_timestamps_df(conn, human_only=human_only)
    _plot_daily_post_counts(ax0, df_posts)

    ax1 = fig.add_subplot(2, 1, 2)
    df_int = fetch_interactions_timestamps_df(conn, human_only=human_only)
    _plot_daily_interactions(ax1, df_int)

    fig.subplots_adjust(hspace=0.28, left=0.08, right=0.98, top=0.95, bottom=0.1)
    return fig
