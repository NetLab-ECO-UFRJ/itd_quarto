"""
Scoring utilities for Social Media Evaluation project.

This module calculates weighted scores based on questions and answers.
Score calculation: question_weight × answer_weight = question_score
"""

from typing import Dict, List, Any, Tuple
from .loader import load_questions, load_answers, load_categories, get_answer_weight, get_answer_label


def calculate_question_score(question: Dict[str, Any], selected_value: str) -> float:
    """
    Calculate the score for a single question.

    Score = question_weight × answer_weight

    Args:
        question: Question dictionary from questions.yml
        selected_value: Selected answer value (e.g., 'yes', 'no', 'partial')

    Returns:
        Calculated score (question weight × answer weight)
    """
    question_weight = question['weight']
    answer_weight = get_answer_weight(question, selected_value)

    return question_weight * answer_weight


def calculate_category_scores(
    questions_dict: Dict[str, Any],
    answers_list: List[Dict[str, str]],
    category: str
) -> Tuple[float, float, List[Dict[str, Any]]]:
    """
    Calculate aggregated scores for a category.

    Args:
        questions_dict: Dictionary of all questions indexed by code
        answers_list: List of answers for this category
        category: Category name (e.g., 'consistency', 'timeliness')

    Returns:
        Tuple of (actual_score, max_possible_score, detailed_results)
        - actual_score: Sum of all question scores in this category
        - max_possible_score: Maximum achievable score (all weights × 1.0)
        - detailed_results: List of dicts with per-question breakdown
    """
    actual_score = 0.0
    max_possible_score = 0.0
    detailed_results = []

    for answer_item in answers_list:
        question_code = answer_item['question_code']
        selected_value = answer_item['selected_answer']
        notes = answer_item.get('notes', '')

        if question_code not in questions_dict:
            raise ValueError(f"Question code '{question_code}' not found in questions.yml")

        question = questions_dict[question_code]

        if question['category'] != category:
            raise ValueError(
                f"Question {question_code} is in category {question['category']}, "
                f"but was placed in {category} answers"
            )

        question_score = calculate_question_score(question, selected_value)
        question_max = question['weight']

        actual_score += question_score
        max_possible_score += question_max

        detailed_results.append({
            'question_code': question_code,
            'question_text': question['text'],
            'question_weight': question['weight'],
            'selected_value': selected_value,
            'selected_label': get_answer_label(question, selected_value),
            'answer_weight': get_answer_weight(question, selected_value),
            'question_score': question_score,
            'question_max': question_max,
            'notes': notes,
            'category': question['category'],
            'category_label': question['category_label']
        })

    return actual_score, max_possible_score, detailed_results


def calculate_platform_score(
    platform: str,
    region: str,
    year: str = "2025",
    scope: str = "regional",
    questions_path: str = None,
    answers_dir: str = None
) -> Dict[str, Any]:
    """
    Calculate complete scores for a platform in a specific region.

    Args:
        platform: Platform name (e.g., 'reddit')
        region: Region code (e.g., 'BR', 'EU', 'UK') or 'GLOBAL' for global scope
        year: Year of the evaluation (default: '2025')
        scope: Either 'regional' or 'global' (default: 'regional')
        questions_path: Override path to questions YAML file (optional)
        answers_dir: Override directory with answer files (optional, for legacy support)

    Returns:
        Dictionary containing:
        - metadata: Platform and region info
        - categories: Dict with category scores, keyed by category name
          Each category contains: score, max, percentage, details
        - total_score: Combined actual score
        - total_max: Combined maximum score
        - total_percentage: Overall percentage
    """
    if questions_path is None:
        questions_path = f"data/questions_{year}.yml"

    questions_dict = load_questions(questions_path, year)
    categories_list = load_categories(questions_path, year)
    answers_data = load_answers(platform, region, year, scope, answers_dir)

    category_results = {}
    total_score = 0.0
    total_max = 0.0

    for category_info in categories_list:
        category_name = category_info['name']
        answers_key = f"{category_name}_answers"

        if answers_key not in answers_data:
            continue

        score, max_score, details = calculate_category_scores(
            questions_dict,
            answers_data[answers_key],
            category_name
        )

        percentage = (score / max_score * 100) if max_score > 0 else 0

        category_results[category_name] = {
            'label': category_info['label'],
            'description': category_info['description'],
            'score': score,
            'max': max_score,
            'percentage': percentage,
            'details': details
        }

        total_score += score
        total_max += max_score

    total_percentage = (total_score / total_max * 100) if total_max > 0 else 0

    return {
        'metadata': answers_data['metadata'],
        'categories': category_results,
        'total_score': total_score,
        'total_max': total_max,
        'total_percentage': total_percentage
    }
