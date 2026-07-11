#!/usr/bin/env python3
"""
AI-Assisted Academic Translator
Translates Chinese academic text to polished English, optimized for biomedical manuscripts.
Supports both OpenAI and Anthropic APIs.

Usage:
    python scripts/ai_translate.py --input drafts/manuscript-zh.md --output drafts/translations/manuscript-en.md
    python scripts/ai_translate.py --input drafts/manuscript-zh.md --api anthropic --model claude-sonnet-5
"""

import argparse
import os
import sys
import re
import json
import time
from pathlib import Path

# ===== Configuration =====
# You can also set these via environment variables
DEFAULT_CONFIG = {
    "openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
    "openai_model": "gpt-4o",
    "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY", ""),
    "anthropic_model": "claude-sonnet-5",
    "chunk_size": 5,  # paragraphs per API call
    "temperature": 0.3,
    "max_tokens": 4096,
}

TRANSLATION_PROMPT = """You are an expert scientific translator specializing in biomedical and nanotechnology manuscripts.

Translate the following Chinese academic text into polished, publication-ready English suitable for submission to Journal of Nanobiotechnology (a high-impact BMC journal, IF ~10).

Guidelines:
1. Output ONLY the English translation, no explanations
2. Use precise scientific terminology (e.g., "plant-derived exosome-like nanovesicles" not "plant exosomes")
3. Make implicit logical connections explicit in English
4. Break long Chinese sentences into concise English sentences
5. Maintain ALL citations [N] exactly as they appear
6. Preserve technical terms, gene names, and numerical values exactly
7. Use passive voice where appropriate for academic style
8. Ensure proper use of articles (a/an/the)
9. Keep paragraph breaks consistent with the source

Chinese text to translate:
---
{text}
---

English translation:"""

POLISH_PROMPT = """You are an expert academic editor for high-impact nanotechnology and biomedical journals.

Polish the following English academic text to meet the standards of Journal of Nanobiotechnology (IF ~10).

Guidelines:
1. Output ONLY the polished text, no explanations
2. Improve sentence flow and academic tone
3. Eliminate redundancy and wordiness
4. Fix grammar, article usage, and awkward phrasing
5. Ensure logical flow between sentences and paragraphs
6. Maintain ALL citations [N] exactly
7. Keep technical terminology unchanged
8. Target: concise, precise, impactful academic prose

Text to polish:
---
{text}
---

Polished text:"""


def split_into_chunks(text, chunk_size=5):
    """Split text into chunks of N paragraphs."""
    paragraphs = text.strip().split('\n\n')
    chunks = []
    for i in range(0, len(paragraphs), chunk_size):
        chunks.append('\n\n'.join(paragraphs[i:i + chunk_size]))
    return chunks


def translate_with_openai(text, config):
    """Translate using OpenAI API."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=config["openai_api_key"])

        chunks = split_into_chunks(text, config["chunk_size"])
        results = []

        for i, chunk in enumerate(chunks):
            print(f"  Translating chunk {i+1}/{len(chunks)}...")
            response = client.chat.completions.create(
                model=config["openai_model"],
                messages=[
                    {"role": "system", "content": "You are an expert biomedical translator. Translate Chinese to polished academic English."},
                    {"role": "user", "content": TRANSLATION_PROMPT.format(text=chunk)}
                ],
                temperature=config["temperature"],
                max_tokens=config["max_tokens"],
            )
            results.append(response.choices[0].message.content.strip())
            time.sleep(0.5)  # Rate limiting

        return '\n\n'.join(results)

    except ImportError:
        print("Error: openai package not installed. Run: pip install openai")
        sys.exit(1)
    except Exception as e:
        print(f"OpenAI API error: {e}")
        sys.exit(1)


def translate_with_anthropic(text, config):
    """Translate using Anthropic Claude API."""
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=config["anthropic_api_key"])

        chunks = split_into_chunks(text, config["chunk_size"])
        results = []

        for i, chunk in enumerate(chunks):
            print(f"  Translating chunk {i+1}/{len(chunks)}...")
            response = client.messages.create(
                model=config["anthropic_model"],
                max_tokens=config["max_tokens"],
                temperature=config["temperature"],
                messages=[
                    {"role": "user", "content": TRANSLATION_PROMPT.format(text=chunk)}
                ]
            )
            results.append(response.content[0].text.strip())
            time.sleep(0.5)

        return '\n\n'.join(results)

    except ImportError:
        print("Error: anthropic package not installed. Run: pip install anthropic")
        sys.exit(1)
    except Exception as e:
        print(f"Anthropic API error: {e}")
        sys.exit(1)


def markdown_to_file(text, output_path):
    """Save translated text to markdown file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding='utf-8')
    print(f"  Saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="AI-assisted academic translation (Chinese → English)"
    )
    parser.add_argument("--input", "-i", required=True, help="Input markdown file (Chinese)")
    parser.add_argument("--output", "-o", required=True, help="Output markdown file (English)")
    parser.add_argument("--api", choices=["openai", "anthropic"], default="openai",
                        help="AI API to use (default: openai)")
    parser.add_argument("--model", help="Override default model")
    parser.add_argument("--polish", action="store_true",
                        help="Also run academic polishing pass")

    args = parser.parse_args()

    config = DEFAULT_CONFIG.copy()
    if args.model:
        if args.api == "openai":
            config["openai_model"] = args.model
        else:
            config["anthropic_model"] = args.model

    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    text = input_path.read_text(encoding='utf-8')
    print(f"Read {len(text)} characters from {args.input}")

    # Translate
    print(f"\nTranslating with {args.api} ({config.get(args.api + '_model', 'default')})...")
    if args.api == "openai":
        translated = translate_with_openai(text, config)
    else:
        translated = translate_with_anthropic(text, config)

    # Save translation
    markdown_to_file(translated, args.output)

    # Optional polish pass
    if args.polish:
        print("\nPolishing English text...")
        if args.api == "openai":
            try:
                from openai import OpenAI
                client = OpenAI(api_key=config["openai_api_key"])
                response = client.chat.completions.create(
                    model=config["openai_model"],
                    messages=[
                        {"role": "system", "content": "You are an expert academic editor."},
                        {"role": "user", "content": POLISH_PROMPT.format(text=translated)}
                    ],
                    temperature=0.3,
                    max_tokens=config["max_tokens"],
                )
                polished = response.choices[0].message.content.strip()
            except Exception:
                print("Polish step failed, saving unpolished translation.")
                polished = translated
        else:
            try:
                from anthropic import Anthropic
                client = Anthropic(api_key=config["anthropic_api_key"])
                response = client.messages.create(
                    model=config["anthropic_model"],
                    max_tokens=config["max_tokens"],
                    temperature=0.3,
                    messages=[
                        {"role": "user", "content": POLISH_PROMPT.format(text=translated)}
                    ]
                )
                polished = response.content[0].text.strip()
            except Exception:
                print("Polish step failed, saving unpolished translation.")
                polished = translated

        polished_path = args.output.replace('.md', '_polished.md')
        markdown_to_file(polished, polished_path)

    print("\n✓ Translation complete!")


if __name__ == "__main__":
    main()
