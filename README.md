# Social Media Platform Evaluation System

A Quarto-based research reporting system for evaluating social media platforms across multiple regions using weighted scoring methodology.

## Project Structure

```
social-media-eval/
├── _quarto.yml              # Main Quarto configuration
├── _brand.yml               # Custom color theme
├── index.qmd                # Landing page
├── data/
│   ├── questions_2025.yml   # Global weighted questions (year-specific)
│   └── 2025/                # Year-based organization
│       ├── global/          # Global platform evaluations
│       │   └── kwai.yml     # Sample global template
│       └── regional/        # Regional evaluations
│           ├── BR/          # Brazil region
│           │   └── reddit/
│           │       ├── answers/
│           │       │   └── reddit_br.yml
│           │       └── report/
│           │           └── reddit_br.qmd
│           ├── UK/          # United Kingdom region
│           └── EU/          # European Union region
├── bib/
│   ├── references_global.bib # Global bibliography
│   └── reddit.bib           # Platform-specific bibliography
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
Edit `data/questions_2025.yml` (or the appropriate year) to add evaluation questions organized by category:

```yaml
categories:
  - name: consistency
    label: "Consistency"
    description: "Evaluates how consistently the platform applies policies"
    questions:
      - code: UGC_01
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

For **regional** evaluations, create:
`data/2025/regional/{REGION}/{platform}/answers/{platform}_{region}.yml`

For **global** evaluations, create:
`data/2025/global/{platform}.yml`

Organize answers by category:

```yaml
metadata:
  platform: "Reddit"
  region_code: "BR"
  region_name: "Brazil"
  evaluation_date: "2025-01-15"

consistency_answers:
  - question_code: UGC_01
    selected_answer: "yes"
    notes: "Policy available at [URL]"

timeliness_answers:
  - question_code: UGC_03
    selected_answer: "regular"
    notes: "Publishes bi-annual reports"
```

### 3. Create Report File

For **regional** evaluations, create:
`data/2025/regional/{REGION}/{platform}/report/{platform}_{region}.qmd`

For **global** evaluations, create:
`data/2025/global/report/{platform}.qmd`

```markdown
---
title: "Platform - Region"
---

\```{python}
import sys
from pathlib import Path
project_root = Path.cwd()
while not (project_root / 'utils').exists() and project_root != project_root.parent:
    project_root = project_root.parent
sys.path.insert(0, str(project_root))

from utils.scoring import calculate_platform_score

# For regional evaluation
results = calculate_platform_score(
    platform='reddit',
    region='BR',
    year='2025',
    scope='regional'
)

# For global evaluation
# results = calculate_platform_score(
#     platform='kwai',
#     region='GLOBAL',
#     year='2025',
#     scope='global'
# )
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

# Access category-specific scores
for category_name, category_data in results['categories'].items():
    print(f"{category_data['label']}: {category_data['percentage']:.1f}%")
```

## Adding New Platforms

### For Regional Evaluation
1. **Create platform directory**: `data/2025/regional/{REGION}/{platform}/`
2. **Create answer file**: `data/2025/regional/{REGION}/{platform}/answers/{platform}_{region}.yml`
3. **Create report**: `data/2025/regional/{REGION}/{platform}/report/{platform}_{region}.qmd`
4. **Update** `_quarto.yml` to include new report
5. **Render**: `quarto render`

### For Global Evaluation
1. **Create answer file**: `data/2025/global/{platform}.yml`
2. **Create report directory** (if needed): `data/2025/global/report/`
3. **Create report**: `data/2025/global/report/{platform}.qmd`
4. **Update** `_quarto.yml` to include new report
5. **Render**: `quarto render`

## Adding New Questions

1. **Edit** `data/questions_2025.yml` (or appropriate year file)
2. **Choose existing category** or create a new one
3. **Add question** with code, weight, and answers under the category
4. **Update answer files** to include responses using `{category}_answers` structure
5. **Re-render** reports

## Working with Different Years

To create evaluations for a new year (e.g., 2026):

1. **Copy questions file**: `cp data/questions_2025.yml data/questions_2026.yml`
2. **Create year directory**: `mkdir -p data/2026/{global,regional/{BR,UK,EU}}`
3. **Update questions** in the new year file as needed
4. **Create platform evaluations** following the same structure under `data/2026/`
5. **Use year parameter**: Pass `year='2026'` to `calculate_platform_score()`

## License

XXXXX

## Contributing

XXXXX

## Contact

XXXXXXx