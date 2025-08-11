# PDF Question Explanation Generator

This tool extracts questions from the CulegereLicenta_2025_ro.pdf file and generates explanations for correct answers only.

## Requirements

The following system packages are required:
- poppler-utils (for pdftotext)
- pandoc (for PDF generation)
- texlive-latex-base, texlive-fonts-recommended, texlive-latex-extra (for LaTeX PDF engine)

## Installation

On Ubuntu/Debian systems:
```bash
sudo apt-get install poppler-utils pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-extra
```

## Usage

1. Basic version (sample explanations):
```bash
python generate_explanations.py
```

2. Complete version (processes all questions from PDF):
```bash
python generate_complete_explanations.py
```

This will generate:
- `Explicatii_CulegereLicenta_2025.md` - Markdown file with explanations
- `Explicatii_CulegereLicenta_2025.pdf` - PDF version of the explanations

## Output Structure

The generated files contain:
- **Tematica 1**: Structuri discrete și algoritmi
- **Tematica 2**: Limbaje de programare și inginerie software  
- **Tematica 3**: Sisteme de calcul

For each question, only the correct answer options are shown with brief explanations (1-2 sentences) in Romanian.

## Limitations

- Complex mathematical symbols are converted to ASCII equivalents for PDF compatibility
- Some questions may require manual verification if OCR extraction is incomplete
- Explanations are generated using pattern matching and may need refinement for highly technical content