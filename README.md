# Plant-Derived Exosome-Like Nanoparticles in Cancer RNA Therapy: From Cross-Kingdom Communication to Engineered Oral Delivery

> **植物源外泌体样纳米颗粒在癌症RNA治疗中的应用：从跨界通讯到工程化口服递送**

[![Status](https://img.shields.io/badge/status-draft-orange)](.)
[![Target Journal](https://img.shields.io/badge/target-Journal%20of%20Nanobiotechnology-blue)](https://jnanobiotechnology.biomedcentral.com/)
[![Language](https://img.shields.io/badge/manuscript-en%20%7C%20zh-green)](.)

## 📄 Overview

This repository contains the manuscript for a comprehensive review on plant-derived exosome-like nanovesicles (PELNs/PDEVs) in cancer RNA therapy. The review covers:

- **Cross-kingdom RNA communication** via plant extracellular vesicles
- **RNA cargo composition** (miRNA, siRNA, mRNA, lncRNA)
- **Engineering strategies** (surface modification, drug loading, hybrid vesicles)
- **Oral delivery systems** and gut-microbiome-immune axis
- **Cancer applications** (breast, glioma, colorectal, lung, pancreatic, etc.)
- **Challenges and perspectives** for clinical translation

## 📁 Repository Structure

```
├── manuscript/           # LaTeX manuscript files
│   ├── main.tex         # Main LaTeX document
│   ├── sections/        # Individual sections
│   ├── figures/         # High-resolution figures
│   └── tables/          # Tables
├── references/          # Bibliography
│   └── references.bib   # BibTeX references
├── drafts/              # Draft versions
│   ├── original-zh.docx # Original Chinese draft
│   └── translations/    # Translation versions
├── scripts/             # Utility scripts
│   ├── ai_translate.py  # AI-assisted translation
│   ├── ai_polish.py     # AI-assisted academic polishing
│   └── format_refs.py   # Reference formatting
├── templates/           # Journal templates
│   └── jnanobiotech/    # Journal of Nanobiotechnology
└── outputs/             # Compiled manuscripts
```

## 🚀 Workflow

1. **Translate**: `python scripts/ai_translate.py --input drafts/original-zh.docx`
2. **Polish**: `python scripts/ai_polish.py --input manuscript/main.tex`
3. **Compile**: Use `latexmk -pdf manuscript/main.tex`
4. **Cite**: Manage references in `references/references.bib`

## 🔗 Key Resources

- [Journal of Nanobiotechnology - Submission Guidelines](https://jnanobiotechnology.biomedcentral.com/submission-guidelines)
- [BMC LaTeX Template](https://www.overleaf.com/latex/templates/biomed-central-article-template/gcgcxpjgjpgx)
- [MISEV Guidelines for EV Research](https://www.isev.org/misev)

## 👥 Setup

```bash
# Install dependencies
pip install openai anthropic python-docx

# Setup Git remote (replace USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/plant-exosome-rna-review.git
git push -u origin main
```

## 📝 License

This work is academic research. All rights reserved.
