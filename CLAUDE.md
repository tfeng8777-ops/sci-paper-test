# CLAUDE.md — Plant Exosome RNA Review Project

## Project Context

This is a SCI Q2-level review paper targeting **Journal of Nanobiotechnology** (IF ~10, BioMed Central).
The manuscript covers plant-derived exosome-like nanoparticles (PELNs/PDEVs) for cancer RNA therapy.

## Key Information

- **Target Journal**: Journal of Nanobiotechnology (BioMed Central)
- **Article Type**: Review
- **Original Language**: Chinese (draft at `drafts/original-zh.docx`)
- **Target Language**: English (for submission)
- **Reference Count**: 125 (needs formatting to journal style)
- **Figures**: 4 embedded in docx (need extraction and optimization)

## Manuscript Structure

1. Introduction (引言)
2. Overview of Plant Extracellular Vesicles (植物外囊泡概述)
3. RNA Composition and Cross-Kingdom Communication (RNA组成与跨界通讯机制)
   - 3.1 miRNA: Species, Abundance, and Cross-Kingdom Regulation
   - 3.2 siRNA: Endogenous siRNA and Therapeutic siRNA Delivery
   - 3.3 Other RNAs (mRNA, lncRNA, mtDNA)
   - 3.4 Molecular Mechanisms of Cross-Kingdom RNA Communication
4. Engineering Modification and Delivery Systems (工程化改造与递送系统)
   - 4.1 Surface Modification Strategies
   - 4.2 Drug Loading Strategies
   - 4.3 Hybrid Vesicles
   - 4.4 Oral Delivery Systems
5. Applications in Cancer Therapy (肿瘤治疗中的应用)
   - 5.1 Breast Cancer
   - 5.2 Glioma
   - 5.3 Colorectal Cancer
   - 5.4 Other Tumors
   - 5.5 Combined Immunotherapy
6. Challenges and Perspectives (挑战与展望)
7. Conclusion (结论)

## Writing Style Guidelines

- **Academic, precise, concise** — avoid redundant phrasing
- **Active voice preferred** where possible
- **No AI-hallucinated references** — only cite papers from the existing reference list
- **Use standardized nomenclature**: "plant-derived exosome-like nanovesicles (PELNs)" or "plant-derived extracellular vesicles (PDEVs)"
- **Figures**: describe key findings, not just "as shown in Figure X"
- **Abbreviations**: define at first use in each major section

## Translation Notes

When translating from Chinese to English:
- Chinese academic expressions often use implicit logic → make causal relationships explicit in English
- Break long Chinese sentences into 2-3 English sentences
- Chinese prefers active constructions → English academic writing can use passive where appropriate
- Pay attention to article usage (a/an/the) — Chinese lacks articles

## Reference Format (Journal of Nanobiotechnology)

```
[1] Author A, Author B. Title. Journal Name. Year;Volume(Issue):Pages.
```

BMC uses numbered citations in square brackets, e.g. [1], [1, 2], [1-3].

## Scripts

- `scripts/ai_translate.py` — Uses AI API to translate sections from Chinese to English
- `scripts/ai_polish.py` — Academic polishing of English text
- `scripts/extract_refs.py` — Extract and format references from docx bibliography
- `scripts/gen_cover_letter.py` — Generate cover letter for submission
