# 📚 Literature Database — Plant Exosome RNA Cancer Therapy

> **Total: 200+ papers across 7 topic areas**
> Target Journal: *Journal of Nanobiotechnology*
> Generated: 2026-07-11

---

## 📑 Topic Index

| # | Topic | Papers | Description |
|---|-------|--------|-------------|
| 01 | [Plant EVs General](01-plant-evs-general/) | ~35 | PELNs/PDEVs overview, isolation, characterization, therapeutic potential |
| 02 | [RNA Cross-Kingdom](02-rna-cross-kingdom/) | ~35 | miRNA, siRNA, mRNA cross-kingdom communication mechanisms |
| 03 | [Engineering & Delivery](03-engineering-delivery/) | ~30 | Surface modification, drug loading, hybrid vesicles, oral delivery |
| 04 | [Cancer Applications](04-cancer-applications/) | ~40 | Breast, glioma, colorectal, lung, pancreatic, gastric, melanoma, immunotherapy |
| 05 | [Clinical Translation](05-clinical-translation/) | ~30 | GMP manufacturing, scale-up, regulatory, MISEV guidelines |
| 06 | [Mammalian EVs Reference](06-mammalian-evs-reference/) | ~25 | EV biogenesis, engineering, MSC-EVs, fundamental principles |
| 07 | [RNA Therapeutics](07-rna-therapeutics/) | ~25 | siRNA, mRNA, LNPs, CRISPR, clinical landscape |

**+125 papers from original manuscript** (`references/references.bib`)

---

## 🔍 Quick Search Guide

### By Keyword

| Keyword | Best Topic(s) |
|---------|---------------|
| Ginger/grapefruit/lemon EVs | 01, 04 |
| miRNA cross-kingdom | 02 |
| siRNA delivery | 02, 03, 07 |
| Oral delivery | 03 |
| Blood-brain barrier | 04 (Glioma section) |
| Breast cancer | 04 |
| Colorectal cancer | 04 |
| GMP/scale-up | 05 |
| MISEV/characterization | 05, 06 |
| LNP/mRNA vaccines | 07 |
| Immunotherapy | 04 |

### By Year

| Year Range | Focus |
|------------|-------|
| 2024-2026 | Latest reviews, engineering advances, clinical trials |
| 2020-2023 | Foundational PELN studies, key mechanism papers |
| 2015-2019 | Early cross-kingdom discoveries, seminal EV papers |

### By Journal

Top journals represented:
- *Journal of Nanobiotechnology*
- *International Journal of Nanomedicine*
- *Journal of Extracellular Vesicles*
- *Journal of Controlled Release*
- *Nature Nanotechnology / Nature Reviews*
- *ACS Nano / Nano Letters*
- *Advanced Drug Delivery Reviews*
- *Frontiers in Bioengineering*

---

## 🛠 Usage

### Merge all topic files into one master BibTeX:

```bash
cat literature/*/references.bib references/references.bib > literature/master.bib
```

### Search across all papers:

```bash
# Search for "ginger" in all BibTeX files
grep -rl "ginger" literature/*/references.bib

# Search in titles
grep "title" literature/*/references.bib | grep -i "miRNA"
```

### Import into Zotero:

```bash
# Better BibTeX can auto-import .bib files
# File → Import → literature/master.bib
```

### Use with LaTeX:

```latex
% In your manuscript:
\bibliography{
  ../references/references,
  ../literature/01-plant-evs-general/references,
  ../literature/02-rna-cross-kingdom/references,
  ../literature/03-engineering-delivery/references,
  ../literature/04-cancer-applications/references,
  ../literature/05-clinical-translation/references,
  ../literature/06-mammalian-evs-reference/references,
  ../literature/07-rna-therapeutics/references
}
```

---

## 📝 Update Schedule

- Pre-submission: verify all citations match target journal format
- Monthly: add new publications via `pubmed_search.py`
- Per revision: check for retracted/updated papers

---

## ⚠️ Notes

- Some BibTeX entries may have incomplete DOI/volume/page fields — fill in before final submission
- Papers marked as `{Various Authors}` need author lists completed
- Cross-reference with your Zotero library for duplicate detection
