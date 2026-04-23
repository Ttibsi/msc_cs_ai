"""
Three-way categorical breakdown: topic category × moderation level × post content_type.

Population: posts with a non-null topic and a join to topics; optional non-bot-only filter
to align with other human-focused analyses.
"""

from __future__ import annotations

import sqlite3
from collections import defaultdict

import numpy as np
from matplotlib.figure import Figure

from database import sql_exclude_bot_users

_MOD_ORDER = {'low': 0, 'medium': 1, 'high': 2}


def _mod_sort_key(level: str) -> int:
    return _MOD_ORDER.get(str(level).strip().lower(), 99)


INTERPRETATION_TEXT = (
    'This view counts posts along three categorical dimensions from the relational schema: '
    'the topic’s category and moderation_level (from topics) and the post’s content_type '
    '(from posts). Only posts linked to a topic are included. When “Human only” is enabled '
    'in the main window, bot-authored posts are excluded (same rule as other human behaviour '
    'analyses).\n\n'
    'The heatmap collapses content_type: each cell is the total post count for that '
    '(category, moderation_level) pair. The bar chart lists the largest individual '
    '(category, moderation_level, content_type) combinations.'
)


def query_three_way_distribution(
        conn: sqlite3.Connection,
        *,
        human_only: bool,
) -> list[tuple[str, str, str, int]]:
    """
    Return rows (category, moderation_level, content_type, count), sorted by count descending.
    Empty strings replace SQL NULLs in the three key columns.
    """
    if human_only:
        bot = sql_exclude_bot_users(users_table_alias='u')
        human_clause = f' AND ({bot})'
    else:
        human_clause = ''
    sql = f'''
        SELECT
            COALESCE(t.category, '') AS category,
            COALESCE(t.moderation_level, '') AS moderation_level,
            COALESCE(p.content_type, '') AS content_type,
            COUNT(*) AS cnt
        FROM posts p
        INNER JOIN users u ON p.user_id = u.user_id
        INNER JOIN topics t ON p.topic_id = t.topic_id
        WHERE p.topic_id IS NOT NULL{human_clause}
        GROUP BY t.category, t.moderation_level, p.content_type
        ORDER BY cnt DESC
    '''
    cur = conn.execute(sql)
    out: list[tuple[str, str, str, int]] = []
    for row in cur.fetchall():
        out.append((str(row[0]), str(row[1]), str(row[2]), int(row[3] or 0)))
    return out


def build_categorical_analysis_figure(
        rows: list[tuple[str, str, str, int]],
        *,
        top_n_bars: int = 15,
) -> Figure:
    """Heatmap: category × moderation_level (total posts). Barh: top triples by count."""
    fig = Figure(figsize=(11, 8), dpi=100)
    ax_h = fig.add_subplot(2, 1, 1)
    ax_b = fig.add_subplot(2, 1, 2)

    if not rows:
        ax_h.text(0.5, 0.5, 'No rows for categorical analysis', ha='center', va='center', transform=ax_h.transAxes)
        ax_h.set_axis_off()
        ax_b.set_axis_off()
        return fig

    marginal: dict[tuple[str, str], int] = defaultdict(int)
    for cat, mod, _ctype, c in rows:
        marginal[(cat, mod)] += c

    cats = sorted({k[0] for k in marginal})
    mods = sorted({k[1] for k in marginal}, key=_mod_sort_key)
    if not cats or not mods:
        ax_h.text(0.5, 0.5, 'Insufficient variety for heatmap', ha='center', va='center', transform=ax_h.transAxes)
        ax_h.set_axis_off()
    else:
        mat = np.zeros((len(cats), len(mods)), dtype=float)
        for i, c in enumerate(cats):
            for j, m in enumerate(mods):
                mat[i, j] = float(marginal.get((c, m), 0))
        im = ax_h.imshow(mat, aspect='auto', cmap='Greens')
        ax_h.set_yticks(range(len(cats)))
        ax_h.set_yticklabels(cats, fontsize=9)
        ax_h.set_xticks(range(len(mods)))
        ax_h.set_xticklabels(mods, rotation=15, ha='right')
        ax_h.set_xlabel('Moderation level')
        ax_h.set_ylabel('Topic category')
        ax_h.set_title('Post volume by category × moderation level (all content types combined)')
        fig.colorbar(im, ax=ax_h, fraction=0.035, pad=0.02, label='Post count')

    triples = sorted(rows, key=lambda r: r[3], reverse=True)[:top_n_bars]
    if not triples:
        ax_b.set_axis_off()
    else:
        labels = [
            f'{c[:14]}{"…" if len(c) > 14 else ""} | {m or "?"} | {ct or "(empty)"}'
            for c, m, ct, _ in triples
        ]
        vals = [t[3] for t in triples]
        y_pos = np.arange(len(labels))
        ax_b.barh(y_pos, vals, color='steelblue', edgecolor='navy', alpha=0.88)
        ax_b.set_yticks(y_pos)
        ax_b.set_yticklabels(labels, fontsize=8)
        ax_b.invert_yaxis()
        ax_b.set_xlabel('Post count')
        ax_b.set_title(
            f'Top {len(triples)} (category | moderation_level | content_type) cells',
        )
        ax_b.grid(True, axis='x', alpha=0.25)

    fig.subplots_adjust(left=0.22, right=0.96, top=0.93, bottom=0.08, hspace=0.38)
    return fig
