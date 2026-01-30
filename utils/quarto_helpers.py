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
import markdown
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


def format_score(results: Dict[str, Any]) -> str:
    """
    Format a score result, returning "Not applicable" if all answers are N/A.

    Args:
        results: Results dictionary from calculate_platform_score

    Returns:
        Formatted score string: either "Not applicable" or "X / Y (Z%)"
    """
    if results.get('is_not_applicable', False):
        return "Not applicable"
    else:
        score = results['total_score']
        max_score = results['total_max']
        percentage = results['total_percentage']
        return f"{score:.0f} / {max_score:.0f} ({percentage:.0f}%)"


def generate_summary_table(results: Dict[str, Any]):
    """
    Generate separate summary tables for each category showing questions with answers and notes.

    Args:
        results: Results dictionary from calculate_platform_score
    """
    for category_name, category_data in results['categories'].items():
        print(f"\n### {category_data['label']}\n")
        print('```{=html}')
        print('<table style="width: 100% !important; max-width: 100% !important; table-layout: fixed; border-collapse: collapse; font-size: 0.9em;">')
        print('<colgroup>')
        print('<col style="width: 45% !important;">')
        print('<col style="width: 15% !important;">')
        print('<col style="width: 40% !important;">')
        print('</colgroup>')
        print('<thead>')
        print('<tr style="border-bottom: 2px solid #ddd;">')
        print('<th style="text-align: left; padding: 8px; width: 45% !important;">Question</th>')
        print('<th style="text-align: left; padding: 8px; width: 15% !important;">Answer</th>')
        print('<th style="text-align: left; padding: 8px; width: 40% !important;">Notes</th>')
        print('</tr>')
        print('</thead>')
        print('<tbody>')

        for item in category_data['details']:
            code = item['question_code']
            topic = f"<strong style='font-family: monospace; font-size: 0.9em;'>{code}:</strong> {item['question_text']}"
            answer = item['selected_label']
            notes_text = (item.get('notes') or '').replace('\n', ' ').replace('\r', ' ')
            notes = markdown.markdown(notes_text, extensions=['extra'])

            answer_icon = ""
            answer_lower = answer.lower()
            if answer_lower.startswith("yes") or answer_lower == "full" or answer_lower.startswith("free"):
                answer_icon = "✅ "
            elif answer_lower.startswith("partial"):
                answer_icon = "⚠️ "
            elif answer_lower == "not_applicable":
                answer_icon = "➖ "
            elif answer_lower == "no":
                answer_icon = "❌ "


            print('<tr style="border-bottom: 1px solid #eee;">')
            print(f'<td style="padding: 8px; vertical-align: top; word-wrap: break-word; word-break: break-word; overflow-wrap: break-word; width: 45% !important;">{topic}</td>')
            print(f'<td style="padding: 8px; vertical-align: top; width: 15% !important;">{answer_icon}{answer}</td>')
            print(f'<td style="padding: 8px; vertical-align: top; word-wrap: break-word; word-break: break-word; overflow-wrap: break-word; max-width: 0; width: 40% !important;">{notes}</td>')
            print('</tr>')

        print('</tbody>')
        print('</table>')
        print('```\n')


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
        print(f"**Score:** {category_data['score']:.0f} / {category_data['max']:.0f} ({category_data['percentage']:.0f}%)\n")
        print(f"\n{h2} Key Findings - {category_data['label']}\n")

        for item in category_data['details']:
            print(f"\n**{item['question_code']}: {item['question_text']}**\n")
            print(f"- **Answer:** {item['selected_label']}  ")
            print(f"- **Score:** {item['question_score']:.0f} / {item['question_max']:.0f} ({item['question_score']/item['question_max']*100:.0f}%)  ")
            if item['notes']:
                notes_cleaned = item['notes'].replace('\n', ' ').replace('\r', ' ')
                print(f"- **Notes:** {notes_cleaned}  ")
            print()
