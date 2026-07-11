#!/usr/bin/env python3
"""
Extract and format references from docx bibliography.
Converts Zotero/Word bibliography to BibTeX and formatted reference list.

Usage:
    python scripts/extract_refs.py --input drafts/original-zh.docx --output references/references.bib
"""

import argparse
import re
import sys
from pathlib import Path


def extract_text_from_docx(docx_path):
    """Extract all text from a docx file using zipfile + xml."""
    import zipfile
    import xml.etree.ElementTree as ET

    with zipfile.ZipFile(docx_path, 'r') as z:
        xml_content = z.read('word/document.xml')

    tree = ET.fromstring(xml_content)
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

    paragraphs = []
    for para in tree.iter(f'{{{ns}}}p'):
        texts = []
        for t in para.iter(f'{{{ns}}}t'):
            if t.text:
                texts.append(t.text)
        if texts:
            paragraphs.append(''.join(texts))

    return paragraphs


def parse_references(paragraphs):
    """Parse reference entries from extracted paragraphs."""
    refs = []
    in_bibliography = False
    current_ref = ""

    # Pattern for reference entries like [1] ... [2] ...
    ref_pattern = re.compile(r'^\[\d+\]')

    for para in paragraphs:
        # Check if we've entered the bibliography section
        if 'CSL_BIBLIOGRAPHY' in para or para.strip().startswith('[1]'):
            in_bibliography = True

        if in_bibliography:
            if ref_pattern.match(para.strip()):
                if current_ref:
                    refs.append(current_ref.strip())
                current_ref = para.strip()
            elif current_ref:
                current_ref += ' ' + para.strip()

    if current_ref:
        refs.append(current_ref.strip())

    return refs


def ref_to_bibtex(ref_num, ref_text):
    """Convert a single reference to BibTeX format."""
    # Remove the citation number prefix
    text = re.sub(r'^\[\d+\]\s*', '', ref_text)

    # Try to extract components
    authors = ""
    title = ""
    journal = ""
    year = ""
    volume = ""
    pages = ""
    doi = ""

    # Extract year
    year_match = re.search(r'\(?(\d{4})\)?', text)
    if year_match:
        year = year_match.group(1)

    # Try to split by common patterns
    parts = text.split('.')
    if len(parts) >= 3:
        authors = parts[0].strip() if len(parts) > 0 else ""
        title = parts[1].strip() if len(parts) > 1 else ""
        journal = parts[2].strip() if len(parts) > 2 else ""

    # Generate a citation key
    first_author = authors.split(',')[0].split(' ')[0].strip() if authors else "unknown"
    key = f"{first_author}{year}"

    # Clean the key
    key = re.sub(r'[^a-zA-Z0-9]', '', key).lower()

    bibtex = f"""@article{{{key},
  author = {{{authors}}},
  title = {{{title}}},
  journal = {{{journal}}},
  year = {{{year}}},
  volume = {{{volume}}},
  pages = {{{pages}}},
  number = {{{ref_num}}}
}}"""

    return bibtex


def main():
    parser = argparse.ArgumentParser(description="Extract references from docx to BibTeX")
    parser.add_argument("--input", "-i", required=True, help="Input docx file")
    parser.add_argument("--output", "-o", required=True, help="Output BibTeX file")
    parser.add_argument("--format", choices=["bibtex", "text"], default="bibtex",
                        help="Output format (default: bibtex)")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    print(f"Extracting references from {args.input}...")
    paragraphs = extract_text_from_docx(args.input)

    refs = parse_references(paragraphs)
    print(f"Found {len(refs)} references")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "bibtex":
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("% References extracted from original manuscript\n")
            f.write(f"% Total: {len(refs)} references\n\n")
            for i, ref in enumerate(refs):
                bibtex = ref_to_bibtex(i + 1, ref)
                f.write(bibtex)
                f.write('\n\n')
    else:
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, ref in enumerate(refs):
                f.write(f"[{i+1}] {ref}\n\n")

    print(f"✓ Saved {len(refs)} references to {args.output}")


if __name__ == "__main__":
    main()
