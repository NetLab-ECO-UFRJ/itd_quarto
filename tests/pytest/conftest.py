"""
Pytest configuration and fixtures for ITD tests.

This file is automatically loaded by pytest and provides
shared fixtures and configuration for all tests.
"""

import pytest
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def project_root_path():
    """Provide path to project root."""
    return project_root


@pytest.fixture(scope="session")
def data_dir():
    """Provide path to data directory."""
    return project_root / "data"


@pytest.fixture(scope="session")
def test_data_dir():
    """Provide path to test data directory."""
    return project_root / "tests" / "test_data"


@pytest.fixture
def sample_question():
    """Provide a sample question for testing."""
    return {
        'code': 'TEST_01',
        'category': 'UGC',
        'text': 'Sample question for testing',
        'weight': 2.0,
        'answers': [
            {'value': 'yes', 'label': 'Yes', 'weight': 1.0},
            {'value': 'partial', 'label': 'Partial', 'weight': 0.5},
            {'value': 'no', 'label': 'No', 'weight': 0.0}
        ]
    }


@pytest.fixture
def sample_metadata():
    """Provide sample metadata for testing."""
    return {
        'platform': 'TestPlatform',
        'region_code': 'TS',
        'region_name': 'Test Region',
        'evaluation_date': '2025-01-15',
        'evaluator': 'Test Suite'
    }


# Configure pytest markers
def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
