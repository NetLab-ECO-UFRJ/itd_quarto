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


def load_questions(questions_path: str = "data/questions_2025.yml", year: str = "2025") -> Dict[str, Any]:
    """
    Load the global questions configuration.

    Args:
        questions_path: Path to questions YAML file (default uses year-specific file)
        year: Year of the evaluation (used if questions_path is not provided)

    Returns:
        Dictionary with question code as keys and question data as values.
        Each question includes its parent category information.

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
    """
    full_path = PROJECT_ROOT / questions_path
    with open(full_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    questions_dict = {}
    for category in data['categories']:
        category_name = category['name']
        category_label = category['label']
        category_description = category['description']

        for question in category['questions']:
            code = question['code']
            questions_dict[code] = {
                'category': category_name,
                'category_label': category_label,
                'category_description': category_description,
                'code': code,
                'text': question['text'],
                'weight': question['weight'],
                'answers': question['answers']
            }

    return questions_dict


def load_categories(questions_path: str = "data/questions_2025.yml", year: str = "2025") -> List[Dict[str, str]]:
    """
    Load the list of all categories.

    Args:
        questions_path: Path to questions YAML file (default uses year-specific file)
        year: Year of the evaluation (used if questions_path is not provided)

    Returns:
        List of category dictionaries with name, label, and description

    Example:
        [
            {
                'name': 'consistency',
                'label': 'Consistency',
                'description': 'Evaluates how consistently...'
            }
        ]
    """
    full_path = PROJECT_ROOT / questions_path
    with open(full_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    categories = []
    for category in data['categories']:
        categories.append({
            'name': category['name'],
            'label': category['label'],
            'description': category['description']
        })

    return categories


def load_answers(platform: str, region: str, year: str = "2025",
                 scope: str = "regional", answers_dir: str = None) -> Dict[str, Any]:
    """
    Load platform-specific answers for a given region.

    Args:
        platform: Platform name (e.g., 'reddit', 'facebook')
        region: Region code (e.g., 'BR', 'UK', 'EU') or 'GLOBAL' for global scope
        year: Year of the evaluation (default: '2025')
        scope: Either 'regional' or 'global' (default: 'regional')
        answers_dir: Override directory containing answer files (optional)

    Returns:
        Dictionary containing metadata and categorized answers

    Example structure:
        {
            'metadata': {...},
            'consistency_answers': [...],
            'timeliness_answers': [...]
        }
    """
    if answers_dir is None:
        if scope == "global":
            # Global structure: data/2025/global/platform.yml
            filename = f"{platform.lower()}.yml"
            filepath = PROJECT_ROOT / "data" / year / "global" / filename
        else:
            # Regional structure: data/2025/regional/REGION/platform/answers/platform_region.yml
            filename = f"{platform.lower()}_{region.lower()}.yml"
            filepath = (PROJECT_ROOT / "data" / year / "regional" /
                       region.upper() / platform.lower() / "answers" / filename)
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
