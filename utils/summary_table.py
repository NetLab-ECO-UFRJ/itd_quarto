"""
Generate summary heatmap tables and overview charts for transparency assessments.

Provides functions to create HTML heatmap tables and matplotlib dot plots
showing scores across all platforms and regions for both UGC and Ads assessments.
"""

from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
import yaml
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from .scoring import calculate_platform_score
from .quarto_helpers import parse_qmd_frontmatter


def get_score_class(score: float) -> str:
    """
    Determine CSS class based on score range.

    Transparency Scale:
    - Meaningful (81-100): Well-established, openly accessible data infrastructure enabling systematic collection
    - Limited (61-80): Functional access tools with notable limitations (paywalls, restricted scope, etc.)
    - Deficient (41-60): Partial transparency resources with significant gaps preventing reliable research
    - Minimal (21-40): Only minimal data access, most features absent or severely constrained
    - Negligible (1-20): Negligible transparency infrastructure, nearly all criteria unmet
    - Not Available (0): No data access mechanisms despite framework applicability

    Args:
        score: Score value (0-100)

    Returns:
        CSS class name for color coding
    """
    if score == 0:
        return "score-not-available"
    elif score >= 81:
        return "score-ideal"
    elif score >= 61:
        return "score-satisfactory"
    elif score >= 41:
        return "score-regular"
    elif score >= 21:
        return "score-precarious"
    else:
        return "score-irrelevant"


VLOP_PLATFORMS = {
    'facebook', 'instagram', 'linkedin', 'pinterest',
    'snapchat', 'tiktok', 'x', 'youtube',
}

PLATFORM_ICON_OVERRIDES = {
    'kwai': 'kuaishou',
    'linkedin': 'https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/linkedin.svg',
}

SIMPLEICONS_CDN = 'https://cdn.simpleicons.org'


def get_platform_icon(platform_display: str, size: int = 16) -> str:
    """Return an <img> tag for the platform's brand icon via Simple Icons CDN."""
    key = platform_display.lower().split('/')[0].strip()
    override = PLATFORM_ICON_OVERRIDES.get(key)
    if override and override.startswith('http'):
        url = override
    else:
        slug = override or key
        url = f'{SIMPLEICONS_CDN}/{slug}/000000'
    return (
        f'<img src="{url}" '
        f'alt="{platform_display}" width="{size}" height="{size}" '
        f'style="vertical-align: middle; margin-right: 6px;">'
    )


def normalize_platform_name(platform_name: str) -> str:
    """
    Normalize platform directory name to display name.

    Args:
        platform_name: Directory name (lowercase)

    Returns:
        Display name with proper capitalization
    """
    special_cases = {
        'x': 'X',
        'tiktok': 'TikTok',
        'youtube': 'YouTube',
        'linkedin': 'LinkedIn',
        'whatsapp': 'WhatsApp'
    }
    return special_cases.get(platform_name.lower(), platform_name.title())


def scan_assessments(project_root: Path, scope: str) -> Dict[str, Dict[str, Optional[Union[float, str]]]]:
    """
    Scan QMD files and calculate scores based on `sources` frontmatter.

    Reads sources.<scope> dict from each appendix QMD to get
    {region: filepath} mappings, then calculates scores.

    Args:
        project_root: Project root directory
        scope: Either 'ugc' or 'ads'

    Returns:
        Dictionary mapping platform names to region scores:
        {'Meta': {'BR': 45.2, 'EU': 38.7, 'UK': None}, ...}
    """
    appendices_dir = project_root / 'chapters' / 'appendices'
    all_regions = ['BR', 'EU', 'UK']
    results = {}

    if not appendices_dir.exists():
        return results

    score_cache: Dict[str, Optional[float]] = {}

    def calculate_score(filepath: str) -> Optional[float]:
        if filepath in score_cache:
            return score_cache[filepath]
        assessment_file = project_root / filepath
        if not assessment_file.exists():
            score_cache[filepath] = None
            return None
        try:
            result = calculate_platform_score(
                year='2025',
                question_type=scope,
                answers_file=filepath
            )
            val = round(result.get('total_score', 0.0))
        except Exception as e:
            print(f"Warning: Failed to calculate score for {filepath}: {e}")
            val = None
        score_cache[filepath] = val
        return val

    for qmd_file in sorted(appendices_dir.glob('*.qmd')):
        frontmatter = parse_qmd_frontmatter(qmd_file)
        platform_display = frontmatter.get('title') or normalize_platform_name(qmd_file.stem)

        sources = frontmatter.get('sources', {})
        mapping = sources.get(scope, {})
        if not mapping:
            continue

        results[platform_display] = {r: None for r in all_regions}
        for region, filepath in mapping.items():
            if region in all_regions:
                results[platform_display][region] = calculate_score(filepath)

    return results


SCORE_BANDS = [
    (0, 20, '#F64A9B', 'Negligible'),
    (20, 40, '#F88C4A', 'Minimal'),
    (40, 60, '#F3CE49', 'Deficient'),
    (60, 80, '#43B5DF', 'Limited'),
    (80, 100, '#308BF2', 'Meaningful'),
]

REGION_COLORS = {
    'BR': '#1b9e77',
    'EU': '#d95f02',
    'UK': '#7570b3',
}


def _find_project_root() -> Path:
    project_root = Path.cwd()
    while not (project_root / 'utils').exists() and project_root != project_root.parent:
        project_root = project_root.parent
    return project_root


def _compute_region_averages(scores: Dict) -> Dict[str, Optional[float]]:
    averages = {}
    for region in ['BR', 'EU', 'UK']:
        vals = [
            regions[region] for _, regions in scores.items()
            if isinstance(regions.get(region), (int, float))
        ]
        averages[region] = round(sum(vals) / len(vals)) if vals else None
    return averages


def generate_overview_dotplot():
    """Generate grouped horizontal bar chart showing average scores per region for UGC and ADS."""
    project_root = _find_project_root()

    ugc_scores = scan_assessments(project_root, 'ugc')
    ads_scores = scan_assessments(project_root, 'ads')

    ugc_avgs = _compute_region_averages(ugc_scores)
    ads_avgs = _compute_region_averages(ads_scores)

    scopes = [('Ads', ads_avgs), ('UGC', ugc_avgs)]
    regions = list(REGION_COLORS.keys())
    n_regions = len(regions)
    bar_height = 0.22
    group_gap = 0.15

    fig, ax = plt.subplots(figsize=(7, 2.6))

    for lo, hi, color, label in SCORE_BANDS:
        if label == 'N/A':
            continue
        ax.axvspan(lo, hi, color=color, alpha=0.18)
        ax.text((lo + hi) / 2, len(scopes) * (n_regions * bar_height + group_gap) - 0.05,
                label, ha='center', va='bottom', fontsize=7,
                color='#555', fontweight='600')

    for scope_idx, (scope_label, avgs) in enumerate(scopes):
        group_center = scope_idx * (n_regions * bar_height + group_gap)
        for i, region in enumerate(regions):
            y = group_center + i * bar_height
            val = avgs.get(region) or 0
            if val > 0:
                ax.barh(y, val, height=bar_height * 0.85, color=REGION_COLORS[region],
                        edgecolor='white', linewidth=0.5, zorder=3)
                ax.text(val + 1, y, f'{val:.0f}', va='center', ha='left',
                        fontsize=7.5, color='#333', fontweight='500')

    y_ticks = []
    y_labels = []
    for scope_idx, (scope_label, _) in enumerate(scopes):
        center = scope_idx * (n_regions * bar_height + group_gap) + (n_regions - 1) * bar_height / 2
        y_ticks.append(center)
        y_labels.append(scope_label)

    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels, fontsize=11, fontweight='600')
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    top = len(scopes) * (n_regions * bar_height + group_gap)
    ax.set_ylim(-0.25, top + 0.15)
    ax.set_xlabel('Average Score', fontsize=10)
    ax.tick_params(axis='x', labelsize=9)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    legend_handles = [
        mpatches.Patch(color=color, label=region)
        for region, color in REGION_COLORS.items()
    ]
    ax.legend(handles=legend_handles, loc='lower right', fontsize=8,
              framealpha=0.9, edgecolor='#ccc')

    plt.tight_layout()
    return fig


def _get_icon_url(platform_display: str) -> str:
    """Return the Simple Icons CDN URL for a platform."""
    key = platform_display.lower().split('/')[0].strip()
    override = PLATFORM_ICON_OVERRIDES.get(key)
    if override and override.startswith('http'):
        return override
    slug = override or key
    return f'{SIMPLEICONS_CDN}/{slug}/000000'


# Score units that map to one icon width at the fixed chart width (700px, icon=22px).
_ICON_OVERLAP_THRESHOLD = 4


def _assign_lanes(items: List[Tuple[str, float]]) -> List[List[Tuple[str, float]]]:
    """
    Assign (platform, score) pairs to horizontal lanes to prevent icon overlap.

    Sorts by score and places each icon in the first lane where no existing
    icon is within _ICON_OVERLAP_THRESHOLD score units.
    """
    lanes: List[List[Tuple[str, float]]] = []
    for platform, score in sorted(items, key=lambda x: x[1]):
        placed = False
        for lane in lanes:
            if all(abs(score - s) >= _ICON_OVERLAP_THRESHOLD for _, s in lane):
                lane.append((platform, score))
                placed = True
                break
        if not placed:
            lanes.append([(platform, score)])
    return lanes


def generate_icon_dotplot(scope: str) -> str:
    """
    Generate an HTML icon dot plot for UGC or ADS assessments.

    Each section represents a region (Brazil, EU, UK). Icons are stacked into
    multiple lanes per region to avoid overlap. The container has a fixed width
    so icons are not stretched across the full page.

    Args:
        scope: Either 'ugc' or 'ads'

    Returns:
        HTML string with the icon dot plot
    """
    project_root = _find_project_root()
    scores = scan_assessments(project_root, scope)

    region_labels = {
        'BR': 'Brazil',
        'EU': 'European Union',
        'UK': 'United Kingdom',
    }

    ICON_SIZE = 22
    LANE_H = ICON_SIZE + 6  # px per lane

    band_bg = ''.join(
        f'<div style="position:absolute;left:{lo}%;width:{hi - lo}%;'
        f'top:0;bottom:0;background:{color};opacity:0.18;pointer-events:none;"></div>'
        for lo, hi, color, _ in SCORE_BANDS
    )

    tick_marks = ''.join(
        f'<span style="position:absolute;left:{t}%;transform:translateX(-50%);'
        f'font-size:10px;color:#888;">{t}</span>'
        for t in [0, 20, 40, 60, 80, 100]
    )

    rows_html = ''
    for region, label in region_labels.items():
        items = [
            (platform, float(region_scores[region]))
            for platform, region_scores in scores.items()
            if isinstance(region_scores.get(region), (int, float))
        ]
        lanes = _assign_lanes(items)
        track_height = max(len(lanes) * LANE_H, LANE_H)

        icons_html = ''
        for lane_idx, lane in enumerate(lanes):
            top_px = lane_idx * LANE_H + (LANE_H - ICON_SIZE) // 2
            for platform, score in lane:
                url = _get_icon_url(platform)
                icons_html += (
                    f'<img src="{url}" alt="{platform}" '
                    f'width="{ICON_SIZE}" height="{ICON_SIZE}" '
                    f'title="{platform}: {score:.0f}" '
                    f'style="position:absolute;left:{score}%;top:{top_px}px;'
                    f'transform:translateX(-50%);display:block;">'
                )

        rows_html += (
            f'<div style="display:flex;align-items:center;margin:10px 0;">'
            f'<div style="width:130px;flex-shrink:0;font-weight:600;font-size:13px;'
            f'color:#333;align-self:center;">{label}</div>'
            f'<div style="position:relative;width:700px;height:{track_height}px;'
            f'background:#f8f9fa;border:1px solid #e0e0e0;border-radius:4px;'
            f'flex-shrink:0;">'
            f'{band_bg}{icons_html}'
            f'</div>'
            f'</div>'
        )

    return (
        f'<div style="margin:20px 0;font-family:system-ui,-apple-system,sans-serif;'
        f'overflow-x:auto;">'
        f'{rows_html}'
        f'<div style="margin-left:130px;position:relative;width:700px;'
        f'height:18px;margin-top:2px;">'
        f'{tick_marks}'
        f'</div>'
        f'</div>'
    )


def generate_overview_chart():
    """
    Generate a matplotlib figure showing platform transparency scores as a
    vertical beeswarm for UGC and ADS, faceted by region.

    Two subplots (UGC left, ADS right). X axis = regions. Y axis = score 0-100.
    Each platform is a coloured dot (score-band colour) with a 3-letter label.
    Beeswarm jitter prevents vertical overlap within each region column.

    Returns:
        matplotlib Figure
    """
    project_root = _find_project_root()
    ugc_scores = scan_assessments(project_root, 'ugc')
    ads_scores = scan_assessments(project_root, 'ads')

    REGIONS = ['BR', 'EU', 'UK']
    REGION_LABELS = ['Brazil', 'European\nUnion', 'United\nKingdom']

    SCORE_COLOR_MAP = [
        (80, '#308BF2'),
        (60, '#43B5DF'),
        (40, '#F3CE49'),
        (20, '#F88C4A'),
        (0,  '#F64A9B'),
    ]

    def score_color(s):
        for threshold, color in SCORE_COLOR_MAP:
            if s >= threshold:
                return color
        return SCORE_COLOR_MAP[-1][1]

    def beeswarm(items, y_radius=3.0, x_step=0.07):
        """Return list of (x_offset, score, platform) sorted by score."""
        sorted_items = sorted(items, key=lambda t: t[1])
        placed = []  # list of (x, y) already placed
        result = []
        candidates = [0]
        for n in range(1, 12):
            candidates += [n * x_step, -n * x_step]
        for platform, score in sorted_items:
            chosen = candidates[-1]
            for offset in candidates:
                collision = any(
                    ((offset - px) / x_step) ** 2 + ((score - py) / y_radius) ** 2 < 1.0
                    for px, py in placed
                )
                if not collision:
                    chosen = offset
                    break
            placed.append((chosen, score))
            result.append((chosen, score, platform))
        return result

    fig, axes = plt.subplots(1, 2, figsize=(11, 7), sharey=True)
    fig.subplots_adjust(wspace=0.06)

    for ax, (title, scope_scores) in zip(axes, [('UGC', ugc_scores), ('ADS', ads_scores)]):
        # Score band backgrounds
        for lo, hi, color, band_label in SCORE_BANDS:
            ax.axhspan(lo, hi, color=color, alpha=0.12, zorder=0)
            ax.text(-0.48, (lo + hi) / 2, band_label, fontsize=7,
                    color='#999', va='center', fontstyle='italic')

        for r_idx, region in enumerate(REGIONS):
            items = [
                (normalize_platform_name(platform.lower().split('/')[0].strip()),
                 float(region_scores[region]))
                for platform, region_scores in scope_scores.items()
                if isinstance(region_scores.get(region), (int, float))
            ]
            if not items:
                continue

            for x_off, score, platform in beeswarm(items):
                x = r_idx + x_off
                c = score_color(score)
                ax.scatter(x, score, color=c, s=520, zorder=4,
                           edgecolors='white', linewidths=0.8)
                abbr = platform[:3].upper()
                ax.text(x, score, abbr, fontsize=6, ha='center', va='center',
                        zorder=5, color='white', fontweight='bold')

        # Vertical separators
        for x in [0.5, 1.5]:
            ax.axvline(x, color='#e8e8e8', linewidth=1, zorder=1)

        ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
        ax.set_xticks(range(len(REGIONS)))
        ax.set_xticklabels(REGION_LABELS, fontsize=10)
        ax.set_xlim(-0.5, len(REGIONS) - 0.5)
        ax.set_ylim(-2, 102)
        ax.set_yticks([0, 20, 40, 60, 80, 100])
        ax.tick_params(axis='x', length=0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

    axes[0].set_ylabel('Score', fontsize=10)
    plt.tight_layout()
    return fig


def generate_vertical_dotplot(scope: str) -> str:
    """
    Generate a vertical HTML icon dot plot for UGC or ADS assessments.

    Regions are columns (Brazil, EU, UK). The score axis runs vertically
    (0 at bottom, 100 at top). Icons are placed at their score height and
    spread into horizontal sub-lanes when scores are too close to avoid overlap.

    Args:
        scope: Either 'ugc' or 'ads'

    Returns:
        HTML string with the vertical dot plot
    """
    project_root = _find_project_root()
    scores = scan_assessments(project_root, scope)

    ICON_SIZE = 20
    TRACK_H = 320
    LANE_W = ICON_SIZE + 4
    SCORE_THRESHOLD = 5  # score units before horizontal spreading

    region_meta = {
        'BR': ('🇧🇷', 'Brazil', REGION_COLORS['BR']),
        'EU': ('🇪🇺', 'European Union', REGION_COLORS['EU']),
        'UK': ('🇬🇧', 'United Kingdom', REGION_COLORS['UK']),
    }

    # Horizontal score band strips (top to bottom = high to low score)
    band_bg = ''.join(
        f'<div style="position:absolute;top:{100 - hi}%;height:{hi - lo}%;'
        f'left:0;right:0;background:{color};opacity:0.18;pointer-events:none;"></div>'
        for lo, hi, color, _ in SCORE_BANDS
    )

    # Y-axis tick labels
    y_axis = ''.join(
        f'<div style="position:absolute;top:{100 - t}%;right:6px;'
        f'transform:translateY(-50%);font-size:9px;color:#aaa;line-height:1;">{t}</div>'
        for t in [0, 20, 40, 60, 80, 100]
    )

    columns_html = ''
    for region, (flag, label, color) in region_meta.items():
        items = [
            (platform, float(region_scores[region]))
            for platform, region_scores in scores.items()
            if isinstance(region_scores.get(region), (int, float))
        ]

        # Assign to horizontal lanes based on vertical score proximity
        lanes = _assign_lanes(items)
        n_lanes = max(len(lanes), 1)
        track_w = n_lanes * LANE_W

        icons_html = ''
        for lane_idx, lane in enumerate(lanes):
            left_px = lane_idx * LANE_W + LANE_W // 2
            for platform, score in lane:
                url = _get_icon_url(platform)
                top_pct = 100 - score
                icons_html += (
                    f'<img src="{url}" alt="{platform}" '
                    f'width="{ICON_SIZE}" height="{ICON_SIZE}" '
                    f'title="{platform}: {score:.0f}" '
                    f'style="position:absolute;left:{left_px}px;top:{top_pct}%;'
                    f'transform:translate(-50%,-50%);display:block;">'
                )

        columns_html += (
            f'<div style="display:flex;flex-direction:column;align-items:center;">'
            f'<div style="font-weight:700;font-size:12px;color:{color};'
            f'margin-bottom:8px;text-align:center;">{flag}<br>{label}</div>'
            f'<div style="position:relative;width:{track_w}px;height:{TRACK_H}px;'
            f'background:#f8f9fa;border:1px solid #e0e0e0;border-radius:4px;">'
            f'{band_bg}{icons_html}'
            f'</div>'
            f'</div>'
        )

    return (
        f'<div style="margin:20px 0;font-family:system-ui,-apple-system,sans-serif;'
        f'display:flex;gap:0;align-items:flex-start;overflow-x:auto;">'
        f'<div style="position:relative;height:{TRACK_H}px;width:28px;'
        f'margin-top:52px;flex-shrink:0;">{y_axis}</div>'
        f'<div style="display:flex;gap:20px;">{columns_html}</div>'
        f'</div>'
    )


def generate_summary_heatmap(
    scope: str,
    include_average_row: bool = True,
    show_values: bool = True
) -> str:
    """
    Generate HTML heatmap table for UGC or Ads assessments.

    Args:
        scope: Either 'ugc' or 'ads'
        include_average_row: If True, adds per-region average row at the bottom
        show_values: If True, shows numeric values inside cells; if False, shows colors only

    Returns:
        HTML string with styled table
    """
    project_root = Path.cwd()

    # Search upward for project root
    while not (project_root / 'utils').exists() and project_root != project_root.parent:
        project_root = project_root.parent

    scores = scan_assessments(project_root, scope)

    html = '''
<style>
.heatmap-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 2px;
    margin: 20px 0;
    font-family: system-ui, -apple-system, sans-serif;
}
.heatmap-table th, .heatmap-table td {
    padding: 10px 12px;
    text-align: center;
    font-weight: 500;
    border-radius: 3px;
}
.heatmap-table th {
    background-color: #f8f9fa;
    font-weight: 600;
}
.heatmap-table td.platform-name {
    text-align: left;
    font-weight: 600;
    background-color: #f8f9fa;
}
.score-ideal { background-color: #308BF2 !important; color: #143A66 !important; font-weight: 600 !important; }
.score-satisfactory { background-color: #43B5DF !important; color: #1F5366 !important; font-weight: 600 !important; }
.score-regular { background-color: #F3CE49 !important; color: #66571F !important; font-weight: 600 !important; }
.score-precarious { background-color: #F88C4A !important; color: #663A1F !important; font-weight: 600 !important; }
.score-irrelevant { background-color: #F64A9B !important; color: #661F40 !important; font-weight: 600 !important; }
.score-not-available { background-color: transparent !important; color: #555 !important; font-weight: 600 !important; border: 1px dashed #aaa !important; }
.score-missing { background-color: #e0e0e0 !important; color: #666 !important; font-style: italic; }
.average-row td {
    background-color: #4a4a4a !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}
.vlop-badge {
    display: inline-block;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.04em;
    padding: 1px 4px;
    border-radius: 3px;
    background-color: #003399;
    color: #ffffff;
    vertical-align: middle;
    margin-left: 5px;
    line-height: 1.4;
}
</style>

<table class="heatmap-table">
    <thead>
        <tr>
            <th>Platform</th>
            <th>Brazil</th>
            <th>EU</th>
            <th>UK</th>
        </tr>
    </thead>
    <tbody>
'''

    # Calculate average score for each platform for sorting
    def calculate_average(regions_dict):
        numeric_scores = [
            score for score in regions_dict.values()
            if score is not None and score != 'N/A' and isinstance(score, (int, float))
        ]
        return sum(numeric_scores) / len(numeric_scores) if numeric_scores else -1

    # Sort platforms by average score (descending)
    sorted_platforms = sorted(scores.items(), key=lambda x: calculate_average(x[1]), reverse=True)

    region_averages = {}
    if include_average_row:
        for region in ['BR', 'EU', 'UK']:
            region_scores = [
                regions.get(region)
                for _, regions in sorted_platforms
                if isinstance(regions.get(region), (int, float))
            ]
            region_averages[region] = (
                round(sum(region_scores) / len(region_scores)) if region_scores else None
            )

    for platform, regions in sorted_platforms:
        html += f'        <tr>\n'
        icon = get_platform_icon(platform)
        vlop_key = platform.lower().split('/')[0].strip()
        vlop_badge = '<span class="vlop-badge" title="Very Large Online Platform (EU DSA)">VLOP</span>' if vlop_key in VLOP_PLATFORMS else ''
        html += f'            <td class="platform-name">{icon}{platform}{vlop_badge}</td>\n'

        for region in ['BR', 'EU', 'UK']:
            score = regions.get(region)

            if score is None:
                display_text = '—' if show_values else '&nbsp;'
                html += f'            <td class="score-missing">{display_text}</td>\n'
            elif score == 'N/A':
                display_text = 'N/A' if show_values else '&nbsp;'
                html += f'            <td class="score-missing">{display_text}</td>\n'
            else:
                css_class = get_score_class(score)
                display_text = f'{score:.0f}' if show_values else '&nbsp;'
                html += f'            <td class="{css_class}">{display_text}</td>\n'

        html += f'        </tr>\n'

    if include_average_row and show_values:
        html += '        <tr class="average-row">\n'
        html += '            <td class="platform-name"><strong>Average</strong></td>\n'
        for region in ['BR', 'EU', 'UK']:
            avg = region_averages.get(region)
            if avg is None:
                display_text = '—' if show_values else '&nbsp;'
                html += f'            <td>{display_text}</td>\n'
            else:
                display_text = f'<strong>{avg:.0f}</strong>' if show_values else '&nbsp;'
                html += f'            <td>{display_text}</td>\n'
        html += '        </tr>\n'

    html += '''    </tbody>
</table>
<p style="font-size: 12px; color: #555; margin-top: 4px;">
  <span class="vlop-badge">VLOP</span>
  &nbsp;Very Large Online Platform designated under the EU Digital Services Act (DSA), subject to enhanced transparency and accountability obligations.
</p>
'''

    return html
