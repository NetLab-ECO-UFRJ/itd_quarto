# Social Media Platform Evaluation System

A Quarto-based research reporting system for evaluating social media platforms across multiple regions using a weighted scoring methodology.

## Para fazer

- Review the taxonomy of question and answers YAML files.

- Review scripts that calculate the score

- Script/methods to convert to/from YAML <> CSV

## Project Structure

TBC

## Technical setup

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
## License

XXXXX

## Contributing

XXXXX

## Contact

XXXXXXx
