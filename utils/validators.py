"""
Validation utilities for ITD evaluation framework.

This module provides validation functions that can be used in:
- Quarto reports (lightweight, critical checks)
- Test notebooks (comprehensive validation)
- pytest tests (automated CI/CD)
"""

from typing import Dict, List, Any


class ValidationError(Exception):
    """Raised when data validation fails."""
    pass


def validate_platform_results(results: Dict[str, Any]) -> bool:
    """
    Validate computed results for a platform evaluation.

    This is a lightweight check suitable for embedding in reports.
    It verifies basic integrity without comprehensive testing.

    Args:
        results: Dictionary returned by calculate_platform_score()

    Returns:
        True if validation passes

    Raises:
        ValidationError: If any validation check fails

    Example:
        >>> results = calculate_platform_score('reddit', 'BR')
        >>> validate_platform_results(results)
        True
    """
    # Check required keys exist
    required_keys = [
        'metadata', 'total_score', 'total_max', 'total_percentage',
        'ugc_score', 'ugc_max', 'ugc_percentage',
        'ads_score', 'ads_max', 'ads_percentage',
        'ugc_details', 'ads_details'
    ]

    for key in required_keys:
        if key not in results:
            raise ValidationError(f"Missing required key: {key}")

    # Check score bounds
    if not 0 <= results['total_percentage'] <= 100:
        raise ValidationError(
            f"Total percentage out of bounds: {results['total_percentage']}"
        )

    if not 0 <= results['ugc_percentage'] <= 100:
        raise ValidationError(
            f"UGC percentage out of bounds: {results['ugc_percentage']}"
        )

    if not 0 <= results['ads_percentage'] <= 100:
        raise ValidationError(
            f"ADS percentage out of bounds: {results['ads_percentage']}"
        )

    # Check score consistency (actual = sum of categories)
    expected_total = results['ugc_score'] + results['ads_score']
    if abs(expected_total - results['total_score']) > 0.01:
        raise ValidationError(
            f"Score sum mismatch: {results['ugc_score']} + {results['ads_score']} "
            f"= {expected_total}, but total_score = {results['total_score']}"
        )

    # Check percentage calculation
    if results['total_max'] > 0:
        calculated_pct = (results['total_score'] / results['total_max']) * 100
        if abs(calculated_pct - results['total_percentage']) > 0.1:
            raise ValidationError(
                f"Percentage calculation error: {calculated_pct:.2f} != "
                f"{results['total_percentage']:.2f}"
            )

    return True


def validate_metadata(metadata: Dict[str, str]) -> bool:
    """
    Validate metadata structure.

    Args:
        metadata: Metadata dictionary from answer file

    Returns:
        True if valid

    Raises:
        ValidationError: If metadata is invalid
    """
    required_fields = ['platform', 'region_code', 'region_name', 'evaluation_date']

    for field in required_fields:
        if field not in metadata:
            raise ValidationError(f"Missing metadata field: {field}")
        if not isinstance(metadata[field], str) or not metadata[field].strip():
            raise ValidationError(f"Invalid metadata field: {field}")

    return True


def validate_answer_values(
    questions_dict: Dict[str, Any],
    answers_list: List[Dict[str, str]],
    category: str
) -> bool:
    """
    Validate that selected answer values exist in question definitions.

    Args:
        questions_dict: Dictionary of questions from questions.yml
        answers_list: List of answers (ugc_answers or ads_answers)
        category: Category name ('UGC' or 'ADS')

    Returns:
        True if all answers are valid

    Raises:
        ValidationError: If any answer is invalid
    """
    for answer_item in answers_list:
        question_code = answer_item.get('question_code')
        selected_value = answer_item.get('selected_answer')

        if not question_code:
            raise ValidationError(f"Answer missing question_code in {category}")

        if not selected_value:
            raise ValidationError(
                f"Answer missing selected_answer for {question_code}"
            )

        # Check question exists
        if question_code not in questions_dict:
            raise ValidationError(
                f"Question code '{question_code}' not found in questions.yml"
            )

        question = questions_dict[question_code]

        # Check category matches
        if question['category'] != category:
            raise ValidationError(
                f"Question {question_code} is in category {question['category']}, "
                f"but answer is in {category}"
            )

        # Check selected value is valid for this question
        valid_values = [a['value'] for a in question['answers']]
        if selected_value not in valid_values:
            raise ValidationError(
                f"Invalid answer value '{selected_value}' for question {question_code}. "
                f"Valid values: {valid_values}"
            )

    return True


def validate_question_coverage(
    questions_dict: Dict[str, Any],
    answers_data: Dict[str, Any]
) -> bool:
    """
    Validate that all questions have corresponding answers.

    Args:
        questions_dict: Dictionary of all questions
        answers_data: Answer data structure with ugc_answers and ads_answers

    Returns:
        True if all questions are covered

    Raises:
        ValidationError: If any questions are missing answers
    """
    # Get all answered question codes
    answered_codes = set()
    for ans in answers_data.get('ugc_answers', []):
        answered_codes.add(ans['question_code'])
    for ans in answers_data.get('ads_answers', []):
        answered_codes.add(ans['question_code'])

    # Check all questions have answers
    all_question_codes = set(questions_dict.keys())
    missing = all_question_codes - answered_codes

    if missing:
        raise ValidationError(
            f"Missing answers for questions: {sorted(missing)}"
        )

    # Check for extra answers
    extra = answered_codes - all_question_codes
    if extra:
        raise ValidationError(
            f"Answers provided for non-existent questions: {sorted(extra)}"
        )

    return True
