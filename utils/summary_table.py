"""
Generate summary heatmap tables for transparency assessments.

Provides functions to create HTML heatmap tables showing scores across
all platforms and regions for both UGC and Ads assessments.
"""

from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
from .scoring import calculate_platform_score

GLOBAL_PLATFORMS = ['Bluesky', 'Discord', 'Kwai', 'Pinterest', 'Reddit', 'Telegram']


def get_score_class(score: float) -> str:
    """
    Determine CSS class based on score range.

    Transparency Scale:
    - Ideal (81-100): Efficient official solutions, APIs, well-documented
    - Satisfactory (61-80): Available without financial restrictions, some limitations
    - Regular (41-60): Some transparency measures, various limitations
    - Precarious (21-40): Significant barriers, monitoring unfeasible for most
    - Irrelevant or Zero (0-20): No transparency investment

    Args:
        score: Score value (0-100)

    Returns:
        CSS class name for color coding
    """
    if score >= 81:
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
        'linkedin': 'LinkedIn'
    }
    return special_cases.get(platform_name.lower(), platform_name.title())


def scan_assessments(project_root: Path, scope: str) -> Dict[str, Dict[str, Optional[Union[float, str]]]]:
    """
    Scan all assessment files and calculate scores.

    Global platforms (Bluesky, Discord, Kwai, Pinterest, Reddit, Telegram)
    always show the same score across all regions.

    Args:
        project_root: Project root directory
        scope: Either 'ugc' or 'ads'

    Returns:
        Dictionary mapping platform names to region scores:
        {'Meta': {'BR': 45.2, 'EU': 38.7, 'UK': None}, ...}
    """
    regional_dir = project_root / 'data' / '2025' / 'regional'
    global_dir = project_root / 'data' / '2025' / 'global'
    regions = ['BR', 'EU', 'UK']
    results = {}

    def calculate_score(assessment_file: Path) -> Optional[float]:
        """Helper to calculate score from assessment file."""
        try:
            result = calculate_platform_score(
                year='2025',
                question_type=scope,
                answers_file=str(assessment_file.relative_to(project_root))
            )
            return round(result.get('total_score', 0.0), 1)
        except Exception as e:
            print(f"Warning: Failed to calculate score for {assessment_file}: {e}")
            return None

    # Scan global assessments
    if global_dir.exists():
        for platform_dir in global_dir.iterdir():
            if not platform_dir.is_dir():
                continue

            platform_display = normalize_platform_name(platform_dir.name)

            if platform_display not in results:
                results[platform_display] = {region: None for region in regions}

            # Special case: Bluesky Ads is always N/A
            if platform_display == 'Bluesky' and scope == 'ads':
                for region in regions:
                    results[platform_display][region] = 'N/A'
                continue

            assessment_file = platform_dir / f'{scope}.yml'
            if assessment_file.exists():
                score = calculate_score(assessment_file)
                if score is not None:
                    for region in regions:
                        results[platform_display][region] = score

    # Scan regional assessments
    for region in regions:
        region_dir = regional_dir / region
        if not region_dir.exists():
            continue

        for platform_dir in region_dir.iterdir():
            if not platform_dir.is_dir():
                continue

            platform_display = normalize_platform_name(platform_dir.name)

            if platform_display not in results:
                results[platform_display] = {reg: None for reg in regions}

            assessment_file = platform_dir / f'{scope}.yml'
            if assessment_file.exists():
                score = calculate_score(assessment_file)
                if score is not None:
                    results[platform_display][region] = score

    # Enforce global platforms have same score across all regions
    for platform in GLOBAL_PLATFORMS:
        if platform in results:
            # Find first non-None score from any region
            global_score = next(
                (results[platform][r] for r in regions if results[platform][r] is not None),
                None
            )
            # Apply to all regions
            if global_score is not None:
                for region in regions:
                    results[platform][region] = global_score

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
    border-collapse: collapse;
    margin: 20px 0;
    font-family: system-ui, -apple-system, sans-serif;
}
.heatmap-table th, .heatmap-table td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: center;
    font-weight: 500;
}
.heatmap-table th {
    background-color: #f8f9fa;
    font-weight: 600;
}
.heatmap-table td.platform-name {
    text-align: left;
    font-weight: 600;
}
.score-ideal { background-color: #2d6a4f !important; color: white !important; }
.score-satisfactory { background-color: #95d5b2 !important; color: black !important; }
.score-regular { background-color: #ffd60a !important; color: black !important; }
.score-precarious { background-color: #f77f00 !important; color: white !important; }
.score-irrelevant { background-color: #d62828 !important; color: white !important; }
.score-missing { background-color: #e0e0e0 !important; color: #666 !important; font-style: italic; }
</style>

<table class="heatmap-table">
    <thead>
        <tr>
            <th>Platform</th>
            <th>Brazil (BR)</th>
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


def generate_legend() -> str:
    """
    Generate HTML legend for the heatmap color scheme.

    Returns:
        HTML string with color legend and transparency scale descriptions
    """
    return '''
<div style="margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-radius: 5px;">
    <h4 style="margin-top: 0;">Transparency Scale</h4>
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <td style="padding: 12px; background-color: #2d6a4f; color: white; font-weight: 600; border: 1px solid #ddd; width: 200px;">
                Transparency <em>ideal</em><br>(81 to 100 points)
            </td>
            <td style="padding: 12px; border: 1px solid #ddd;">
                Platforms with efficient official solutions for data collection, including APIs and a data collection interface, with well-documented examples.
            </td>
        </tr>
        <tr>
            <td style="padding: 12px; background-color: #95d5b2; color: black; font-weight: 600; border: 1px solid #ddd;">
                Transparency <em>satisfactory</em><br>(61 to 80 points)
            </td>
            <td style="padding: 12px; border: 1px solid #ddd;">
                Platforms that make data available with limitations on the volume of data that can be requested and/or with quality problems, especially consistency. 
            </td>
        </tr>
        <tr>
            <td style="padding: 12px; background-color: #ffd60a; color: black; font-weight: 600; border: 1px solid #ddd;">
                Transparency <em>regular</em><br>(41 to 60 points)
            </td>
            <td style="padding: 12px; border: 1px solid #ddd;">
                Platforms that present some measures of transparency and access to data, but with various limitations related to the type of content that can be accessed and the sample of the universe of public data that can be collected. 
            </td>
        </tr>
        <tr>
            <td style="padding: 12px; background-color: #f77f00; color: white; font-weight: 600; border: 1px solid #ddd;">
                Transparency <em>precarious</em><br>(21 to 40 points)
            </td>
            <td style="padding: 12px; border: 1px solid #ddd;">
                Platforms that impose significant technical, operational and/or financial barriers to their data access measures, making monitoring unfeasible for most researchers and interested parties. 
            </td>
        </tr>
        <tr>
            <td style="padding: 12px; background-color: #d62828; color: white; font-weight: 600; border: 1px solid #ddd;">
                Not available<br>(0 to 20 points)
            </td>
            <td style="padding: 12px; border: 1px solid #ddd;">
                Platforms with no transparency and data access measures. 
            </td>
        </tr>
        <tr>
            <td style="padding: 12px; background-color: #e0e0e0; color: #666; font-weight: 600; border: 1px solid #ddd; font-style: italic;">
                Not Applicable (N/A)
            </td>
            <td style="padding: 12px; border: 1px solid #ddd;">
                Platform has not been assessed yet or data is not available for this region.
            </td>
        </tr>
    </table>
</div>
'''
