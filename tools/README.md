# PDF Question Explanation Generator

This tool extracts questions from the CulegereLicenta_2025_ro.pdf file and generates explanations for correct answers.

## Usage

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the script:
```bash
python generate_explanations.py
```

This will generate:
- `Explicatii_CulegereLicenta_2025.md` - Markdown file with explanations
- `Explicatii_CulegereLicenta_2025.pdf` - PDF version of the explanations

## Requirements

- Python 3.7+
- Dependencies listed in requirements.txt
- The original PDF file should be in the parent directory