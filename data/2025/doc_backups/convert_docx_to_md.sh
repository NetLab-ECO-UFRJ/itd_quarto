#!/bin/bash

set -e

MARKDOWN_DIR="markdown"

mkdir -p "$MARKDOWN_DIR"

for docx_file in *.docx; do
    if [ -f "$docx_file" ]; then
        base_name="${docx_file%.docx}"
        md_file="${MARKDOWN_DIR}/${base_name}.md"

        echo "Converting $docx_file to $md_file..."
        pandoc "$docx_file" -o "$md_file"

        echo "Converted: $docx_file -> $md_file"
    fi
done

echo "All DOCX files have been converted to Markdown in the '$MARKDOWN_DIR' folder."
