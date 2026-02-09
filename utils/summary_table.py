"""
Generate summary heatmap tables for transparency assessments.

Provides functions to create HTML heatmap tables showing scores across
all platforms and regions for both UGC and Ads assessments.
"""

from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
import yaml
from .scoring import calculate_platform_score
from .quarto_helpers import parse_qmd_frontmatter


def get_score_class(score: float) -> str:
    """
    Determine CSS class based on score range.

    Transparency Scale:
    - Strong (81-100): Efficient official solutions, APIs, well-documented
    - Restricted (61-80): Available with limitations
    - Deficient (41-60): Some transparency measures, various limitations
    - Precarious (21-40): Significant barriers, monitoring unfeasible for most
    - Irrelevant (1-20): Minimal or insufficient transparency measures
    - Not Available (0): No transparency despite framework applicability

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
            val = round(result.get('total_score', 0.0), 1)
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


def generate_summary_heatmap(scope: str) -> str:
    """
    Generate HTML heatmap table for UGC or Ads assessments.

    Args:
        scope: Either 'ugc' or 'ads'

    Returns:
        HTML string with styled table
    """
    project_root = Path.cwd()

    # Search upward for project root
    while not (project_root / 'utils').exists() and project_root != project_root.parent:
        project_root = project_root.parent

    scores = scan_assessments(project_root, scope)

    scope_display = 'UGC (User-Generated Content)' if scope == 'ugc' else 'Ads (Advertising)'

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
.score-not-available { background-color: #F3496B !important; color: #661F2D !important; font-weight: 600 !important; }
.score-missing { background-color: #e0e0e0 !important; color: #666 !important; font-style: italic; }
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

    for platform, regions in sorted_platforms:
        html += f'        <tr>\n'
        html += f'            <td class="platform-name">{platform}</td>\n'

        for region in ['BR', 'EU', 'UK']:
            score = regions.get(region)

            if score is None:
                html += f'            <td class="score-missing">—</td>\n'
            elif score == 'N/A':
                html += f'            <td class="score-missing">N/A</td>\n'
            else:
                css_class = get_score_class(score)
                html += f'            <td class="{css_class}">{score:.0f}</td>\n'

        html += f'        </tr>\n'

    html += '''    </tbody>
</table>
'''

    return html
