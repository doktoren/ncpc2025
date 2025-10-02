#!/bin/bash
set -e

echo "Updating algorithm documentation..."
echo "This will generate 6 PDF files (3 languages × 2 versions each)"
echo ""

cd docs-generator

# Run the documentation generator with proper dependencies
uv run --python 3.13 --with pygments --with playwright python3 generate_docs.py

echo ""
echo "Documentation update complete!"
echo "Generated files in docs-generator/output/:"
ls -la output/*.pdf | awk '{print "  " $9 " (" $5 " bytes)"}'