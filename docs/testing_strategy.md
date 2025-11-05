# Technical Assessment: Integrating Computational Tests

## Executive Summary

This document evaluates approaches for integrating computational tests into the ITD (Internet Transparency Database) evaluation framework. We compare **standalone Jupyter notebooks** vs. **embedded Quarto chunks** and provide recommendations based on use case, maintainability, and reproducibility requirements.

## Current System Analysis

### Architecture Overview
- **Data Layer**: YAML files (`questions.yml`, `answers/*.yml`)
- **Logic Layer**: Python utilities (`loader.py`, `scoring.py`)
- **Presentation Layer**: Quarto reports (`.qmd` files)

### Current Testing Gap
The system currently has:
- ✅ Inline computation in reports (scoring calculations)
- ❌ No validation tests for data integrity
- ❌ No unit tests for scoring logic
- ❌ No integration tests for report generation
- ❌ No documentation of expected behaviors

## Types of Tests Needed

### 1. Data Validation Tests
**Purpose**: Ensure YAML files are well-formed and consistent

- Schema validation (required fields present)
- Answer values match question options
- All questions have corresponding answers
- Metadata completeness
- Cross-reference integrity

**Example**:
```python
# Test that selected_answer exists in question's answer list
def test_answer_validity():
    questions = load_questions()
    answers = load_answers('reddit', 'BR')
    for ans in answers['ugc_answers']:
        question = questions[ans['question_code']]
        valid_values = [a['value'] for a in question['answers']]
        assert ans['selected_answer'] in valid_values
```

### 2. Scoring Logic Tests
**Purpose**: Verify mathematical correctness

- Question score calculation (weight × answer_weight)
- Category aggregation (sum of question scores)
- Percentage calculations
- Edge cases (zero weights, missing data)

**Example**:
```python
# Test scoring formula
def test_question_score_calculation():
    question = {'weight': 2.0, 'answers': [{'value': 'yes', 'weight': 0.5}]}
    score = calculate_question_score(question, 'yes')
    assert score == 1.0  # 2.0 * 0.5
```

### 3. Consistency Tests
**Purpose**: Ensure data completeness across evaluations

- All regions have answers for all questions
- No orphaned question codes
- Evaluation dates are valid
- Score ranges are within bounds (0-100%)

### 4. Integration Tests
**Purpose**: End-to-end workflow validation

- Full report generation without errors
- Output files created successfully
- References resolved correctly
- Tables render properly

### 5. Regression Tests
**Purpose**: Detect unintended changes

- Scores remain stable when data unchanged
- Output format consistency
- API compatibility

## Approach Comparison

### Option A: Standalone Jupyter Notebooks

**Structure**:
```
tests/
├── notebooks/
│   ├── 01_data_validation.ipynb
│   ├── 02_scoring_tests.ipynb
│   ├── 03_consistency_checks.ipynb
│   └── 04_integration_tests.ipynb
└── test_data/
    ├── sample_questions.yml
    └── sample_answers.yml
```

#### Advantages ✅

1. **Separation of Concerns**
   - Tests are isolated from reports
   - Reports remain focused on presentation
   - Clear distinction between validation and analysis

2. **Interactive Development**
   - Iterative test development
   - Easy debugging with cell-by-cell execution
   - Inline visualizations of test results

3. **Comprehensive Documentation**
   - Tests can include explanatory markdown
   - Visual outputs show expected vs. actual
   - Examples serve as tutorials

4. **Flexible Execution**
   - Run tests independently of reports
   - Selective test execution during development
   - Easy integration with CI/CD (pytest-notebook)

5. **Reusability**
   - Test utilities can be extracted to modules
   - Notebooks can test multiple platforms
   - Setup code shared across test notebooks

#### Disadvantages ❌

1. **Duplication Risk**
   - May duplicate data loading code
   - Test environment setup separate from reports
   - Version control of .ipynb files (JSON format)

2. **Execution Overhead**
   - Separate step in workflow
   - Not automatically run when rendering reports
   - Requires discipline to run regularly

3. **Synchronization**
   - Tests may drift from actual report code
   - Changes to utils require updating tests separately

### Option B: Embedded Quarto Chunks

**Structure**:
```
reports/
├── reddit_br.qmd
│   └── (includes test chunks)
└── _tests.qmd  (shared test utilities)
```

#### Advantages ✅

1. **Single Source of Truth**
   - Tests run every time report renders
   - Guaranteed synchronization with report logic
   - Immediate feedback on data issues

2. **Self-Documenting**
   - Tests visible alongside results
   - Validation happens in context
   - Readers see data quality checks

3. **Simplified Workflow**
   - One command (`quarto render`) does everything
   - No separate test execution step
   - Freeze feature caches successful runs

4. **Native Integration**
   - Leverages Quarto's dependency tracking
   - Parameters can be shared across chunks
   - Output formats (HTML, PDF) include test results

#### Disadvantages ❌

1. **Cluttered Reports**
   - Test code mixes with presentation
   - Harder to distinguish validation from analysis
   - Reports become longer and more complex

2. **Performance**
   - Tests run on every render (unless frozen)
   - Slows down iterative report development
   - No selective test execution

3. **Limited Testing Scope**
   - Difficult to test utility functions in isolation
   - Cross-platform tests require multiple reports
   - No systematic test organization

4. **Readability**
   - Code-fold helps but tests still present
   - Readers may be confused by test chunks
   - Professional reports shouldn't expose tests

## Hybrid Approach (Recommended)

**Combine the strengths of both approaches:**

### Architecture

```
project/
├── tests/
│   ├── notebooks/
│   │   ├── test_data_validation.ipynb      # Development & documentation
│   │   ├── test_scoring_logic.ipynb
│   │   └── test_integration.ipynb
│   ├── pytest/
│   │   ├── test_loader.py                  # CI/CD automated tests
│   │   ├── test_scoring.py
│   │   └── conftest.py
│   └── test_data/
│       └── fixtures/
├── reports/
│   ├── reddit_br.qmd                       # Production reports
│   └── _validation.qmd                     # Shared minimal validation
└── utils/
    ├── loader.py
    ├── scoring.py
    └── validators.py                       # New: validation functions
```

### Implementation Strategy

#### 1. Lightweight Validation in Reports
Add **minimal, critical checks** directly in Quarto reports:

```{python}
#| label: validate-data
#| include: false

# Critical validation only - fast checks
from utils.validators import validate_answers

try:
    validate_answers(results)
except ValidationError as e:
    raise ValueError(f"Data validation failed: {e}")
```

**What to include in reports:**
- ✅ Data availability checks
- ✅ Required fields present
- ✅ Score bounds validation (0-100%)
- ❌ Comprehensive schema validation
- ❌ Unit tests of scoring functions
- ❌ Cross-platform consistency checks

#### 2. Comprehensive Tests in Notebooks
Use **Jupyter notebooks** for development, exploration, and documentation:

```python
# tests/notebooks/test_scoring_logic.ipynb

# Cell 1: Setup
from utils.scoring import calculate_platform_score
from utils.loader import load_questions, load_answers

# Cell 2: Test - Basic Scoring
def test_reddit_br_scoring():
    """Verify Reddit Brazil scores are calculated correctly"""
    results = calculate_platform_score('reddit', 'BR')

    # Expected scores (calculated manually)
    expected_ugc = 3.5  # UGC_01: 2.0*1.0 + UGC_02: 1.5*0.6 + UGC_03: 1.0*1.0

    assert abs(results['ugc_score'] - expected_ugc) < 0.01
    print(f"✓ UGC Score: {results['ugc_score']:.2f} (expected: {expected_ugc})")

test_reddit_br_scoring()

# Cell 3: Visual validation
import matplotlib.pyplot as plt
# ... plot expected vs actual scores
```

**What to include in notebooks:**
- ✅ Detailed test suites with explanations
- ✅ Visual validation (plots, tables)
- ✅ Edge case exploration
- ✅ Performance profiling
- ✅ Tutorial-style documentation

#### 3. Automated Tests with pytest
Use **pytest** for CI/CD pipeline:

```python
# tests/pytest/test_scoring.py

import pytest
from utils.scoring import calculate_question_score

def test_question_score_formula():
    """Test basic score calculation"""
    question = {
        'weight': 2.0,
        'answers': [{'value': 'yes', 'weight': 0.5}]
    }
    score = calculate_question_score(question, 'yes')
    assert score == 1.0

@pytest.mark.parametrize("platform,region", [
    ("reddit", "BR"),
    # Add more as available
])
def test_full_report_generation(platform, region):
    """Integration test: can we generate a complete report?"""
    results = calculate_platform_score(platform, region)
    assert 0 <= results['total_percentage'] <= 100
```

**Run in CI/CD:**
```bash
# .github/workflows/tests.yml
- name: Run pytest
  run: uv run pytest tests/pytest/
```

## Decision Matrix

| Criterion | Standalone Notebooks | Embedded Chunks | Hybrid |
|-----------|---------------------|-----------------|--------|
| **Report Clarity** | ⭐⭐⭐⭐⭐ Clean | ⭐⭐ Cluttered | ⭐⭐⭐⭐ Clean |
| **Test Coverage** | ⭐⭐⭐⭐⭐ Comprehensive | ⭐⭐⭐ Limited | ⭐⭐⭐⭐⭐ Comprehensive |
| **CI/CD Integration** | ⭐⭐⭐⭐ Good (pytest-notebook) | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐⭐ Excellent |
| **Development Speed** | ⭐⭐⭐⭐ Fast iteration | ⭐⭐ Slow renders | ⭐⭐⭐⭐ Fast iteration |
| **Documentation Value** | ⭐⭐⭐⭐⭐ High | ⭐⭐ Mixed with report | ⭐⭐⭐⭐⭐ High |
| **Maintenance Burden** | ⭐⭐⭐ Moderate sync | ⭐⭐⭐⭐ Auto-sync | ⭐⭐⭐ Moderate |
| **Reproducibility** | ⭐⭐⭐⭐ Explicit | ⭐⭐⭐⭐⭐ Built-in | ⭐⭐⭐⭐⭐ Best of both |
| **Reader Experience** | ⭐⭐⭐⭐⭐ Professional | ⭐⭐ Technical | ⭐⭐⭐⭐⭐ Professional |

## Recommendations

### For ITD Project: Hybrid Approach

**Phase 1: Immediate (Week 1-2)**
1. Create `utils/validators.py` with basic validation functions
2. Add minimal validation chunks to `reports/reddit_br.qmd` (hidden)
3. Create first test notebook: `tests/notebooks/01_data_validation.ipynb`

**Phase 2: Build Out (Week 3-4)**
4. Add `tests/pytest/` directory with unit tests
5. Create test notebooks for scoring logic and consistency
6. Set up GitHub Actions workflow for pytest

**Phase 3: Documentation (Week 5-6)**
7. Enhance test notebooks with explanatory markdown
8. Create tutorial notebook showing how to add new platforms
9. Document testing procedures in README

### Usage Guidelines

**When to use each approach:**

| Test Type | Location | Why |
|-----------|----------|-----|
| Data exists and loads | Report chunk | Fast, critical for rendering |
| Score bounds check | Report chunk | Quick validation, prevents errors |
| Manual score verification | Notebook | Visual, exploratory |
| Unit tests (utilities) | pytest | Fast, automatable |
| Schema validation | Notebook + pytest | Documentation + CI |
| Cross-platform consistency | Notebook | Complex, visual |
| Regression tests | pytest | CI/CD pipeline |
| Performance benchmarks | Notebook | Profiling tools, visualization |

## Implementation Example

### Step 1: Create validators.py

```python
# utils/validators.py

def validate_platform_results(results):
    """
    Validate computed results for a platform evaluation.

    Raises:
        ValueError: If validation fails
    """
    # Check required keys
    required = ['total_score', 'total_max', 'total_percentage',
                'ugc_score', 'ugc_max', 'ads_score', 'ads_max']
    for key in required:
        if key not in results:
            raise ValueError(f"Missing required key: {key}")

    # Check score bounds
    if not 0 <= results['total_percentage'] <= 100:
        raise ValueError(f"Invalid percentage: {results['total_percentage']}")

    # Check score consistency
    calculated_pct = (results['total_score'] / results['total_max']) * 100
    if abs(calculated_pct - results['total_percentage']) > 0.1:
        raise ValueError("Score percentage mismatch")

    return True
```

### Step 2: Add to Report

```markdown
<!-- reports/reddit_br.qmd -->

```{python}
#| label: setup
#| include: false

from utils.scoring import calculate_platform_score
from utils.validators import validate_platform_results

results = calculate_platform_score(platform='reddit', region='BR')

# Validate before proceeding
validate_platform_results(results)
```

### Step 3: Create Test Notebook

See appendix for full notebook example.

## Conclusion

**Recommendation: Hybrid Approach**

- **Reports remain clean and professional** (embedded validation only)
- **Comprehensive testing in notebooks** (development and documentation)
- **Automated testing with pytest** (CI/CD integration)

This approach provides:
- ✅ Maximum test coverage
- ✅ Clean, readable reports
- ✅ Excellent documentation
- ✅ CI/CD integration
- ✅ Flexibility for future growth

The hybrid approach is industry best practice for computational research projects, balancing rigor, usability, and maintainability.

---

## Next Steps

1. Review and approve this plan
2. Create initial directory structure
3. Implement validators.py
4. Create first test notebook
5. Set up pytest infrastructure
6. Configure CI/CD pipeline

Estimated effort: 2-3 weeks for full implementation
