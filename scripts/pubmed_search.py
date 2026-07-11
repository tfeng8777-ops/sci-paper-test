#!/usr/bin/env python3
"""
PubMed Literature Search & BibTeX Generator
============================================
Search PubMed for papers related to plant-derived exosomes and RNA cancer therapy.
Generates structured BibTeX entries organized by topic.

Requirements: pip install biopython requests

Usage:
    python scripts/pubmed_search.py --topic "plant extracellular vesicles" --max 50
    python scripts/pubmed_search.py --all-topics --max 30
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

# ===== Topic Search Queries =====
TOPICS = {
    "01-plant-evs-general": [
        '("plant-derived extracellular vesicles"[Title/Abstract] OR "plant exosome-like nanoparticles"[Title/Abstract] OR "plant nanovesicles"[Title/Abstract]) AND ("2019"[Date - Publication] : "2026"[Date - Publication])',
        '("edible plant exosomes"[Title/Abstract] OR "fruit-derived nanovesicles"[Title/Abstract] OR "plant-derived exosomes" AND review[Publication Type])',
        '("ginger exosome-like nanoparticles"[All Fields] OR "grapefruit-derived nanovectors"[All Fields] OR "lemon extracellular vesicles"[All Fields] OR "ginseng exosomes"[All Fields])',
    ],
    "02-rna-cross-kingdom": [
        '("cross-kingdom RNA"[Title/Abstract] OR "plant miRNA cross-kingdom"[Title/Abstract]) AND ("extracellular vesicles"[Title/Abstract] OR "exosomes"[Title/Abstract])',
        '("plant microRNA" AND "mammalian cells" AND ("delivery" OR "regulation" OR "cross-kingdom"))',
        '("small RNA loading"[Title/Abstract] AND "extracellular vesicles"[Title/Abstract] AND "plant"[All Fields])',
        '("plant mRNA" AND "extracellular vesicles" AND ("fungal" OR "mammalian" OR "cross-species"))',
    ],
    "03-engineering-delivery": [
        '("extracellular vesicles" AND "engineering" AND ("surface modification" OR "targeting" OR "drug loading")) AND ("cancer" OR "tumor")',
        '("oral delivery"[Title/Abstract] AND "nanoparticles"[Title/Abstract] AND ("exosome" OR "extracellular vesicle" OR "plant-derived"))',
        '("hybrid vesicles"[Title/Abstract] OR "membrane fusion"[Title/Abstract]) AND ("drug delivery"[Title/Abstract] OR "cancer"[Title/Abstract])',
        '("plant vesicles" AND ("loading" OR "electroporation" OR "sonication") AND ("siRNA" OR "miRNA" OR "drug"))',
    ],
    "04-cancer-applications": [
        '("extracellular vesicles" OR "exosomes") AND ("breast cancer" OR "glioma" OR "colorectal cancer" OR "lung cancer") AND ("plant-derived" OR "natural")',
        '("tumor microenvironment" AND "extracellular vesicles" AND ("reprogramming" OR "macrophage" OR "immune"))',
        '("cancer immunotherapy" AND "extracellular vesicles" AND ("checkpoint" OR "PD-L1" OR "immune"))',
    ],
    "05-clinical-translation": [
        '("extracellular vesicles" AND ("clinical trial" OR "scale-up" OR "manufacturing" OR "GMP")) AND ("2019"[Date - Publication] : "2026"[Date - Publication])',
        '("exosome therapeutics" AND ("FDA" OR "regulatory" OR "quality control" OR "standardization"))',
        '("plant-derived nanovesicles" AND ("safety" OR "toxicity" OR "biodistribution" OR "pharmacokinetics"))',
    ],
    "06-mammalian-evs-reference": [
        '("extracellular vesicles"[Title] OR "exosomes"[Title]) AND ("biogenesis"[Title/Abstract] OR "uptake"[Title/Abstract] OR "cargo sorting"[Title/Abstract]) AND review[Publication Type]',
        '("MISEV"[All Fields] OR "extracellular vesicle characterization"[Title] OR "EV isolation methods"[Title])',
    ],
    "07-rna-therapeutics": [
        '("RNA therapeutics"[Title/Abstract] OR "RNA delivery"[Title/Abstract] OR "siRNA delivery"[Title/Abstract]) AND ("nanoparticle"[Title/Abstract] OR "lipid nanoparticle"[Title/Abstract]) AND review[Publication Type]',
        '("mRNA vaccine" OR "mRNA therapeutic" OR "RNA interference therapy") AND ("delivery" OR "clinical") AND ("2020"[Date - Publication] : "2026"[Date - Publication])',
    ],
}


def search_pubmed(query, max_results=30, retmax=30):
    """Search PubMed via E-utilities API and return list of PMIDs."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    # Step 1: Search
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": str(retmax),
        "retmode": "json",
        "sort": "relevance",
    }
    search_url = f"{base_url}/esearch.fcgi?{urllib.parse.urlencode(search_params)}"

    try:
        with urllib.request.urlopen(search_url, timeout=30) as resp:
            data = json.loads(resp.read())
        pmids = data.get("esearchresult", {}).get("idlist", [])
        return pmids
    except Exception as e:
        print(f"  Search error: {e}")
        return []


def fetch_pubmed_details(pmids, batch_size=20):
    """Fetch article details from PubMed by PMIDs."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    all_articles = []

    for i in range(0, len(pmids), batch_size):
        batch = pmids[i:i + batch_size]
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(batch),
            "retmode": "xml",
        }
        fetch_url = f"{base_url}/efetch.fcgi?{urllib.parse.urlencode(fetch_params)}"

        try:
            with urllib.request.urlopen(fetch_url, timeout=30) as resp:
                xml_data = resp.read()

            root = ET.fromstring(xml_data)
            for article in root.findall(".//PubmedArticle"):
                try:
                    info = parse_article(article)
                    all_articles.append(info)
                except Exception:
                    pass

            time.sleep(0.35)  # Rate limiting (NCBI allows ~3/sec)
        except Exception as e:
            print(f"  Fetch error: {e}")
            time.sleep(1)

    return all_articles


def parse_article(article):
    """Parse a PubmedArticle XML element into a dict."""
    citation = article.find(".//Article")

    # Title
    title_el = citation.find(".//ArticleTitle")
    title = "".join(title_el.itertext()) if title_el is not None else ""

    # Authors
    authors = []
    for author in citation.findall(".//Author"):
        last = author.find("./LastName")
        init = author.find("./Initials")
        if last is not None and last.text:
            name = last.text
            if init is not None and init.text:
                name += " " + init.text
            authors.append(name)

    # Journal
    journal_el = citation.find(".//Journal/Title")
    journal = journal_el.text if journal_el is not None else ""

    # Year
    year_el = citation.find(".//PubDate/Year")
    if year_el is None:
        year_el = citation.find(".//PubDate/MedlineDate")
    year = year_el.text[:4] if year_el is not None and year_el.text else ""

    # Volume / Issue / Pages
    vol_el = citation.find(".//Journal/JournalIssue/Volume")
    iss_el = citation.find(".//Journal/JournalIssue/Issue")
    pages_el = citation.find(".//Pagination/MedlinePgn")

    volume = vol_el.text if vol_el is not None else ""
    issue = iss_el.text if iss_el is not None else ""
    pages = pages_el.text if pages_el is not None else ""

    # DOI
    doi = ""
    for eid in article.findall(".//ELocationID"):
        if eid.get("EIdType") == "doi" and eid.text:
            doi = eid.text

    # PMID
    pmid_el = article.find(".//PMID")
    pmid = pmid_el.text if pmid_el is not None else ""

    # Abstract
    abstract_el = citation.find(".//Abstract/AbstractText")
    abstract = "".join(abstract_el.itertext()) if abstract_el is not None else ""

    # Keywords
    keywords = []
    for kw in citation.findall(".//Keyword"):
        if kw.text:
            keywords.append(kw.text)

    return {
        "pmid": pmid,
        "title": title.strip(),
        "authors": authors,
        "journal": journal.strip(),
        "year": year,
        "volume": volume,
        "issue": issue,
        "pages": pages,
        "doi": doi,
        "abstract": abstract.strip()[:500],
        "keywords": keywords,
    }


def article_to_bibtex(article, cite_key):
    """Convert article dict to BibTeX entry."""
    authors_str = " and ".join(article["authors"][:10])
    if len(article["authors"]) > 10:
        authors_str += " and others"

    title = article["title"].replace("{", "").replace("}", "")
    title = title.replace("&", "\\&").replace("_", "\\_")

    journal = article["journal"].replace("&", "\\&")

    pages = article["pages"]
    if pages:
        pages = pages.replace("–", "--")

    bibtex = f"""@article{{{cite_key},
  author = {{{authors_str}}},
  title = {{{title}}},
  journal = {{{journal}}},
  year = {{{article['year']}}},
  volume = {{{article['volume']}}},
  number = {{{article['issue']}}},
  pages = {{{pages}}},
  doi = {{{article['doi']}}},
  pmid = {{{article['pmid']}}}
}}"""
    return bibtex


def generate_cite_key(article, existing_keys):
    """Generate a unique BibTeX citation key."""
    if article["authors"]:
        first_author = article["authors"][0].split()[-1]
    else:
        first_author = "Unknown"

    year = article["year"] or "0000"
    base_key = f"{first_author}{year}"

    # Handle duplicates
    key = base_key.lower()
    counter = 0
    while key in existing_keys:
        counter += 1
        key = f"{base_key}{chr(96 + counter)}".lower()

    existing_keys.add(key)
    return key


def search_and_save(topic_id, queries, max_results, output_dir, all_keys):
    """Search PubMed for a topic and save BibTeX results."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    bib_path = output_dir / "references.bib"
    json_path = output_dir / "papers.json"

    all_articles = []
    seen_pmids = set()

    for query in queries:
        print(f"  Query: {query[:80]}...")
        pmids = search_pubmed(query, max_results=max_results // len(queries))

        new_pmids = [p for p in pmids if p not in seen_pmids]
        seen_pmids.update(new_pmids)

        if new_pmids:
            articles = fetch_pubmed_details(new_pmids)
            for a in articles:
                if a["pmid"] not in [x["pmid"] for x in all_articles]:
                    all_articles.append(a)
            print(f"    Found {len(articles)} articles")

        time.sleep(0.5)

    print(f"\n  Total unique articles: {len(all_articles)}")

    # Write BibTeX
    with open(bib_path, "w", encoding="utf-8") as f:
        f.write(f"% ===== {topic_id} =====\n")
        f.write(f"% Papers found: {len(all_articles)}\n")
        f.write(f"% Search date: {time.strftime('%Y-%m-%d')}\n\n")

        for article in all_articles:
            cite_key = generate_cite_key(article, all_keys)
            bibtex = article_to_bibtex(article, cite_key)
            f.write(bibtex)
            f.write("\n\n")

    # Write JSON metadata (includes abstracts for local search)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    print(f"  Saved: {bib_path} ({len(all_articles)} entries)")
    print(f"  Saved: {json_path}")

    return all_articles


def main():
    parser = argparse.ArgumentParser(
        description="Search PubMed and build a BibTeX literature database"
    )
    parser.add_argument("--topic", "-t", help="Topic directory ID (e.g., 01-plant-evs-general)")
    parser.add_argument("--all-topics", action="store_true", help="Search all predefined topics")
    parser.add_argument("--max", type=int, default=30, help="Max results per topic")
    parser.add_argument("--query", "-q", help="Custom PubMed query")
    parser.add_argument("--output-dir", "-o", default="literature",
                        help="Output directory (default: literature/)")

    args = parser.parse_args()

    output_base = Path(args.output_dir)
    all_keys = set()

    if args.query:
        # Custom single query
        print(f"Custom search: {args.query}")
        articles = search_and_save(
            "custom", [args.query], args.max, output_base / "custom", all_keys
        )
        print(f"\nTotal: {len(articles)} papers")

    elif args.topic:
        topic_id = args.topic
        if topic_id not in TOPICS:
            print(f"Unknown topic: {topic_id}")
            print(f"Available topics: {list(TOPICS.keys())}")
            sys.exit(1)

        print(f"Searching: {topic_id}")
        queries = TOPICS[topic_id]
        search_and_save(topic_id, queries, args.max, output_base / topic_id, all_keys)

    elif args.all_topics:
        total = 0
        for topic_id, queries in TOPICS.items():
            print(f"\n{'='*60}")
            print(f"Topic: {topic_id}")
            print(f"{'='*60}")
            articles = search_and_save(topic_id, queries, args.max,
                                       output_base / topic_id, all_keys)
            total += len(articles)
            print(f"  Running total: {total} papers")

        # Write master index
        print(f"\n{'='*60}")
        print(f"ALL TOPICS COMPLETE: {total} total papers")
        print(f"{'='*60}")

        index_path = output_base / "README.md"
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(f"# Literature Database Index\n\n")
            f.write(f"> Auto-generated: {time.strftime('%Y-%m-%d')}\n")
            f.write(f"> Total papers: {total}\n\n")
            f.write("| Topic | Papers | Path |\n")
            f.write("|-------|--------|------|\n")
            for topic_id in TOPICS:
                topic_dir = output_base / topic_id
                bib = topic_dir / "references.bib"
                if bib.exists():
                    count = sum(1 for l in open(bib, encoding='utf-8')
                                if l.startswith('@article'))
                    f.write(f"| {topic_id} | {count} | {topic_dir}/ |\n")
            f.write(f"\n## Search Queries\n\n")
            for topic_id, queries in TOPICS.items():
                f.write(f"### {topic_id}\n")
                for q in queries:
                    f.write(f"- `{q[:120]}...`\n")
                f.write("\n")

        print(f"  Index: {index_path}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
