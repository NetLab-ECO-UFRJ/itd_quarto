"""
Data loader utilities for Social Media Evaluation project.

This module provides functions to load and parse YAML configuration files
for questions and platform-specific answers.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any


# Get the project root directory (parent of utils/)
PROJECT_ROOT = Path(__file__).parent.parent


def load_questions(year: str = "2025", question_type: str = "all") -> Dict[str, Any]:
    """
    Load questions configuration from separate UGC and ADS files.
    Both files use section-based structure (no 'categories' wrapper).

    Args:
        year: Year of the evaluation (default: '2025')
        question_type: Type of questions to load - 'ugc', 'ads', or 'all' (default: 'all')

    Returns:
        Dictionary with question code as keys and question data as values.
        Each question includes its parent category (section) information.

    Example structure:
        {
            'UGC_01': {
                'category': 'consistency',
                'category_label': 'Consistency',
                'category_description': 'Evaluates how consistently...',
                'text': 'Does the platform...',
                'weight': 2.0,
                'answers': [...]
            }
        }

    Note: Questions use 'title' field in YAML, which is loaded into 'text' field here.
    """
    questions_dict = {}

    # Determine which files to load
    files_to_load = []
    if question_type in ["ugc", "all"]:
        files_to_load.append(f"data/{year}/questions_ugc_{year}.yml")
    if question_type in ["ads", "all"]:
        files_to_load.append(f"data/{year}/questions_ads_{year}.yml")

    if not files_to_load:
        raise ValueError(f"Invalid question_type: {question_type}. Must be 'ugc', 'ads', or 'all'")

    # Load each file
    for questions_path in files_to_load:
        full_path = PROJECT_ROOT / questions_path
        with open(full_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        # Section-based structure (consistency, accessibility, special-criteria, etc.)
        for section_name, questions_list in data.items():
            if isinstance(questions_list, list):
                # Convert section name to label (e.g., "special-criteria" -> "Special Criteria")
                category_label = section_name.replace('-', ' ').title()

                for question in questions_list:
                    code = question['code']
                    question_text = question.get('title', '')

                    questions_dict[code] = {
                        'category': section_name,
                        'category_label': category_label,
                        'category_description': question.get('description', ''),
                        'code': code,
                        'text': question_text,
                        'weight': question['weight'],
                        'answers': question['answers']
                    }

    return questions_dict


def load_categories(year: str = "2025", question_type: str = "all") -> List[Dict[str, str]]:
    """
    Load categories from separate UGC and ADS question files.

    Args:
        year: Year of the evaluation (default: '2025')
        question_type: Type of questions to load categories from - 'ugc', 'ads', or 'all' (default: 'all')

    Returns:
        List of category dictionaries with name, label, and description.
        Categories are deduplicated by name when loading from multiple files.

    Example:
        [
            {
                'name': 'consistency',
                'label': 'Consistency',
                'description': 'Evaluates how consistently...'
            }
        ]
    """
    categories_dict = {}

    # Determine which files to load
    files_to_load = []
    if question_type in ["ugc", "all"]:
        files_to_load.append(f"data/{year}/questions_ugc_{year}.yml")
    if question_type in ["ads", "all"]:
        files_to_load.append(f"data/{year}/questions_ads_{year}.yml")

    if not files_to_load:
        raise ValueError(f"Invalid question_type: {question_type}. Must be 'ugc', 'ads', or 'all'")

    # Load each file and merge categories (deduplicate by name)
    for questions_path in files_to_load:
        full_path = PROJECT_ROOT / questions_path
        with open(full_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        # Section-based structure: extract sections as categories
        for section_name, questions_list in data.items():
            if isinstance(questions_list, list) and questions_list:
                if section_name not in categories_dict:
                    # Convert section name to label (e.g., "special-criteria" -> "Special Criteria")
                    category_label = section_name.replace('-', ' ').title()
                    # Use first question's description as category description
                    category_desc = questions_list[0].get('description', '')

                    categories_dict[section_name] = {
                        'name': section_name,
                        'label': category_label,
                        'description': category_desc
                    }

    return list(categories_dict.values())


def load_answers(platform: str = None, region: str = None, year: str = "2025",
                 scope: str = "regional", question_type: str = None,
                 answers_dir: str = None, answers_file: str = None) -> Dict[str, Any]:
    """
    Load platform-specific answers for a given region.

    Args:
        platform: Platform name (e.g., 'reddit', 'facebook') - optional if answers_file is provided
        region: Region code (e.g., 'BR', 'UK', 'EU') or 'GLOBAL' for global scope - optional if answers_file is provided
        year: Year of the evaluation (default: '2025')
        scope: Either 'regional' or 'global' (default: 'regional')
        question_type: Type of answers to load - 'ugc' or 'ads' (optional, for split files)
        answers_dir: Override directory containing answer files (optional, legacy)
        answers_file: Direct path to answer file (e.g., 'data/2025/global/kwai/kwai_ugc.yml')
                     If provided, all path auto-discovery is skipped

    Returns:
        Dictionary containing metadata and categorized answers

    Example structure:
        {
            'metadata': {...},
            'consistency_answers': [...],
            'timeliness_answers': [...]
        }
    """
    if answers_file:
        # Use direct file path
        filepath = PROJECT_ROOT / answers_file
    elif answers_dir is None:
        if scope == "global":
            # Global structure: data/2025/global/platform/platform_ugc/ads.yml or platform_ugc/ads.yml
            if question_type:
                filename = f"{platform.lower()}_{question_type.lower()}.yml"
            else:
                filename = f"{platform.lower()}.yml"

            # Try platform subfolder first (e.g., kwai/kwai_ads.yml)
            filepath = PROJECT_ROOT / "data" / year / "global" / platform.lower() / filename
            if not filepath.exists():
                # Fall back to root global folder (e.g., platform_ads.yml)
                filepath = PROJECT_ROOT / "data" / year / "global" / filename
        else:
            # Regional structure: data/2025/regional/REGION/platform/platform_region_ugc/ads.yml
            if question_type:
                filename = f"{platform.lower()}_{region.lower()}_{question_type.lower()}.yml"
            else:
                filename = f"{platform.lower()}_{region.lower()}.yml"
            filepath = (PROJECT_ROOT / "data" / year / "regional" /
                       region.upper() / platform.lower() / filename)
    else:
        # Legacy path support
        filename = f"{platform.lower()}_{region.lower()}.yml"
        filepath = PROJECT_ROOT / answers_dir / filename

    if not filepath.exists():
        raise FileNotFoundError(f"Answer file not found: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        answers_data = yaml.safe_load(f)

    return answers_data


def get_answer_weight(question: Dict[str, Any], selected_value: str) -> float:
    """
    Get the weight for a specific answer value within a question.

    Args:
        question: Question dictionary containing answers list
        selected_value: The selected answer value (e.g., 'yes', 'no', 'partial')

    Returns:
        Weight of the selected answer (0.0 to 1.0)

    Raises:
        ValueError: If selected_value not found in question's answers
    """
    for answer in question['answers']:
        if answer['value'] == selected_value:
            return answer['weight']

    # If not found, raise error
    raise ValueError(
        f"Answer value '{selected_value}' not found in question '{question['code']}'"
    )


def get_answer_label(question: Dict[str, Any], selected_value: str) -> str:
    """
    Get the human-readable label for a specific answer value.

    Args:
        question: Question dictionary containing answers list
        selected_value: The selected answer value

    Returns:
        Label text for the answer
    """
    for answer in question['answers']:
        if answer['value'] == selected_value:
            return answer['label']

    return selected_value  # Fallback to value if label not found
