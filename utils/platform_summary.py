"""
Generate platform summary pages with score cards and category heatmaps.

Reads source mappings from appendix QMD frontmatter, calculates scores
per region/framework, and outputs HTML for Quarto rendering.
"""

from pathlib import Path
from typing import Dict, Optional

from .scoring import calculate_platform_score
from .quarto_helpers import get_platform_sources
from .summary_table import (
    get_score_class,
    get_platform_icon,
    normalize_platform_name,
    SCORE_BANDS,
)


def _find_project_root() -> Path:
    project_root = Path.cwd()
    while not (project_root / "utils").exists() and project_root != project_root.parent:
        project_root = project_root.parent
    return project_root


def get_score_band_label(score: float) -> str:
    if score == 0:
        return "Not Available"
    for lo, hi, _, label in SCORE_BANDS:
        if lo <= score < hi:
            return label
    if score >= 100:
        return "Strong"
    return "N/A"


def _get_score_band_color(score: float) -> str:
    if score == 0:
        return "#F3496B"
    for lo, hi, color, _ in SCORE_BANDS:
        if lo <= score < hi:
            return color
    if score >= 100:
        return "#308BF2"
    return "#F3496B"


def _compute_scores_for_sources(
    sources: Dict[str, str], question_type: str, year: str = "2025"
) -> Dict[str, dict]:
    results = {}
    for region, filepath in sources.items():
        try:
            result = calculate_platform_score(
                year=year, question_type=question_type, answers_file=filepath
            )
            results[region] = result
        except Exception as e:
            print(f"<!-- Warning: Failed to calculate {question_type} score for {region}: {e} -->")
    return results


def _generate_score_badge_html(score: float, is_not_applicable: bool = False) -> str:
    if is_not_applicable:
        return '<span style="font-size: 2.2rem; font-weight: 700; color: #999;">N/A</span>'
    color = _get_score_band_color(score)
    return f'<span style="font-size: 2.2rem; font-weight: 700; color: {color};">{score:.0f}</span>'


def _generate_overall_scores_html(
    ugc_scores: Dict[str, dict],
    ads_scores: Dict[str, dict],
    platform_slug: str,
) -> str:
    platform_display = normalize_platform_name(platform_slug)
    icon = get_platform_icon(platform_display, size=24)

    cards = []

    for framework_label, scores in [("User-Generated Content", ugc_scores), ("Advertising", ads_scores)]:
        if not scores:
            badge = _generate_score_badge_html(0, is_not_applicable=True)
            cards.append(
                f'<div style="flex: 1; min-width: 250px; border-radius: 8px; padding: 20px 24px; '
                f'background: #f8f9fa; border: 1px solid #e0e0e0; opacity: 0.5;">'
                f'<div style="margin: 0 0 12px 0; font-size: 1rem; color: #555; font-weight: 600;">{framework_label}</div>'
                f'<div style="margin-bottom: 4px;">{badge}</div>'
                f'<div style="font-size: 0.85rem; font-weight: 600; color: #999;">Not applicable</div>'
                f'</div>'
            )
            continue

        all_na = all(r.get("is_not_applicable", False) for r in scores.values())
        valid_scores = [
            r["total_score"]
            for r in scores.values()
            if not r.get("is_not_applicable", False)
        ]
        avg_score = round(sum(valid_scores) / len(valid_scores)) if valid_scores else 0

        if all_na:
            badge = _generate_score_badge_html(0, is_not_applicable=True)
            cards.append(
                f'<div style="flex: 1; min-width: 250px; border-radius: 8px; padding: 20px 24px; '
                f'background: #f8f9fa; border: 1px solid #e0e0e0; opacity: 0.5;">'
                f'<div style="margin: 0 0 12px 0; font-size: 1rem; color: #555; font-weight: 600;">{framework_label}</div>'
                f'<div style="margin-bottom: 4px;">{badge}</div>'
                f'<div style="font-size: 0.85rem; font-weight: 600; color: #999;">Not applicable</div>'
                f'</div>'
            )
            continue

        band_label = get_score_band_label(avg_score)
        band_color = _get_score_band_color(avg_score)
        badge = _generate_score_badge_html(avg_score)

        region_parts = []
        for region in ["BR", "EU", "UK"]:
            if region in scores:
                r = scores[region]
                if r.get("is_not_applicable", False):
                    region_parts.append(
                        f'<div style="text-align: center;">'
                        f'<span style="font-weight: 600; display: block; margin-bottom: 2px;">{region}</span>N/A</div>'
                    )
                else:
                    s = round(r["total_score"])
                    region_parts.append(
                        f'<div style="text-align: center;">'
                        f'<span style="font-weight: 600; display: block; margin-bottom: 2px;">{region}</span>{s}</div>'
                    )

        region_html = "".join(region_parts)
        cards.append(
            f'<div style="flex: 1; min-width: 250px; border-radius: 8px; padding: 20px 24px; '
            f'background: #f8f9fa; border: 1px solid #e0e0e0;">'
            f'<div style="margin: 0 0 12px 0; font-size: 1rem; color: #555; font-weight: 600;">{framework_label}</div>'
            f'<div style="margin-bottom: 4px;">{badge}</div>'
            f'<div style="font-size: 0.85rem; font-weight: 600; color: {band_color};">{band_label}</div>'
            f'<div style="display: flex; gap: 16px; font-size: 0.8rem; color: #666; '
            f'border-top: 1px solid #e0e0e0; padding-top: 10px; margin-top: 8px;">{region_html}</div>'
            f'</div>'
        )

    cards_html = "".join(cards)
    return f'\n<div style="display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap;">{cards_html}</div>\n'


def _generate_category_heatmap_html(
    scores_by_region: Dict[str, dict], question_type: str, heading: str
) -> str:
    regions = [r for r in ["BR", "EU", "UK"] if r in scores_by_region]
    if not regions:
        return ""

    ref_region = regions[0]
    ref_result = scores_by_region[ref_region]
    if ref_result.get("is_not_applicable", False):
        return ""

    categories = ref_result.get("categories", {})
    if not categories:
        return ""

    region_labels = {"BR": "Brazil", "EU": "EU", "UK": "UK"}

    html = f"\n### {heading} — Category Scores\n\n"
    html += """<style>
.category-heatmap {
    width: 100%;
    border-collapse: separate;
    border-spacing: 2px;
    margin: 10px 0 20px 0;
    font-family: system-ui, -apple-system, sans-serif;
}
.category-heatmap th, .category-heatmap td {
    padding: 8px 12px;
    text-align: center;
    font-weight: 500;
    border-radius: 3px;
}
.category-heatmap th {
    background-color: #f8f9fa;
    font-weight: 600;
}
.category-heatmap td.cat-name {
    text-align: left;
    font-weight: 600;
    background-color: #f8f9fa;
}
.score-ideal { background-color: #308BF2 !important; color: #143A66 !important; font-weight: 600 !important; }
.score-satisfactory { background-color: #43B5DF !important; color: #1F5366 !important; font-weight: 600 !important; }
.score-regular { background-color: #F3CE49 !important; color: #66571F !important; font-weight: 600 !important; }
.score-precarious { background-color: #F88C4A !important; color: #663A1F !important; font-weight: 600 !important; }
.score-irrelevant { background-color: #F64A9B !important; color: #661F40 !important; font-weight: 600 !important; }
.score-not-available { background-color: #F3496B !important; color: #661F2D !important; font-weight: 600 !important; }
.score-missing { background-color: #e0e0e0 !important; color: #666 !important; font-style: italic; }
</style>
"""

    header_cols = "".join(f"<th>{region_labels.get(r, r)}</th>" for r in regions)
    html += f'<table class="category-heatmap"><thead><tr><th>Category</th>{header_cols}</tr></thead><tbody>\n'

    for cat_name, cat_data in categories.items():
        label = cat_data["label"]
        html += f'<tr><td class="cat-name">{label}</td>'
        for region in regions:
            r_result = scores_by_region.get(region, {})
            r_cats = r_result.get("categories", {})
            r_cat = r_cats.get(cat_name)
            if r_cat is None:
                html += '<td class="score-missing">—</td>'
            else:
                pct = round(r_cat["percentage"])
                css = get_score_class(pct)
                html += f'<td class="{css}">{pct}%</td>'
        html += "</tr>\n"

    html += "</tbody></table>\n"
    return html


def generate_platform_summary(platform_slug: str, year: str = "2025"):
    """Generate full platform summary HTML and print it for Quarto `output: asis`."""
    project_root = _find_project_root()

    ugc_sources = get_platform_sources(platform_slug, "ugc", project_root)
    ads_sources = get_platform_sources(platform_slug, "ads", project_root)

    ugc_scores = _compute_scores_for_sources(ugc_sources, "ugc", year) if ugc_sources else {}
    ads_scores = _compute_scores_for_sources(ads_sources, "ads", year) if ads_sources else {}

    print(_generate_overall_scores_html(ugc_scores, ads_scores, platform_slug))

    if ugc_scores and not all(r.get("is_not_applicable", False) for r in ugc_scores.values()):
        print(_generate_category_heatmap_html(ugc_scores, "ugc", "User-Generated Content"))

    if ads_scores and not all(r.get("is_not_applicable", False) for r in ads_scores.values()):
        print(_generate_category_heatmap_html(ads_scores, "ads", "Advertising"))
