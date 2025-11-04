"""
Scoring utilities for Social Media Evaluation project.

This module calculates weighted scores based on questions and answers.
Score calculation: question_weight × answer_weight = question_score
"""

from typing import Dict, List, Any, Tuple
from .loader import load_questions, load_answers, get_answer_weight, get_answer_label


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
    Calculate aggregated scores for a category (UGC or ADS).

    Args:
        questions_dict: Dictionary of all questions indexed by code
        answers_list: List of answers for this category
        category: Category name ('UGC' or 'ADS')

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

        # Get question definition
        if question_code not in questions_dict:
            raise ValueError(f"Question code '{question_code}' not found in questions.yml")

        question = questions_dict[question_code]

        # Verify category match
        if question['category'] != category:
            raise ValueError(
                f"Question {question_code} is in category {question['category']}, "
                f"but was placed in {category} answers"
            )

        # Calculate score for this question
        question_score = calculate_question_score(question, selected_value)
        question_max = question['weight']  # Max is weight × 1.0

        actual_score += question_score
        max_possible_score += question_max

        # Store detailed breakdown
        detailed_results.append({
            'question_code': question_code,
            'question_text': question['text'],
            'question_weight': question['weight'],
            'selected_value': selected_value,
            'selected_label': get_answer_label(question, selected_value),
            'answer_weight': get_answer_weight(question, selected_value),
            'question_score': question_score,
            'question_max': question_max,
            'notes': notes
        })

    return actual_score, max_possible_score, detailed_results


def calculate_platform_score(
    platform: str,
    country: str,
    questions_path: str = "data/questions.yml",
    answers_dir: str = "data/answers"
) -> Dict[str, Any]:
    """
    Calculate complete scores for a platform in a specific country.

    Args:
        platform: Platform name (e.g., 'reddit')
        country: Country code (e.g., 'BR')
        questions_path: Path to questions.yml
        answers_dir: Directory with answer files

    Returns:
        Dictionary containing:
        - metadata: Platform and country info
        - ugc_score: UGC category actual score
        - ugc_max: UGC category maximum possible score
        - ugc_percentage: UGC score as percentage
        - ugc_details: Per-question UGC breakdown
        - ads_score: ADS category actual score
        - ads_max: ADS category maximum possible score
        - ads_percentage: ADS score as percentage
        - ads_details: Per-question ADS breakdown
        - total_score: Combined actual score
        - total_max: Combined maximum score
        - total_percentage: Overall percentage
    """
    # Load data
    questions_dict = load_questions(questions_path)
    answers_data = load_answers(platform, country, answers_dir)

    # Calculate UGC scores
    ugc_score, ugc_max, ugc_details = calculate_category_scores(
        questions_dict,
        answers_data['ugc_answers'],
        'UGC'
    )

    # Calculate ADS scores
    ads_score, ads_max, ads_details = calculate_category_scores(
        questions_dict,
        answers_data['ads_answers'],
        'ADS'
    )

    # Calculate totals
    total_score = ugc_score + ads_score
    total_max = ugc_max + ads_max

    # Calculate percentages
    ugc_percentage = (ugc_score / ugc_max * 100) if ugc_max > 0 else 0
    ads_percentage = (ads_score / ads_max * 100) if ads_max > 0 else 0
    total_percentage = (total_score / total_max * 100) if total_max > 0 else 0

    return {
        'metadata': answers_data['metadata'],
        'ugc_score': ugc_score,
        'ugc_max': ugc_max,
        'ugc_percentage': ugc_percentage,
        'ugc_details': ugc_details,
        'ads_score': ads_score,
        'ads_max': ads_max,
        'ads_percentage': ads_percentage,
        'ads_details': ads_details,
        'total_score': total_score,
        'total_max': total_max,
        'total_percentage': total_percentage
    }
