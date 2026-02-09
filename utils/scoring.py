"""
Scoring utilities for Social Media Evaluation project.

"""

from typing import Dict, List, Any, Tuple
from .loader import load_questions, load_answers, load_categories, get_answer_weight, get_answer_label


def get_question_family_prefix(question_type: str) -> str:
    """Return the code family prefix used in master question codes."""
    code_prefix_map = {
        'ugc': 'UGC',
        'ads': 'AD'
    }
    family_prefix = code_prefix_map.get(question_type)
    if not family_prefix:
        raise ValueError(f"Invalid question_type: {question_type}")

    return family_prefix


def get_expected_special_codes(questions_dict: Dict[str, Any], question_type: str) -> set:
    """Get expected special-criteria question codes from loaded master questions."""
    family_prefix = get_question_family_prefix(question_type)
    special_prefix = f"{family_prefix}_SC"
    return {q.get('code', '') for q in questions_dict.values() if q.get('code', '').startswith(special_prefix)}


def get_expected_other_count(questions_dict: Dict[str, Any], question_type: str) -> int:
    """
    Count "other criteria" questions from the loaded master question set.

    Other criteria are identified by OC question codes (e.g., UGC_OC2, AD_OC18).
    """
    family_prefix = get_question_family_prefix(question_type)
    prefix = f"{family_prefix}_OC"
    return sum(1 for q in questions_dict.values() if q.get('code', '').startswith(prefix))


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
        question_code = answer_item['code']
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


def calculate_methodology_score(
    answers_data: Dict[str, Any],
    questions_dict: Dict[str, Any],
    question_type: str
) -> Dict[str, Any]:
    """
    Calculate score using the methodology formulas.

    Args:
        answers_data: Loaded answers containing special-criteria and other categories
        questions_dict: Dictionary of all questions
        question_type: 'ugc' or 'ads'

    Returns:
        Dictionary with special_score, other_score, total_score (0-100 scale)
    """
    special_answers = answers_data.get('special-criteria_answers', [])

    get_question_family_prefix(question_type)  # Validate input early

    other_count = get_expected_other_count(questions_dict, question_type)
    expected_special_codes = get_expected_special_codes(questions_dict, question_type)

    if len(special_answers) != len(expected_special_codes):
        raise ValueError(
            f"Expected {len(expected_special_codes)} special criteria for {question_type.upper()}, "
            f"but got {len(special_answers)}"
        )

    special_weighted_sum = 0.0
    seen_special_codes = set()
    for answer_item in special_answers:
        question_code = answer_item['code']
        selected_value = answer_item['selected_answer']

        if question_code not in questions_dict:
            raise ValueError(f"Question code '{question_code}' not found")
        if question_code not in expected_special_codes:
            raise ValueError(
                f"Question code '{question_code}' is not a special criterion for {question_type.upper()}"
            )

        question = questions_dict[question_code]
        answer_weight = get_answer_weight(question, selected_value)

        special_weighted_sum += question['weight'] * answer_weight
        seen_special_codes.add(question_code)

    if seen_special_codes != expected_special_codes:
        missing_codes = sorted(expected_special_codes - seen_special_codes)
        raise ValueError(
            f"Missing special criteria answers for {question_type.upper()}: {', '.join(missing_codes)}"
        )

    special_score = 75 * special_weighted_sum

    other_sum = 0.0
    other_questions_count = 0
    applicable_count = 0

    for category_name, category_answers in answers_data.items():
        if category_name == 'metadata' or category_name == 'special-criteria_answers':
            continue

        if not category_name.endswith('_answers'):
            continue

        for answer_item in category_answers:
            question_code = answer_item['code']
            selected_value = answer_item['selected_answer']

            if question_code not in questions_dict:
                raise ValueError(f"Question code '{question_code}' not found")

            question = questions_dict[question_code]
            answer_weight = get_answer_weight(question, selected_value)

            other_sum += answer_weight
            other_questions_count += 1

            if selected_value != 'not_applicable':
                applicable_count += 1

    if other_questions_count != other_count:
        raise ValueError(
            f"Expected {other_count} other criteria for {question_type.upper()}, "
            f"but got {other_questions_count}"
        )

    denominator = applicable_count if applicable_count > 0 else other_count
    other_score = 25 * (other_sum / denominator)

    total_score = special_score + other_score

    all_not_applicable = True
    for answer_item in special_answers:
        if answer_item['selected_answer'] != 'not_applicable':
            all_not_applicable = False
            break

    if all_not_applicable:
        for category_name, category_answers in answers_data.items():
            if category_name == 'metadata' or category_name == 'special-criteria_answers':
                continue
            if not category_name.endswith('_answers'):
                continue
            for answer_item in category_answers:
                if answer_item['selected_answer'] != 'not_applicable':
                    all_not_applicable = False
                    break
            if not all_not_applicable:
                break

    return {
        'special_score': special_score,
        'other_score': other_score,
        'total_score': total_score,
        'special_max': 75.0,
        'other_max': 25.0,
        'total_max': 100.0,
        'is_not_applicable': all_not_applicable
    }


def calculate_platform_score(
    platform: str = None,
    region: str = None,
    year: str = "2025",
    scope: str = "regional",
    question_type: str = "all",
    answers_dir: str = None,
    answers_file: str = None
) -> Dict[str, Any]:
    """
    Calculate complete scores for a platform using the methodology.

    Args:
        platform: Platform name (e.g., 'reddit') - optional if answers_file is provided
        region: Region code (e.g., 'BR', 'EU', 'UK') or 'GLOBAL' for global scope - optional if answers_file is provided
        year: Year of the evaluation (default: '2025')
        scope: Either 'regional' or 'global' (default: 'regional')
        question_type: Type of questions to evaluate - 'ugc', 'ads', or 'all' (default: 'all')
        answers_dir: Override directory with answer files (optional, for legacy support)
        answers_file: Direct path to answer file (e.g., 'data/2025/global/kwai/ugc.yml')
                     If provided, platform/region/scope are ignored for path discovery

    Returns:
        Dictionary containing:
        - metadata: Platform and region info
        - categories: Dict with category scores, keyed by category name
          Each category contains: score, max, percentage, details
        - total_score: Score on 0-100 scale
        - total_max: Always 100.0
        - total_percentage: Overall percentage
        - special_score: Special criteria component (0-75)
        - other_score: Other criteria component (0-25)
    """
    questions_dict = load_questions(year=year, question_type=question_type)
    categories_list = load_categories(year=year, question_type=question_type)
    answers_data = load_answers(platform, region, year, scope, question_type, answers_dir, answers_file)

    category_results = {}

    for category_info in categories_list:
        category_name = category_info['name']
        answers_key = f"{category_name}_answers"

        # Handle both underscore and hyphen variants for category names
        # (e.g., both "special_criteria_answers" and "special-criteria_answers")
        if answers_key not in answers_data:
            answers_key_alt = answers_key.replace('_', '-', 1)  # Try hyphen variant
            if answers_key_alt not in answers_data:
                continue
            answers_key = answers_key_alt

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

    if question_type in ['ugc', 'ads']:
        methodology_scores = calculate_methodology_score(answers_data, questions_dict, question_type)

        return {
            'metadata': answers_data['metadata'],
            'categories': category_results,
            'total_score': methodology_scores['total_score'],
            'total_max': methodology_scores['total_max'],
            'total_percentage': methodology_scores['total_score'],
            'special_score': methodology_scores['special_score'],
            'other_score': methodology_scores['other_score'],
            'is_not_applicable': methodology_scores.get('is_not_applicable', False)
        }
    else:
        total_score = sum(cat['score'] for cat in category_results.values())
        total_max = sum(cat['max'] for cat in category_results.values())
        total_percentage = (total_score / total_max * 100) if total_max > 0 else 0

        return {
            'metadata': answers_data['metadata'],
            'categories': category_results,
            'total_score': total_score,
            'total_max': total_max,
            'total_percentage': total_percentage
        }
