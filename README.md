# Social Media Platform Evaluation System

A Quarto-based research reporting system for evaluating social media platforms across multiple regions using a weighted scoring methodology.

## Para fazer

- importa data from Meta, Reddit
- add emojis to partial answers
- import evaluations from UK and UE
- Review scripts that calculate the score

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

## Importing Data from Excel

### Overview

The project includes a script to import platform assessment data from Excel files and generate YAML files and QMD reports automatically.

### Before Importing

**Important:** To avoid conflicts or issues with existing data, remove the platform directory before reimporting.

```bash
# Remove existing platform data 
rm -rf data/2025/global/*

# For regional data 
rm -rf data/2025/regional/BR/*
```

### Excel File Location

Place your Excel files in the `data/2025/xlsx_backups/` directory. The script expects two files:
- One for UGC (User-Generated Content) framework responses
- One for ADS (Advertising) framework responses

### Import Commands

#### Bulk Import (All Platforms)

Import all global platforms:

```bash
for platform in telegram bluesky discord kwai; do uv run python scripts/transform_excel_to_yaml.py --platform $platform --scope-type global --ads-file "Advertising Framework (respostas).xlsx" --ugc-file "UGC Framework (respostas).xlsx"; done
```

Import regional in Brazil:

```bash
for platform in x tiktok linkedin pinterest snapchat; do uv run python scripts/transform_excel_to_yaml.py --platform $platform --scope-type regional --region br --ads-file "Advertising Framework (respostas).xlsx" --ugc-file "UGC Framework (respostas).xlsx"; done
```

This command:
- Imports **global scope**: Telegram, Bluesky, Discord, TikTok, Kwai, LinkedIn, Pinterest, Snapchat

#### Individual Platform Import

##### Global Scope

For global assessments:

```bash
uv run python scripts/transform_excel_to_yaml.py \
  --platform bluesky \
  --scope-type global \
  --ads-file "Advertising Framework (respostas).xlsx" \
  --ugc-file "UGC Framework (respostas).xlsx"
```

##### Regional Scope

For regional assessments:

```bash
uv run python scripts/transform_excel_to_yaml.py \
  --platform x \
  --scope-type regional \
  --region BR \
  --ads-file "Advertising Framework (respostas).xlsx" \
  --ugc-file "UGC Framework (respostas).xlsx"
```

Note: Both global and regional scopes now use the same Excel file parameters.

### What the Script Does

1. **Reads Excel files** from `data/2025/xlsx_backups/`
2. **Creates YAML files** with normalized answers:
   - `data/2025/global/{platform}/ugc.yml`
   - `data/2025/global/{platform}/ads.yml`
3. **Generates QMD report** from template:
   - `data/2025/global/{platform}/{platform}.qmd`

### After Import

Once imported, update `_quarto.yml` to include the new platform in the book chapters:

```yaml
- part: "Global Assessments"
  chapters:
    - data/2025/global/bluesky/bluesky.qmd
```

Then render the report:

```bash
uv run quarto render data/2025/global/bluesky/bluesky.qmd --to html
```

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
