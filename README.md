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

## Weighted Scoring Methodology

### Question Weights
Each question has an **importance weight** (1.0 to 2.5+):
- Higher weight = more critical question
- Example: Ad transparency might be weighted 2.5, while minor features 1.0

### Answer Weights
Each possible answer has a **performance weight** (0.0 to 1.0):
- `1.0` = Best practice / full compliance
- `0.5` = Partial implementation
- `0.0` = No implementation / poor practice

### Score Calculation
```
Question Score = Question Weight × Answer Weight
Category Score = Sum of all Question Scores in category
Total Score = UGC Score + ADS Score
```

### Example
```yaml
# Question with weight 2.0
question_weight: 2.0

# Selected answer with weight 0.5
answer_weight: 0.5

# Final question score
score: 2.0 × 0.5 = 1.0

# If max possible was 2.0 (weight × 1.0)
percentage: 1.0 / 2.0 = 50%
```

## Installation

### Prerequisites
- Python 3.8+
- Quarto 1.3+
- PyYAML
- Pandas

### Setup
```bash
# Install Python dependencies
pip install pyyaml pandas

# Install Quarto
# Visit https://quarto.org/docs/get-started/

# Clone repository
git clone <repository-url>
cd social-media-eval
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

### 4. Update _quarto.yml
Add new report to book chapters:

```yaml
book:
  chapters:
    - index.qmd
    - part: "Country Reports"
      chapters:
        - reports/reddit_br.qmd
        - reports/facebook_uk.qmd  # Add new reports here
```

### 5. Render Reports

```bash
# Render to HTML
quarto render

# Render to PDF
quarto render --to pdf

# Preview with live reload
quarto preview
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

## Customization

### Colors
Edit `_brand.yml` to change theme colors:

```yaml
scss:
  primary: "#2C5F8D"    # Main brand color
  success: "#27AE60"    # High scores
  warning: "#F39C12"    # Medium scores
  danger: "#E74C3C"     # Low scores
```

### Question Weights
Adjust importance in `data/questions.yml`:
- `1.0` = Standard importance
- `2.0` = High importance
- `2.5+` = Critical importance

### Answer Weights
Define performance levels:
- `1.0` = Excellent
- `0.7-0.9` = Good
- `0.4-0.6` = Moderate
- `0.1-0.3` = Poor
- `0.0` = Unacceptable

## Output Formats

- **HTML**: Interactive book with navigation
- **PDF**: Print-ready reports with table of contents
- **Single files**: Use `embed-resources: true` for standalone HTML

## License

[Specify your license]

## Contributing

1. Add new questions to `data/questions.yml`
2. Create answer files for new platforms/regions
3. Build platform-specific bibliographies in `bib/`
4. Submit pull requests with evaluation methodology

## Contact

[Your contact information]
