#!/bin/bash
# Merge all topic BibTeX files into a master literature database
# Usage: bash scripts/merge_literature.sh

OUTPUT="literature/master.bib"
TOPIC_DIR="literature"

echo "% ==========================================" > "$OUTPUT"
echo "% Master Literature Database" >> "$OUTPUT"
echo "% Plant Exosome RNA Cancer Therapy Review" >> "$OUTPUT"
echo "% Merged: $(date '+%Y-%m-%d %H:%M:%S')" >> "$OUTPUT"
echo "% ==========================================" >> "$OUTPUT"
echo "" >> "$OUTPUT"

TOTAL=0

for dir in "$TOPIC_DIR"/*/; do
    topic=$(basename "$dir")
    bib_file="$dir/references.bib"

    if [ -f "$bib_file" ]; then
        count=$(grep -c '^@article' "$bib_file" 2>/dev/null || echo 0)
        echo "% ----- $topic ($count papers) -----" >> "$OUTPUT"
        echo "" >> "$OUTPUT"
        cat "$bib_file" >> "$OUTPUT"
        echo "" >> "$OUTPUT"
        TOTAL=$((TOTAL + count))
        echo "  + $topic: $count papers"
    fi
done

# Also include the manuscript's own references
if [ -f "references/references.bib" ]; then
    count=$(grep -c '^@article' "references/references.bib" 2>/dev/null || echo 0)
    echo "% ----- manuscript references ($count papers) -----" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
    cat "references/references.bib" >> "$OUTPUT"
    TOTAL=$((TOTAL + count))
    echo "  + manuscript references: $count papers"
fi

echo ""
echo "==================================="
echo "Total papers merged: $TOTAL"
echo "Output: $OUTPUT"
echo "==================================="
