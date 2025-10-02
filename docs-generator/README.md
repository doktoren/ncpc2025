# Algorithm Documentation Generator

This tool generates printable HTML documents containing source code for algorithms optimized for programming competitions. It creates clean, fixed-width formatted documents suitable for printing and reference during contests.

## Usage

To see all available options:

```bash
uv run --python 3.13 generate_docs.py --help
```

Basic usage:
```bash
# Generate docs for Python algorithms (with syntax highlighting)
uv run --python 3.13 --with pygments generate_docs.py python

# Generate docs for all languages
uv run --python 3.13 --with pygments generate_docs.py all

# Include development tests (normally excluded)
uv run --python 3.13 --with pygments generate_docs.py python --include-dev-tests
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

### 2. Comprehensive Syntax Highlighting ✅ RESOLVED

**Problem**: Limited syntax highlighting coverage, especially for C++ and Java languages.

**Solution Implemented**:
- **Complete Pygments class coverage**: Added CSS for all language-specific syntax elements
- **C++ improvements**: Keywords, types (`int`, `string`), preprocessor directives (`#include`), multiline comments
- **Java improvements**: Declarations (`public`, `static`), types (`String`, `List`), annotations, attributes
- **Consistent color scheme**: Different colors for keywords, types, comments, functions, strings, numbers

**Current Status**: **Resolved** - All three languages now have comprehensive syntax highlighting with 1000+ highlighted elements per language.

**Current Behavior**: Rich color highlighting works in browser view with language-specific syntax elements properly colored.

### 3. Chrome Print Color Support ✅ RESOLVED

**Problem**: Chrome strips colors when printing to save ink, making syntax highlighting invisible in print preview and printed output.

**Solution Implemented**:
- Applied `-webkit-print-color-adjust: exact`, `color-adjust: exact`, and `print-color-adjust: exact` CSS properties
- Used darker, print-friendly colors that work better in print mode
- Added print-specific color overrides with `!important` declarations

**Current Status**: **Resolved** - Syntax highlighting colors now appear when printing from Chrome, provided the user enables "Background graphics" in print settings or generates PDFs programmatically with `print_background=True`.

**Current Behavior**: Syntax highlighting works in both browser view and print output. Users need to enable "More settings" → "Options" → "Background graphics" in Chrome's print dialog for colors to appear in printed output.

### 4. CSS Print Media Limitations ⚠️ ONGOING

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
- ✅ **Syntax highlighting always enabled** with print-friendly colors
- ✅ Support for all languages or individual language selection
- ✅ Configurable output directory
- ✅ Clean page breaks between algorithms
- ✅ Responsive design (works in browser and print)
- ✅ **Chrome print color support** (requires "Background graphics" setting)

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

## Debugging Tools

For debugging print preview and CSS rendering issues, use the included Playwright-based tools:

### Setup
```bash
# Install debugging dependencies
uv pip install -r debug/requirements-debug.txt

# Install browser binaries (one time setup)
uv run playwright install
```

### Automated Testing
```bash
# Generate screenshots and PDFs across browsers
uv run --python 3.13 debug/debug_print.py

# Check debug_output/ for:
# - *_screen.png (normal browser view)
# - *_print.png (print media emulation)
# - chromium_print.pdf (actual PDF output)
```

### Interactive Debugging
```bash
# Open browsers manually for inspection
uv run --python 3.13 debug/debug_interactive.py

# Compare rendering across Chrome, Firefox, Safari
# Test print dialogs and CSS media queries
```

### What the Debug Tools Show
- **CSS computed values** for syntax highlighting elements
- **Page break properties** and their actual behavior
- **Visual differences** between screen and print media
- **Cross-browser comparison** of rendering

## Technical Notes

- **Python 3.13 compatibility**: Updated to use modern Python syntax (`list[T]` instead of `List[T]`)
- **Ruff linting**: Passes all linting checks with Python 3.13
- **Comprehensive syntax highlighting**: Complete Pygments coverage for Python, C++, and Java with 1000+ elements per language
- **Print color support**: Uses `-webkit-print-color-adjust: exact` and darker colors for print compatibility
- **Language-specific highlighting**: Types, declarations, preprocessor directives, annotations properly colored
- **Competition barriers**: Respects existing comment markers to exclude development tests
- **Cross-language consistency**: Maintains same structure and functionality across Python, C++, and Java
- **Playwright debugging**: Automated and interactive tools for testing print behavior across browsers