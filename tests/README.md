# Testing Infrastructure

This directory contains the testing infrastructure for the ITD (Internet Transparency Database) evaluation framework.

## Directory Structure

```
tests/
├── notebooks/              # Interactive test notebooks
│   └── test_data_validation.ipynb
├── pytest/                 # Automated pytest tests
│   ├── conftest.py        # Pytest configuration
│   └── test_scoring.py    # Scoring logic tests
├── test_data/             # Test fixtures and sample data
│   └── fixtures/
└── README.md              # This file
```

## Testing Approach

We use a **hybrid testing strategy** that combines:

1. **Jupyter Notebooks** - Interactive development and documentation
2. **Pytest** - Automated CI/CD testing
3. **Report Validation** - Lightweight checks embedded in reports

See `docs/testing_strategy.md` for detailed rationale.

## Running Tests

### Option 1: Interactive Notebooks

```bash
# Launch Jupyter
jupyter notebook tests/notebooks/

# Or use JupyterLab
jupyter lab tests/notebooks/
```

**When to use:**
- Exploring data quality
- Visual validation of results
- Developing new test cases
- Documentation and tutorials

### Option 2: Automated Pytest

```bash
# Run all tests
pytest tests/pytest/ -v

# Run specific test file
pytest tests/pytest/test_scoring.py -v

# Run with coverage report
pytest tests/pytest/ --cov=utils --cov-report=html

# Run only fast tests (exclude slow integration tests)
pytest tests/pytest/ -m "not slow"
```

**When to use:**
- CI/CD pipelines
- Pre-commit hooks
- Quick validation during development
- Regression testing

### Option 3: In Quarto Reports

Validation runs automatically when rendering reports:

```bash
quarto render reports/reddit_br.qmd
```

**What gets validated:**
- Data loads successfully
- Required fields present
- Score bounds (0-100%)
- Calculation consistency

## Test Categories

### 1. Data Validation Tests

**File:** `notebooks/test_data_validation.ipynb`

Validates:
- YAML structure and completeness
- Answer values match question options
- All questions have answers
- Metadata integrity

### 2. Scoring Logic Tests

**File:** `pytest/test_scoring.py`

Tests:
- Question score calculation (weight × answer_weight)
- Category aggregation
- Percentage calculations
- Edge cases and error handling

### 3. Integration Tests

**File:** `pytest/test_scoring.py` (TestPlatformScoring)

Tests:
- End-to-end report generation
- Cross-platform consistency
- File I/O operations

### 4. Validation Function Tests

**File:** `pytest/test_scoring.py` (TestValidators)

Tests:
- `validate_metadata()`
- `validate_answer_values()`
- `validate_question_coverage()`
- `validate_platform_results()`

## Adding New Tests

### Adding a Test Notebook

1. Create new `.ipynb` file in `tests/notebooks/`
2. Follow structure of existing notebooks:
   - Setup imports
   - Markdown explanations
   - Test cells with assertions
   - Visual outputs (plots, tables)
3. Document purpose and usage

### Adding a Pytest Test

1. Add test to `tests/pytest/test_scoring.py` or create new file
2. Follow naming convention: `test_*.py`
3. Use descriptive test names: `test_what_is_being_tested`
4. Add docstrings explaining purpose
5. Use fixtures from `conftest.py`

Example:
```python
def test_new_feature():
    """Test that new feature works correctly."""
    # Arrange
    input_data = ...

    # Act
    result = function_under_test(input_data)

    # Assert
    assert result == expected_value
```

## Test Data

### Using Real Data
Tests typically use actual data files:
- `data/questions.yml`
- `data/answers/reddit_br.yml`

### Using Test Fixtures
For unit tests, use fixtures from `conftest.py`:

```python
def test_with_fixture(sample_question):
    # sample_question provided by conftest.py
    result = process_question(sample_question)
    assert result is not None
```

### Creating Mock Data
For testing edge cases, create mock data:

```python
def test_edge_case():
    mock_question = {
        'code': 'MOCK_01',
        'weight': 0.0,  # Edge case: zero weight
        'answers': []
    }
    # Test behavior with unusual input
```

## Continuous Integration

### GitHub Actions Workflow

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Install dependencies
        run: uv sync

      - name: Run pytest
        run: uv run pytest tests/pytest/ -v --cov=utils

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "Running tests..."
uv run pytest tests/pytest/ -x
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

Make executable: `chmod +x .git/hooks/pre-commit`

## Best Practices

### Writing Good Tests

1. **Test one thing** - Each test should verify a single behavior
2. **Use descriptive names** - Test name should explain what's being tested
3. **Arrange-Act-Assert** - Structure tests clearly
4. **Test edge cases** - Zero values, empty lists, invalid inputs
5. **Document assumptions** - Explain why test exists

### Maintaining Tests

1. **Run tests regularly** - Before commits, during development
2. **Update tests with code** - When changing utils, update tests
3. **Fix failing tests immediately** - Don't let tests stay red
4. **Review test coverage** - Aim for >80% coverage on utils
5. **Refactor tests** - Keep tests clean and maintainable

### Test-Driven Development

1. Write test first (it fails)
2. Implement minimum code to pass test
3. Refactor while keeping tests passing
4. Repeat

## Troubleshooting

### Tests fail with ImportError

```bash
# Ensure project root is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or run with uv
uv run pytest tests/pytest/
```

### Notebook tests fail

```bash
# Install notebook dependencies
uv add --dev jupyter matplotlib

# Ensure kernel has access to utils
# (notebooks handle this in setup cell)
```

### Tests pass locally but fail in CI

- Check Python version consistency
- Verify all dependencies in pyproject.toml
- Check for hardcoded paths
- Review environment variables

## Resources

- **Pytest Documentation**: https://docs.pytest.org/
- **Testing Best Practices**: See `docs/testing_strategy.md`
- **Coverage Reports**: Run `pytest --cov` to generate

## Questions?

If you have questions about testing:
1. Review `docs/testing_strategy.md` for strategy rationale
2. Look at existing tests as examples
3. Check pytest documentation
4. Ask the team
