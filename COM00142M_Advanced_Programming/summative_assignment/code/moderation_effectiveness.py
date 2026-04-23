"""
Moderation effectiveness: aggregates, topic-level metrics, patterns, and charts.

Definitions match the GUI copy: human post authors, non-null topic, human reporters,
``interaction_type`` = report (case-insensitive); placeholder reporter U9999 excluded
from counts with a running ignored tally.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass

import numpy as np
from matplotlib.figure import Figure

from database import sql_exclude_bot_users

PLACEHOLDER_REPORTER_USER_ID = 'U9999'

_MODERATION_ORDER = {'low': 0, 'medium': 1, 'high': 2}

DEFINITIONS_TEXT = (
    'Population: posts with a topic, human (non-bot) author, joined to topics.\n'
    'Reports: interactions where interaction_type = report (case-insensitive), '
    'reporter is human (non-bot), and reporter is not the placeholder user '
    f'{PLACEHOLDER_REPORTER_USER_ID!r}.\n'
    'Metrics: posts_in_group / reports_in_group / reports_per_post / '
    'pct_posts_with_reports are computed per (category, moderation_level). '
    'Topic charts use per-topic post and report counts on the same population.'
)


def _mod_rank(level: str | None) -> int:
    if level is None:
        return 1
    return _MODERATION_ORDER.get(str(level).strip().lower(), 1)


def _effectiveness_ctes(*, ua: str, ur: str, ph: str) -> str:
    return f'''
    WITH in_scope_posts AS (
        SELECT
            p.post_id,
            t.topic_id,
            t.topic_name,
            t.category,
            t.moderation_level
        FROM posts p
        INNER JOIN users ua ON p.user_id = ua.user_id
        INNER JOIN topics t ON p.topic_id = t.topic_id
        WHERE {ua} AND p.topic_id IS NOT NULL
    ),
    human_reports AS (
        SELECT i.post_id, COUNT(*) AS cnt
        FROM interactions i
        INNER JOIN users ur ON i.user_id = ur.user_id
        WHERE lower(trim(coalesce(i.interaction_type, ''))) = 'report'
        AND {ur}
        AND i.user_id != '{ph}'
        GROUP BY i.post_id
    )
    '''


@dataclass(frozen=True)
class ModerationEffectivenessResult:
    summary_colnames: list[str]
    summary_rows: list[tuple[object, ...]]
    ignored_placeholder_reports: int
    topic_rows: list[tuple[object, ...]]
    """topic_id, topic_name, category, moderation_level, post_count, report_count."""
    pattern_messages: list[str]
    summary_stats_lines: list[str]


def run_moderation_effectiveness_analysis(
        conn: sqlite3.Connection,
) -> ModerationEffectivenessResult:
    ua = sql_exclude_bot_users(users_table_alias='ua')
    ur = sql_exclude_bot_users(users_table_alias='ur')
    ph = PLACEHOLDER_REPORTER_USER_ID

    ignored_row = conn.execute(
        '''
        SELECT COUNT(*) FROM interactions
        WHERE lower(trim(coalesce(interaction_type, ''))) = 'report'
        AND user_id = ?
        ''',
        (ph,),
    ).fetchone()
    ignored_placeholder_reports = int(ignored_row[0]) if ignored_row else 0

    cte = _effectiveness_ctes(ua=ua, ur=ur, ph=ph)

    agg_sql = cte + '''
    SELECT
        isp.category,
        isp.moderation_level,
        COUNT(DISTINCT isp.post_id) AS posts_in_group,
        SUM(COALESCE(hr.cnt, 0)) AS reports_in_group,
        (SUM(COALESCE(hr.cnt, 0)) * 1.0 / COUNT(DISTINCT isp.post_id)) AS reports_per_post,
        (100.0 * SUM(CASE WHEN COALESCE(hr.cnt, 0) > 0 THEN 1 ELSE 0 END)
            / COUNT(DISTINCT isp.post_id)) AS pct_posts_with_reports
    FROM in_scope_posts isp
    LEFT JOIN human_reports hr ON hr.post_id = isp.post_id
    GROUP BY isp.category, isp.moderation_level
    ORDER BY isp.category, isp.moderation_level
    '''
    cur = conn.execute(agg_sql)
    summary_colnames = [d[0] for d in cur.description] if cur.description else []
    summary_rows = cur.fetchall()

    topic_sql = cte + '''
    SELECT
        isp.topic_id,
        isp.topic_name,
        isp.category,
        isp.moderation_level,
        COUNT(DISTINCT isp.post_id) AS post_count,
        SUM(COALESCE(hr.cnt, 0)) AS report_count
    FROM in_scope_posts isp
    LEFT JOIN human_reports hr ON hr.post_id = isp.post_id
    GROUP BY isp.topic_id, isp.topic_name, isp.category, isp.moderation_level
    ORDER BY isp.category, isp.moderation_level, isp.topic_id
    '''
    topic_rows = conn.execute(topic_sql).fetchall()

    stats_lines = _summary_stat_lines(
        summary_rows,
        summary_colnames,
        topic_rows,
        ignored_placeholder_reports,
    )
    patterns = _detect_patterns(summary_rows, summary_colnames, topic_rows)
    return ModerationEffectivenessResult(
        summary_colnames=summary_colnames,
        summary_rows=summary_rows,
        ignored_placeholder_reports=ignored_placeholder_reports,
        topic_rows=topic_rows,
        pattern_messages=patterns,
        summary_stats_lines=stats_lines,
    )


def _col_index(colnames: list[str], name: str) -> int:
    try:
        return colnames.index(name)
    except ValueError:
        return -1


def _summary_stat_lines(
        summary_rows: list[tuple[object, ...]],
        colnames: list[str],
        topic_rows: list[tuple[object, ...]],
        ignored_placeholder: int,
) -> list[str]:
    lines: list[str] = []
    pi = _col_index(colnames, 'posts_in_group')
    ri = _col_index(colnames, 'reports_in_group')
    rpp = _col_index(colnames, 'reports_per_post')
    if pi < 0 or ri < 0:
        return ['(Could not compute summary stats: unexpected column layout.)']

    total_posts = sum(int(r[pi] or 0) for r in summary_rows)
    total_reports = sum(int(r[ri] or 0) for r in summary_rows)
    lines.append(f'Total in-scope posts (aggregate buckets): {total_posts}')
    lines.append(f'Total human reports attributed to those posts: {total_reports}')
    if total_posts:
        lines.append(f'Overall reports per post (bucket totals): {total_reports / total_posts:.4f}')
    lines.append(
        f'Placeholder ({PLACEHOLDER_REPORTER_USER_ID!r}) report interactions excluded from numerators: '
        f'{ignored_placeholder}',
    )
    rates = [float(r[rpp]) for r in summary_rows if rpp >= 0 and r[rpp] is not None]
    if rates:
        lines.append(
            f'Across (category, moderation) buckets: median reports/post = {float(np.median(rates)):.4f}, '
            f'mean = {float(np.mean(rates)):.4f}',
        )
    n_topics = len(topic_rows)
    lines.append(f'Topics represented in topic-level view: {n_topics}')
    return lines


def _detect_patterns(
        summary_rows: list[tuple[object, ...]],
        colnames: list[str],
        topic_rows: list[tuple[object, ...]],
) -> list[str]:
    patterns: list[str] = []
    cat_i = _col_index(colnames, 'category')
    mod_i = _col_index(colnames, 'moderation_level')
    pi = _col_index(colnames, 'posts_in_group')
    ri = _col_index(colnames, 'reports_in_group')
    rpp_i = _col_index(colnames, 'reports_per_post')

    if cat_i < 0 or mod_i < 0 or pi < 0 or ri < 0 or rpp_i < 0:
        return ['Insufficient aggregate columns for pattern rules.']

    # --- Concentration: share of reports from top 3 topics ---
    t_reports = [(str(r[0]), str(r[1]), int(r[4] or 0), int(r[5] or 0)) for r in topic_rows]
    # topic_id, name, posts, reports
    by_rep = sorted(t_reports, key=lambda x: x[3], reverse=True)
    total_r = sum(x[3] for x in by_rep)
    if total_r > 0 and len(by_rep) >= 1:
        top3 = sum(x[3] for x in by_rep[:3])
        share = top3 / total_r
        if share >= 0.5:
            names = ', '.join(f'{x[0]} ({x[3]} reports)' for x in by_rep[:3])
            patterns.append(
                f'Concentration: top 3 topics account for {100.0 * share:.1f}% of reports ({names}). '
                f'Threshold: ≥50%.',
            )

    # --- Strictness vs rate within category (aggregate) ---
    by_cat: dict[str, list[tuple[str, float, int]]] = {}
    for row in summary_rows:
        cat = str(row[cat_i]) if row[cat_i] is not None else ''
        mod = str(row[mod_i]) if row[mod_i] is not None else ''
        rate = float(row[rpp_i] or 0.0)
        posts = int(row[pi] or 0)
        by_cat.setdefault(cat, []).append((mod, rate, posts))

    for cat, lst in sorted(by_cat.items()):
        low_rates = [r for m, r, p in lst if _mod_rank(m) == 0 and p > 0]
        high_rates = [r for m, r, p in lst if _mod_rank(m) == 2 and p > 0]
        if low_rates and high_rates:
            mean_low = float(np.mean(low_rates))
            mean_high = float(np.mean(high_rates))
            if mean_high > mean_low + 1e-6:
                patterns.append(
                    f'Mismatch (aggregate): in category {cat!r}, buckets labeled high moderation show '
                    f'higher mean reports/post ({mean_high:.4f}) than low ({mean_low:.4f}). '
                    f'Interpret: stricter label does not correspond to lower reporting in this slice.',
                )

    # --- Topic outliers within category (90th percentile of report rate) ---
    t_by_cat: dict[str, list[tuple[str, int, int, float]]] = {}
    for r in topic_rows:
        tid, _name, cat, _mod, posts, rep = (
            str(r[0]),
            str(r[1]),
            str(r[2]) if r[2] is not None else '',
            str(r[3]) if r[3] is not None else '',
            int(r[4] or 0),
            int(r[5] or 0),
        )
        rate = (rep / posts) if posts else 0.0
        if posts >= 3:
            t_by_cat.setdefault(cat, []).append((tid, posts, rep, rate))

    for cat, lst in sorted(t_by_cat.items()):
        if len(lst) < 3:
            continue
        rates_arr = np.array([x[3] for x in lst], dtype=float)
        p90 = float(np.percentile(rates_arr, 90))
        flagged = [x for x in lst if x[3] > p90 + 1e-9]
        for tid, posts, rep, rate in flagged[:5]:
            patterns.append(
                f'Outlier topic: {tid!r} in category {cat!r} has report rate {rate:.4f} '
                f'({rep} reports / {posts} posts), above ~90th percentile within category ({p90:.4f}). '
                f'Min posts per topic for rule: 3.',
            )
        if len(flagged) > 5:
            patterns.append(
                f'… and {len(flagged) - 5} more outlier topic(s) in category {cat!r}.',
            )

    if not patterns:
        patterns.append(
            'No rule-based patterns fired (concentration ≥50%, strictness mismatch, or topic outliers). '
            'This may reflect balanced data or thresholds.',
        )
    return patterns


def build_moderation_effectiveness_figure(
        result: ModerationEffectivenessResult,
) -> Figure:
    """Bar (rate by moderation level), heatmap (category × level), scatter (topics)."""
    fig = Figure(figsize=(11, 9), dpi=100)
    ax_bar = fig.add_subplot(2, 2, 1)
    ax_heat = fig.add_subplot(2, 2, 2)
    ax_scatter = fig.add_subplot(2, 1, 2)

    colnames = result.summary_colnames
    mod_i = _col_index(colnames, 'moderation_level')
    pi = _col_index(colnames, 'posts_in_group')
    ri = _col_index(colnames, 'reports_in_group')
    cat_i = _col_index(colnames, 'category')

    # --- Weighted bar: reports per post by moderation_level ---
    if mod_i >= 0 and pi >= 0 and ri >= 0 and result.summary_rows:
        level_posts: dict[str, int] = {}
        level_reports: dict[str, int] = {}
        for row in result.summary_rows:
            m = str(row[mod_i]) if row[mod_i] is not None else 'unknown'
            level_posts[m] = level_posts.get(m, 0) + int(row[pi] or 0)
            level_reports[m] = level_reports.get(m, 0) + int(row[ri] or 0)
        order = sorted(level_posts.keys(), key=lambda x: _mod_rank(x))
        xs = np.arange(len(order))
        rates = [
            level_reports[k] / level_posts[k] if level_posts[k] else 0.0
            for k in order
        ]
        ax_bar.bar(xs, rates, color='steelblue', edgecolor='navy', alpha=0.85)
        ax_bar.set_xticks(xs)
        ax_bar.set_xticklabels(order, rotation=20, ha='right')
        ax_bar.set_ylabel('Reports / post (weighted)')
        ax_bar.set_title('Report intensity by moderation level')
        ax_bar.grid(True, axis='y', alpha=0.3)
    else:
        ax_bar.text(0.5, 0.5, 'No aggregate data', ha='center', va='center', transform=ax_bar.transAxes)
        ax_bar.set_axis_off()

    # --- Heatmap category × moderation_level ---
    if cat_i >= 0 and mod_i >= 0 and result.summary_rows:
        cats = sorted({str(r[cat_i]) for r in result.summary_rows if r[cat_i] is not None})
        mods = sorted(
            {str(r[mod_i]) for r in result.summary_rows if r[mod_i] is not None},
            key=_mod_rank,
        )
        mat = np.full((len(cats), len(mods)), np.nan)
        for row in result.summary_rows:
            c = str(row[cat_i]) if row[cat_i] is not None else ''
            m = str(row[mod_i]) if row[mod_i] is not None else ''
            if c in cats and m in mods:
                i, j = cats.index(c), mods.index(m)
                mat[i, j] = float(row[_col_index(colnames, 'reports_per_post')] or 0.0)
        if np.isnan(mat).all():
            ax_heat.text(0.5, 0.5, 'No heatmap data', ha='center', va='center', transform=ax_heat.transAxes)
            ax_heat.set_axis_off()
        else:
            im = ax_heat.imshow(mat, aspect='auto', cmap='YlOrRd')
            ax_heat.set_yticks(range(len(cats)))
            ax_heat.set_yticklabels(cats, fontsize=8)
            ax_heat.set_xticks(range(len(mods)))
            ax_heat.set_xticklabels(mods, rotation=15, ha='right')
            ax_heat.set_title('Reports / post (category × moderation)')
            fig.colorbar(im, ax=ax_heat, fraction=0.046, pad=0.04)
    else:
        ax_heat.text(0.5, 0.5, 'No heatmap data', ha='center', va='center', transform=ax_heat.transAxes)
        ax_heat.set_axis_off()

    # --- Scatter: topics ---
    if result.topic_rows:
        posts = [int(r[4] or 0) for r in result.topic_rows]
        reps = [int(r[5] or 0) for r in result.topic_rows]
        mods_t = [str(r[3]) if r[3] is not None else '' for r in result.topic_rows]
        labels = sorted(set(mods_t), key=_mod_rank)
        cmap = {'low': 'tab:green', 'medium': 'tab:orange', 'high': 'tab:red'}
        for m in labels:
            xs = [posts[i] for i in range(len(posts)) if mods_t[i] == m]
            ys = [reps[i] for i in range(len(reps)) if mods_t[i] == m]
            ax_scatter.scatter(
                xs, ys,
                label=m,
                alpha=0.75,
                c=cmap.get(m.lower(), 'gray'),
                edgecolors='black',
                linewidths=0.3,
                s=45,
            )
        ax_scatter.set_xlabel('In-scope posts per topic')
        ax_scatter.set_ylabel('Human reports per topic')
        ax_scatter.set_title('Topics: post volume vs report volume (colour = moderation level)')
        ax_scatter.legend(title='mod level', fontsize=8)
        ax_scatter.grid(True, alpha=0.25)
    else:
        ax_scatter.text(0.5, 0.5, 'No topic-level rows', ha='center', va='center', transform=ax_scatter.transAxes)
        ax_scatter.set_axis_off()

    fig.subplots_adjust(left=0.08, right=0.96, top=0.94, bottom=0.08, hspace=0.35, wspace=0.35)
    return fig


def build_moderation_correlation_figure(
        result: ModerationEffectivenessResult,
) -> tuple[Figure, float | None]:
    """
    Correlation-focused view: ordinal moderation (low=0 … high=2) vs per-topic
    report rate (human reports ÷ in-scope posts), plus mean±spread of topic rates by label.

    Returns the figure and Pearson r when defined (≥2 topics, variation on both axes).
    """
    fig = Figure(figsize=(11, 5.2), dpi=100)
    ax_s = fig.add_subplot(1, 2, 1)
    ax_b = fig.add_subplot(1, 2, 2)

    topic_rows = result.topic_rows
    if not topic_rows:
        ax_s.text(0.5, 0.5, 'No topic-level rows', ha='center', va='center', transform=ax_s.transAxes)
        ax_s.set_axis_off()
        ax_b.set_axis_off()
        return fig, None

    x_rank: list[float] = []
    y_rate: list[float] = []
    post_n: list[int] = []
    mod_labels: list[str] = []
    for r in topic_rows:
        posts = int(r[4] or 0)
        reps = int(r[5] or 0)
        if posts <= 0:
            continue
        mod = str(r[3]) if r[3] is not None else ''
        x_rank.append(float(_mod_rank(mod)))
        y_rate.append(reps / posts)
        post_n.append(posts)
        mod_labels.append(mod.lower() or 'unknown')

    n_pts = len(x_rank)
    if n_pts < 2:
        ax_s.text(
            0.5,
            0.5,
            'Need at least two topics with posts to correlate',
            ha='center',
            va='center',
            transform=ax_s.transAxes,
        )
        ax_s.set_axis_off()
        ax_b.set_axis_off()
        return fig, None

    xa = np.array(x_rank, dtype=float)
    ya = np.array(y_rate, dtype=float)
    sizes = np.clip(25.0 + 4.0 * np.sqrt(np.array(post_n, dtype=float)), 28.0, 220.0)

    r_pearson: float | None = None
    if float(np.std(xa)) > 1e-9 and float(np.std(ya)) > 1e-9:
        r_mat = np.corrcoef(xa, ya)
        v = float(r_mat[0, 1])
        r_pearson = v if not np.isnan(v) else None

    rng = np.random.default_rng(42)
    x_j = xa + rng.uniform(-0.11, 0.11, size=xa.shape)
    color_map = {'low': '#2ca02c', 'medium': '#ff7f0e', 'high': '#d62728'}
    pt_colors = [color_map.get(m, '#7f7f7f') for m in mod_labels]
    ax_s.scatter(
        x_j,
        ya,
        s=sizes,
        c=pt_colors,
        alpha=0.75,
        edgecolors='black',
        linewidths=0.35,
    )
    coef = np.polyfit(xa, ya, 1)
    x_line = np.linspace(-0.15, 2.15, 60)
    ax_s.plot(x_line, coef[0] * x_line + coef[1], 'k--', linewidth=1.4, alpha=0.85, label='OLS fit')
    ax_s.set_xticks([0.0, 1.0, 2.0])
    ax_s.set_xticklabels(['low', 'medium', 'high'])
    ax_s.set_xlabel('Topic moderation level (ordinal for correlation)')
    ax_s.set_ylabel('Human reports per in-scope post (topic)')
    r_txt = f'Pearson r = {r_pearson:.3f}' if r_pearson is not None else 'Pearson r = n/a (no variation)'
    ax_s.set_title(f'Topic-level association\n{n_pts} topics. {r_txt}')
    ax_s.legend(loc='upper left', fontsize=8)
    ax_s.grid(True, alpha=0.28)
    ax_s.set_xlim(-0.35, 2.35)

    level_order = sorted(
        {str(r[3]) if r[3] is not None else '' for r in topic_rows},
        key=_mod_rank,
    )
    means: list[float] = []
    errs: list[float] = []
    for lev in level_order:
        rates = []
        for r in topic_rows:
            if str(r[3] if r[3] is not None else '') != lev:
                continue
            p = int(r[4] or 0)
            if p <= 0:
                continue
            rates.append(int(r[5] or 0) / p)
        if len(rates) == 0:
            means.append(0.0)
            errs.append(0.0)
        elif len(rates) == 1:
            means.append(float(rates[0]))
            errs.append(0.0)
        else:
            arr = np.array(rates, dtype=float)
            means.append(float(np.mean(arr)))
            errs.append(float(np.std(arr, ddof=1)))

    xb = np.arange(len(level_order))
    ax_b.bar(
        xb,
        means,
        yerr=errs,
        capsize=5,
        color='steelblue',
        edgecolor='navy',
        alpha=0.88,
    )
    ax_b.set_xticks(xb)
    ax_b.set_xticklabels(level_order, rotation=18, ha='right')
    ax_b.set_ylabel('Mean topic reports/post ± s.d. (within label)')
    ax_b.set_title('Report rate distribution by moderation label')
    ax_b.grid(True, axis='y', alpha=0.28)

    fig.subplots_adjust(left=0.07, right=0.98, top=0.88, bottom=0.14, wspace=0.28)
    return fig, r_pearson


def moderation_effectiveness_summary(
        conn: sqlite3.Connection,
) -> tuple[list[str], list[tuple[object, ...]], int]:
    """Backward-compatible aggregate query only."""
    r = run_moderation_effectiveness_analysis(conn)
    return r.summary_colnames, r.summary_rows, r.ignored_placeholder_reports
