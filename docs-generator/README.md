# Algorithm Documentation Generator

This tool generates printable HTML documents containing source code for algorithms optimized for programming competitions. It creates clean, fixed-width formatted documents suitable for printing and reference during contests.

## Usage

To see all available options:

```bash
uv run --python 3.13 generate_docs.py --help
```

Basic usage:
```bash
# Generate docs for Python algorithms
uv run --python 3.13 generate_docs.py python

# Generate docs for all languages
uv run --python 3.13 generate_docs.py all

# Include syntax highlighting (requires pygments)
uv run --python 3.13 --with pygments generate_docs.py python --syntax-highlighting

# Include development tests (normally excluded)
uv run --python 3.13 generate_docs.py python --include-dev-tests
```

The script processes algorithm files from the parent directory's `python/`, `cpp/`, and `java/` folders and generates HTML documents in the `output/` directory.

## Problems Encountered and Current Status

### 1. Odd Page Alignment Issue ❌ UNRESOLVED

**Problem**: The original requirement was for each algorithm to start on an odd page (right-hand side) for double-sided printing, which would automatically insert blank pages when needed.

**Attempts Made**:
- Used CSS `page-break-before: right` and `break-before: right` properties
- Tried both legacy and modern CSS page break properties
- Implemented manual page counting with explicit spacer pages
- Added various CSS workarounds and browser-specific properties

**Current Status**: The CSS `page-break-before: right` property has inconsistent browser support. Chrome and Firefox do not reliably implement this feature for forcing content to start on odd pages. The feature has been **removed** from the current implementation.

**Current Behavior**: Each algorithm starts on a new page (using `page-break-before: always`) but not necessarily an odd page.

### 2. Chrome Print Color Stripping ❌ UNRESOLVED

**Problem**: Chrome strips colors when printing to save ink, making syntax highlighting invisible in print preview and printed output.

**Attempts Made**:
- Used `color-adjust: exact` and `-webkit-print-color-adjust: exact` properties
- Moved color CSS into print media queries with `!important` declarations
- Implemented print-friendly alternatives using text styling (bold, italic, underline, opacity)

**Current Status**: **Unresolved** - Chrome continues to strip both colors and text styling effects when printing. The print-friendly alternatives (bold, italic, underline) are also ignored or rendered inconsistently in Chrome's print output.

**Current Behavior**: Syntax highlighting works in browser view (colors) but is effectively invisible when printing from Chrome. Text styling alternatives are also not reliably rendered in print output.

### 3. CSS Print Media Limitations ⚠️ ONGOING

**Problem**: Web browsers have inconsistent implementation of CSS print properties, making reliable print formatting challenging.

**Current Status**: Using basic, well-supported CSS properties:
- `page-break-before: always` for new pages
- `page-break-inside: avoid` for keeping content together
- Fixed-width fonts and consistent sizing
- Conditional print styling only when syntax highlighting is requested

## Current Features ✅

- ✅ Generates HTML documents for Python, C++, and Java algorithms
- ✅ Table of contents on first page
- ✅ Fixed-width fonts optimized for code display
- ✅ Extracts only competition-relevant code (stops at competition barriers)
- ✅ Optional syntax highlighting with print-friendly fallbacks
- ✅ Support for all languages or individual language selection
- ✅ Configurable output directory
- ✅ Clean page breaks between algorithms
- ✅ Responsive design (works in browser and print)

## Future Todos

### High Priority
1. **Investigate alternative document formats**: Consider generating PDF directly using libraries like `weasyprint` or `reportlab` which may have better page control than HTML/CSS print
2. **Browser-specific print guides**: Document optimal print settings for different browsers
3. **Print preview testing**: Systematic testing across Chrome, Firefox, Safari, and Edge

### Medium Priority
4. **Enhanced print styling**: Improve readability with better font sizing and spacing
5. **Page numbering**: Add optional page numbers to generated documents
6. **Algorithm categorization**: Group algorithms by type (data structures, graphs, etc.) in TOC

### Low Priority
7. **Custom CSS themes**: Allow users to specify custom CSS for different printing preferences
8. **Batch processing**: Support processing multiple algorithm directories simultaneously
9. **Integration with build tools**: Add makefile or script integration for automated documentation generation

## Technical Notes

- **Python 3.13 compatibility**: Updated to use modern Python syntax (`list[T]` instead of `List[T]`)
- **Ruff linting**: Passes all linting checks with Python 3.13
- **Conditional styling**: Print-specific CSS only added when syntax highlighting is enabled
- **Competition barriers**: Respects existing comment markers to exclude development tests
- **Cross-language consistency**: Maintains same structure and functionality across Python, C++, and Java