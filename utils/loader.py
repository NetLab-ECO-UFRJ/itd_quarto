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


def load_questions(questions_path: str = "data/questions.yml") -> Dict[str, Any]:
    """
    Load the global questions configuration.

    Args:
        questions_path: Path to questions YAML file

    Returns:
        Dictionary with question code as keys and question data as values

    Example structure:
        {
            'UGC_01': {
                'category': 'UGC',
                'text': 'Does the platform...',
                'weight': 2.0,
                'answers': [...]
            }
        }
    """
    # Resolve path relative to project root
    full_path = PROJECT_ROOT / questions_path
    with open(full_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Convert list to dictionary indexed by question code for easier lookup
    questions_dict = {}
    for question in data['questions']:
        code = question['code']
        questions_dict[code] = question

    return questions_dict


def load_answers(platform: str, region: str,
                 answers_dir: str = "data/answers") -> Dict[str, Any]:
    """
    Load platform-specific answers for a given region.

    Args:
        platform: Platform name (e.g., 'reddit', 'facebook')
        region: Region code (e.g., 'BR', 'UK', 'EU')
        answers_dir: Directory containing answer files

    Returns:
        Dictionary containing metadata and categorized answers

    Example structure:
        {
            'metadata': {...},
            'ugc_answers': [...],
            'ads_answers': [...]
        }
    """
    # Build filename: platform_region.yml (lowercase)
    filename = f"{platform.lower()}_{region.lower()}.yml"
    # Resolve path relative to project root
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
