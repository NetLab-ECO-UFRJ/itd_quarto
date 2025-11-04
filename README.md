# Social Media Platform Evaluation System

A Quarto-based research reporting system for evaluating social media platforms across multiple regions using weighted scoring methodology.

## Project Structure

```
social-media-eval/
├── _quarto.yml              # Main Quarto configuration
├── _brand.yml               # Custom color theme
├── index.qmd                # Landing page
├── data/
│   ├── questions.yml        # Global weighted questions
│   └── answers/
│       └── reddit_br.yml    # Platform-specific answers
├── bib/
│   └── references_global.bib # Bibliography
├── reports/
│   └── reddit_br.qmd        # Platform reports
└── utils/
    ├── __init__.py
    ├── loader.py            # YAML data loading
    └── scoring.py           # Weighted score calculation
```

## Installation

### Prerequisites
- Python 3.9+
- Quarto 1.3+
- uv (Python package manager)

### Setup
```bash
# Clone repository
git clone <repository-url>
cd social-media-eval

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python dependencies
uv sync

# Install Quarto
# Visit https://quarto.org/docs/get-started/
```

## Usage

### 1. Define Questions
Edit `data/questions.yml` to add evaluation questions:

```yaml
questions:
  - code: UGC_01
    category: UGC
    text: "Does the platform have clear policies?"
    weight: 2.0  # Importance weight
    answers:
      - value: "no"
        label: "No policy"
        weight: 0.0  # Performance weight
      - value: "yes"
        label: "Clear policy"
        weight: 1.0
```

### 2. Create Answer Files
Create `data/answers/{platform}_{country}.yml`:

```yaml
metadata:
  platform: "Reddit"
  country_code: "BR"
  country_name: "Brazil"
  evaluation_date: "2025-01-15"

ugc_answers:
  - question_code: UGC_01
    selected_answer: "yes"
    notes: "Policy available at [URL]"

ads_answers:
  - question_code: ADS_01
    selected_answer: "partial"
    notes: "Limited ad library"
```

### 3. Create Report File
Create `reports/{platform}_{country}.qmd`:

```markdown
---
title: "Platform - Country"
---

\```{python}
from utils.scoring import calculate_platform_score

results = calculate_platform_score(
    platform='reddit',
    country='BR'
)
\```

# Results
Score: `{python} results['total_percentage']`%
```


### Render Reports

```bash
# Render to HTML (uv ensures Python dependencies are available)
uv run quarto render

# Render to PDF
uv run quarto render --to pdf

# Preview with live reload
uv run quarto preview

# Or activate the virtual environment first
source .venv/bin/activate
quarto render
```

Output will be in `_output/` directory.

## Python API

### Load Data
```python
from utils.loader import load_questions, load_answers

# Load all questions
questions = load_questions()

# Load platform answers
answers = load_answers('reddit', 'BR')
```

### Calculate Scores
```python
from utils.scoring import calculate_platform_score

# Calculate all scores for a platform
results = calculate_platform_score('reddit', 'BR')

print(f"Total: {results['total_score']:.2f} / {results['total_max']:.2f}")
print(f"UGC: {results['ugc_percentage']:.1f}%")
print(f"ADS: {results['ads_percentage']:.1f}%")
```

## Adding New Platforms

1. **Create answer file**: `data/answers/{platform}_{country}.yml`
2. **Create report**: `reports/{platform}_{country}.qmd`
3. **Update** `_quarto.yml` to include new report
4. **Render**: `quarto render`

## Adding New Questions

1. **Edit** `data/questions.yml`
2. **Add question** with code, category, weight, and answers
3. **Update answer files** to include responses to new questions
4. **Re-render** reports

## License

XXXXX

## Contributing

XXXXX

## Contact

XXXXXXx