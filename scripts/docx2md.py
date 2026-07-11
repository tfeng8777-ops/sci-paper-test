#!/usr/bin/env python3
"""
Quick utility to convert docx to clean markdown for AI-assisted editing.

Usage:
    python scripts/docx2md.py --input drafts/original-zh.docx --output drafts/manuscript-zh.md
"""

import argparse
import re
import sys
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET


def extract_paragraphs(docx_path):
    """Extract paragraphs from docx."""
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


def extract_images(docx_path, output_dir):
    """Extract images from docx."""
    with zipfile.ZipFile(docx_path, 'r') as z:
        image_files = [f for f in z.namelist() if f.startswith('word/media/')]
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        extracted = []
        for img in image_files:
            filename = Path(img).name
            z.extract(img, output_dir)
            # Move from word/media/ to figures/
            src = output_dir / 'word' / 'media' / filename
            dst = output_dir / filename
            if src.exists():
                import shutil
                shutil.move(str(src), str(dst))
            extracted.append(str(dst))

        # Cleanup
        word_dir = output_dir / 'word'
        if word_dir.exists():
            import shutil
            shutil.rmtree(word_dir)

        return extracted


def paragraphs_to_markdown(paragraphs):
    """Convert paragraphs to clean markdown."""
    lines = []
    section_pattern = re.compile(r'^(\d+)\s+(.+)$')
    subsection_pattern = re.compile(r'^(\d+\.\d+)\s+(.+)$')

    for para in paragraphs:
        text = para.strip()
        if not text:
            lines.append('')
            continue

        # Skip TOC fields
        if text.startswith('TOC ') or 'HYPERLINK' in text or 'PAGEREF' in text:
            continue

        # Section headers
        sec_match = section_pattern.match(text)
        subsec_match = subsection_pattern.match(text)

        if sec_match and not subsec_match:
            num, title = sec_match.groups()
            lines.append(f'## {num} {title}')
        elif subsec_match:
            num, title = subsec_match.groups()
            level = num.count('.') + 1
            prefix = '#' * min(level + 1, 4)
            lines.append(f'{prefix} {num} {title}')
        elif text.startswith('Figure '):
            lines.append(f'\n*[{text}]*\n')
        else:
            lines.append(text)

    return '\n\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="Convert docx to markdown for AI editing")
    parser.add_argument("--input", "-i", required=True, help="Input docx file")
    parser.add_argument("--output", "-o", required=True, help="Output markdown file")
    parser.add_argument("--extract-images", action="store_true",
                        help="Also extract embedded images")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    print(f"Converting {args.input} to markdown...")
    paragraphs = extract_paragraphs(input_path)
    markdown = paragraphs_to_markdown(paragraphs)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding='utf-8')

    print(f"✓ Saved markdown to {args.output}")
    print(f"  {len(paragraphs)} paragraphs extracted")

    if args.extract_images:
        figures_dir = Path(args.output).parent.parent / 'manuscript' / 'figures'
        images = extract_images(input_path, figures_dir)
        print(f"✓ Extracted {len(images)} images to {figures_dir}")


if __name__ == "__main__":
    main()
