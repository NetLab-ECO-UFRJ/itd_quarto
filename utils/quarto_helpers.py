"""
Quarto helper utilities for generating platform evaluation reports.

Provides functions to simplify Python code blocks in QMD files by:
- Auto-discovering project root and setting up imports
- Loading and calculating platform scores in one call
- Generating formatted markdown output for category scores
"""

import sys
from pathlib import Path
from typing import Dict, Any, Tuple
from .scoring import calculate_platform_score


def setup_quarto_environment() -> Path:
    """
    Auto-discover project root and setup sys.path for imports.

    Searches upward from current directory to find the project root
    (directory containing 'utils' folder) and adds it to sys.path.

    Returns:
        Path: Project root directory
    """
    project_root = Path.cwd()

    # Search upward for project root (contains 'utils' directory)
    while not (project_root / 'utils').exists() and project_root != project_root.parent:
        project_root = project_root.parent

    # Add to sys.path if not already there
    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)

    return project_root


def load_platform_results(
    ugc_file: str,
    ads_file: str,
    year: str = '2025'
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Load and calculate both UGC and ADS scores for a platform.

    Args:
        ugc_file: Path to UGC answers YAML file (e.g., 'data/2025/global/kwai/ugc.yml')
        ads_file: Path to ADS answers YAML file (e.g., 'data/2025/global/kwai/ads.yml')
        year: Evaluation year (default: '2025')

    Returns:
        Tuple of (results_ugc, results_ads) dictionaries containing:
        - metadata: Platform and region info
        - categories: Dict with category scores
        - total_score: Score on 0-100 scale
        - total_max: Always 100.0
        - total_percentage: Overall percentage
        - special_score: Special criteria component (0-75)
        - other_score: Other criteria component (0-25)
    """
    results_ugc = calculate_platform_score(
        year=year,
        question_type='ugc',
        answers_file=ugc_file
    )

    results_ads = calculate_platform_score(
        year=year,
        question_type='ads',
        answers_file=ads_file
    )

    return results_ugc, results_ads


def generate_category_scores(results: Dict[str, Any], heading_level: int = 3):
    """
    Generate markdown output for category scores with details.

    This function prints formatted markdown that Quarto will render,
    including category headers, scores, and detailed question breakdowns.

    Args:
        results: Results dictionary from calculate_platform_score
        heading_level: Base heading level for categories (default: 3 for ###)
                      Sub-headings (Key Findings) will be heading_level + 1

    Example output:
        ### Category Name
        *Category description*
        **Score:** 10.50 / 15.00 (70.0%)

        #### Key Findings - Category Name

        **Q1: Question text?**
        - **Answer:** Yes
        - **Score:** 2.00 / 2.00 (100.0%)
        - **Notes:** Additional context
    """
    h1 = '#' * heading_level
    h2 = '#' * (heading_level + 1)

    for category_name, category_data in results['categories'].items():
        print(f"\n{h1} {category_data['label']}\n")
        print(f"*{category_data['description']}*\n")
        print(f"**Score:** {category_data['score']:.2f} / {category_data['max']:.2f} ({category_data['percentage']:.1f}%)\n")
        print(f"\n{h2} Key Findings - {category_data['label']}\n")

        for item in category_data['details']:
            print(f"\n**{item['question_code']}: {item['question_text']}**\n")
            print(f"- **Answer:** {item['selected_label']}  ")
            print(f"- **Score:** {item['question_score']:.2f} / {item['question_max']:.2f} ({item['question_score']/item['question_max']*100:.1f}%)  ")
            if item['notes']:
                print(f"- **Notes:** {item['notes']}  ")
            print()
