"""
Generate summary heatmap tables for transparency assessments.

Provides functions to create HTML heatmap tables showing scores across
all platforms and regions for both UGC and Ads assessments.
"""

from pathlib import Path
from typing import Dict, List, Tuple, Optional
from .scoring import calculate_platform_score


def get_score_class(score: float) -> str:
    """
    Determine CSS class based on score range.

    Args:
        score: Score value (0-100)

    Returns:
        CSS class name for color coding
    """
    if score >= 76:
        return "score-high"
    elif score >= 51:
        return "score-medium"
    elif score >= 26:
        return "score-low"
    else:
        return "score-zero"


def scan_assessments(project_root: Path, scope: str) -> Dict[str, Dict[str, Optional[float]]]:
    """
    Scan all assessment files and calculate scores.

    Args:
        project_root: Project root directory
        scope: Either 'ugc' or 'ads'

    Returns:
        Dictionary mapping platform names to region scores:
        {'Meta': {'BR': 45.2, 'EU': 38.7, 'UK': None}, ...}
        Global assessments fill all regions with the same value.
    """
    regional_dir = project_root / 'data' / '2025' / 'regional'
    global_dir = project_root / 'data' / '2025' / 'global'

    platforms = ['Bluesky', 'Discord', 'Kwai', 'Telegram', 'Meta', 'YouTube', 'X', 'TikTok', 'LinkedIn', 'Pinterest', 'Snapchat']
    regions = ['BR', 'EU', 'UK']

    results = {platform: {region: None for region in regions} for platform in platforms}

    # Normalize platform names
    platform_mapping = {
        'bluesky': 'Bluesky',
        'discord': 'Discord',
        'kwai': 'Kwai',
        'telegram': 'Telegram',
        'meta': 'Meta',
        'youtube': 'YouTube',
        'x': 'X',
        'tiktok': 'TikTok',
        'linkedin': 'LinkedIn',
        'pinterest': 'Pinterest',
        'snapchat': 'Snapchat'
    }

    # Scan global assessments - fill all regions with the same value
    if global_dir.exists():
        for platform_dir in global_dir.iterdir():
            if not platform_dir.is_dir():
                continue

            platform_name = platform_dir.name
            platform_display = platform_mapping.get(platform_name.lower(), platform_name.title())

            if platform_display not in platforms:
                continue

            assessment_file = platform_dir / f'{scope}.yml'

            if assessment_file.exists():
                try:
                    result = calculate_platform_score(
                        year='2025',
                        question_type=scope,
                        answers_file=str(assessment_file.relative_to(project_root))
                    )

                    score = result.get('total_score', 0.0)
                    score_rounded = round(score, 1)

                    # Fill all regions with the same global score
                    for region in regions:
                        results[platform_display][region] = score_rounded

                except Exception as e:
                    print(f"Warning: Failed to calculate score for {platform_display}/Global/{scope}: {e}")

    # Scan regional assessments - these override global values if they exist
    for region in ['BR', 'EU', 'UK']:
        region_dir = regional_dir / region
        if not region_dir.exists():
            continue

        for platform_dir in region_dir.iterdir():
            if not platform_dir.is_dir():
                continue

            platform_name = platform_dir.name
            platform_display = platform_mapping.get(platform_name.lower(), platform_name.title())

            if platform_display not in platforms:
                continue

            assessment_file = platform_dir / f'{scope}.yml'

            if assessment_file.exists():
                try:
                    result = calculate_platform_score(
                        year='2025',
                        question_type=scope,
                        answers_file=str(assessment_file.relative_to(project_root))
                    )

                    score = result.get('total_score', 0.0)
                    results[platform_display][region] = round(score, 1)

                except Exception as e:
                    print(f"Warning: Failed to calculate score for {platform_display}/{region}/{scope}: {e}")
                    results[platform_display][region] = None

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
.score-high { background-color: #084298 !important; color: white !important; }
.score-medium { background-color: #6c9bcf !important; color: white !important; }
.score-low { background-color: #cfe2ff !important; color: black !important; }
.score-zero { background-color: #f5f5f5 !important; color: black !important; }
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

    for platform, regions in scores.items():
        html += f'        <tr>\n'
        html += f'            <td class="platform-name">{platform}</td>\n'

        for region in ['BR', 'EU', 'UK']:
            score = regions.get(region)

            if score is None:
                html += f'            <td class="score-missing">—</td>\n'
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
        HTML string with color legend
    """
    return '''
<div style="margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-radius: 5px;">
    <h4 style="margin-top: 0;">Score Legend</h4>
    <table style="width: 100%; max-width: 500px;">
        <tr>
            <td style="padding: 8px; background-color: #084298; color: white; text-align: center; border: 1px solid #ddd;">High</td>
            <td style="padding: 8px;">76-100 points</td>
        </tr>
        <tr>
            <td style="padding: 8px; background-color: #6c9bcf; color: white; text-align: center; border: 1px solid #ddd;">Medium</td>
            <td style="padding: 8px;">51-75 points</td>
        </tr>
        <tr>
            <td style="padding: 8px; background-color: #cfe2ff; color: black; text-align: center; border: 1px solid #ddd;">Low</td>
            <td style="padding: 8px;">26-50 points</td>
        </tr>
        <tr>
            <td style="padding: 8px; background-color: #f5f5f5; color: black; text-align: center; border: 1px solid #ddd;">Zero</td>
            <td style="padding: 8px;">0-25 points</td>
        </tr>
        <tr>
            <td style="padding: 8px; background-color: #e0e0e0; color: #666; text-align: center; border: 1px solid #ddd; font-style: italic;">—</td>
            <td style="padding: 8px;">Not Yet Assessed</td>
        </tr>
    </table>
</div>
'''
