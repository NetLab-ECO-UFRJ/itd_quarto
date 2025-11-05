"""
Pytest tests for scoring calculations.

These tests are designed for automated CI/CD pipelines.
Run with: pytest tests/pytest/

For interactive testing and exploration, see tests/notebooks/
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.loader import load_questions, load_answers, get_answer_weight
from utils.scoring import (
    calculate_question_score,
    calculate_category_scores,
    calculate_platform_score
)
from utils.validators import (
    validate_platform_results,
    validate_metadata,
    validate_answer_values,
    validate_question_coverage,
    ValidationError
)


class TestQuestionScoring:
    """Test individual question score calculations."""

    def test_basic_question_score(self):
        """Test basic question score calculation."""
        question = {
            'code': 'TEST_01',
            'weight': 2.0,
            'answers': [
                {'value': 'yes', 'weight': 1.0},
                {'value': 'no', 'weight': 0.0}
            ]
        }

        score = calculate_question_score(question, 'yes')
        assert score == 2.0, "Score should be 2.0 * 1.0 = 2.0"

        score = calculate_question_score(question, 'no')
        assert score == 0.0, "Score should be 2.0 * 0.0 = 0.0"

    def test_partial_answer_score(self):
        """Test scoring with partial answer weight."""
        question = {
            'code': 'TEST_02',
            'weight': 1.5,
            'answers': [
                {'value': 'full', 'weight': 1.0},
                {'value': 'partial', 'weight': 0.6},
                {'value': 'none', 'weight': 0.0}
            ]
        }

        score = calculate_question_score(question, 'partial')
        expected = 1.5 * 0.6
        assert abs(score - expected) < 0.01, f"Score should be {expected}"

    def test_invalid_answer_raises_error(self):
        """Test that invalid answer value raises ValueError."""
        question = {
            'code': 'TEST_03',
            'weight': 1.0,
            'answers': [{'value': 'yes', 'weight': 1.0}]
        }

        with pytest.raises(ValueError):
            calculate_question_score(question, 'invalid')


class TestValidators:
    """Test validation functions."""

    def test_validate_metadata_success(self):
        """Test metadata validation with valid data."""
        metadata = {
            'platform': 'Reddit',
            'region_code': 'BR',
            'region_name': 'Brazil',
            'evaluation_date': '2025-01-15'
        }

        assert validate_metadata(metadata) is True

    def test_validate_metadata_missing_field(self):
        """Test metadata validation fails with missing field."""
        metadata = {
            'platform': 'Reddit',
            'region_code': 'BR'
            # Missing region_name and evaluation_date
        }

        with pytest.raises(ValidationError):
            validate_metadata(metadata)

    def test_validate_metadata_empty_field(self):
        """Test metadata validation fails with empty field."""
        metadata = {
            'platform': '',
            'region_code': 'BR',
            'region_name': 'Brazil',
            'evaluation_date': '2025-01-15'
        }

        with pytest.raises(ValidationError):
            validate_metadata(metadata)

    def test_validate_answer_values_success(self):
        """Test answer validation with valid data."""
        questions = {
            'UGC_01': {
                'category': 'UGC',
                'answers': [
                    {'value': 'yes', 'weight': 1.0},
                    {'value': 'no', 'weight': 0.0}
                ]
            }
        }

        answers = [
            {'question_code': 'UGC_01', 'selected_answer': 'yes'}
        ]

        assert validate_answer_values(questions, answers, 'UGC') is True

    def test_validate_answer_values_invalid_value(self):
        """Test answer validation fails with invalid answer value."""
        questions = {
            'UGC_01': {
                'category': 'UGC',
                'answers': [
                    {'value': 'yes', 'weight': 1.0},
                    {'value': 'no', 'weight': 0.0}
                ]
            }
        }

        answers = [
            {'question_code': 'UGC_01', 'selected_answer': 'maybe'}  # Invalid
        ]

        with pytest.raises(ValidationError):
            validate_answer_values(questions, answers, 'UGC')

    def test_validate_answer_values_wrong_category(self):
        """Test answer validation fails with wrong category."""
        questions = {
            'UGC_01': {
                'category': 'UGC',
                'answers': [{'value': 'yes', 'weight': 1.0}]
            }
        }

        answers = [
            {'question_code': 'UGC_01', 'selected_answer': 'yes'}
        ]

        with pytest.raises(ValidationError):
            validate_answer_values(questions, answers, 'ADS')  # Wrong category


class TestPlatformScoring:
    """Test complete platform scoring."""

    def test_reddit_br_scoring(self):
        """Test Reddit Brazil evaluation produces valid results."""
        results = calculate_platform_score('reddit', 'BR')

        # Check all required keys exist
        assert 'total_score' in results
        assert 'total_max' in results
        assert 'total_percentage' in results
        assert 'ugc_score' in results
        assert 'ads_score' in results

        # Validate results
        assert validate_platform_results(results) is True

    def test_score_bounds(self):
        """Test that scores are within valid bounds."""
        results = calculate_platform_score('reddit', 'BR')

        # Check percentage bounds
        assert 0 <= results['total_percentage'] <= 100
        assert 0 <= results['ugc_percentage'] <= 100
        assert 0 <= results['ads_percentage'] <= 100

        # Check score <= max
        assert results['total_score'] <= results['total_max']
        assert results['ugc_score'] <= results['ugc_max']
        assert results['ads_score'] <= results['ads_max']

    def test_score_consistency(self):
        """Test that total score equals sum of category scores."""
        results = calculate_platform_score('reddit', 'BR')

        expected_total = results['ugc_score'] + results['ads_score']
        assert abs(expected_total - results['total_score']) < 0.01

        expected_max = results['ugc_max'] + results['ads_max']
        assert abs(expected_max - results['total_max']) < 0.01

    def test_percentage_calculation(self):
        """Test that percentage is calculated correctly."""
        results = calculate_platform_score('reddit', 'BR')

        if results['total_max'] > 0:
            expected_pct = (results['total_score'] / results['total_max']) * 100
            assert abs(expected_pct - results['total_percentage']) < 0.1


class TestDataIntegrity:
    """Test data file integrity."""

    def test_questions_file_loads(self):
        """Test that questions.yml loads successfully."""
        questions = load_questions()
        assert len(questions) > 0, "Questions file should not be empty"

    def test_reddit_br_file_loads(self):
        """Test that Reddit Brazil answer file loads."""
        answers = load_answers('reddit', 'BR')
        assert 'metadata' in answers
        assert 'ugc_answers' in answers
        assert 'ads_answers' in answers

    def test_all_questions_have_answers(self):
        """Test that Reddit Brazil has answers for all questions."""
        questions = load_questions()
        answers = load_answers('reddit', 'BR')

        assert validate_question_coverage(questions, answers) is True

    def test_no_orphaned_answers(self):
        """Test that there are no answers for non-existent questions."""
        questions = load_questions()
        answers = load_answers('reddit', 'BR')

        # This will raise ValidationError if there are orphaned answers
        assert validate_question_coverage(questions, answers) is True


# Parametrized tests for future platforms
@pytest.mark.parametrize("platform,region", [
    ("reddit", "BR"),
    # Add more platforms as they become available:
    # ("facebook", "BR"),
    # ("instagram", "UK"),
])
def test_platform_evaluation(platform, region):
    """Test that platform evaluation completes successfully."""
    results = calculate_platform_score(platform, region)
    assert validate_platform_results(results) is True
    assert 0 <= results['total_percentage'] <= 100


if __name__ == '__main__':
    # Allow running directly for quick testing
    pytest.main([__file__, '-v'])
