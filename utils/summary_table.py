"""
Generate summary heatmap tables for transparency assessments.

Provides functions to create HTML heatmap tables showing scores across
all platforms and regions for both UGC and Ads assessments.
"""

from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
import yaml
from .scoring import calculate_platform_score

REGION_CODE_MAP = {
    'GLOBAL': ['BR', 'EU', 'UK'],
    'BRAZIL': ['BR'],
    'EU': ['EU'],
    'UK': ['UK'],
    'BR': ['BR'],
}


def parse_qmd_frontmatter(qmd_path: Path) -> dict:
    """Extract YAML frontmatter from QMD file."""
    content = qmd_path.read_text()
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            return yaml.safe_load(content[3:end]) or {}
    return {}


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
    Scan QMD files and calculate scores based on frontmatter answer file paths.

    Reads ugc_answers_file/ads_answers_file and region_code from QMD frontmatter
    to determine which answer files to use for each platform/region combination.

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
    answer_file_key = f'{scope}_answers_file'

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

    def process_qmd(qmd_path: Path, platform_display: str):
        """Process a QMD file and update results based on frontmatter."""
        frontmatter = parse_qmd_frontmatter(qmd_path)

        answer_file_path = frontmatter.get(answer_file_key)
        region_code = frontmatter.get('region_code', 'GLOBAL')

        if not answer_file_path:
            return

        assessment_file = project_root / answer_file_path
        if not assessment_file.exists():
            return

        if platform_display not in results:
            results[platform_display] = {region: None for region in regions}

        score = calculate_score(assessment_file)
        if score is not None:
            target_regions = REGION_CODE_MAP.get(region_code, [])
            for region in target_regions:
                results[platform_display][region] = score

    # Scan global QMD files
    if global_dir.exists():
        for platform_dir in global_dir.iterdir():
            if not platform_dir.is_dir():
                continue

            platform_display = normalize_platform_name(platform_dir.name)

            # Skip Bluesky for Ads assessments (no advertising)
            if platform_display == 'Bluesky' and scope == 'ads':
                continue

            for qmd_file in platform_dir.glob('*.qmd'):
                process_qmd(qmd_file, platform_display)

    # Scan regional QMD files
    for region in regions:
        region_dir = regional_dir / region
        if not region_dir.exists():
            continue

        for platform_dir in region_dir.iterdir():
            if not platform_dir.is_dir():
                continue

            platform_display = normalize_platform_name(platform_dir.name)

            for qmd_file in platform_dir.glob('*.qmd'):
                process_qmd(qmd_file, platform_display)

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
.score-not-available { background-color: #e0e0e0 !important; color: #666 !important; }
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


