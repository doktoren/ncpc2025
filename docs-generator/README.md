# Algorithm Documentation Generator

This tool generates printable PDF documents containing source code for algorithms optimized for programming competitions. It creates clean, fixed-width formatted documents with comprehensive syntax highlighting suitable for printing and reference during contests.

## Usage

The script automatically generates 6 PDF documents (3 languages × 2 versions each):
- `algorithms_python.pdf` / `algorithms_python_extra.pdf`
- `algorithms_cpp.pdf` / `algorithms_cpp_extra.pdf`
- `algorithms_java.pdf` / `algorithms_java_extra.pdf`

Basic usage:
```bash
# Generate all PDF documentation (6 files total)
python3 generate_docs.py

# Or use the uv wrapper script (recommended)
../update_docs.sh
```

The script processes algorithm files from the parent directory's `python/`, `cpp/`, and `java/` folders and generates PDF documents in the `output/` directory. No arguments are needed - it always generates all combinations.

## Implementation Details

### 1. Comprehensive Syntax Highlighting ✅ IMPLEMENTED

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

- ✅ **PDF generation** for Python, C++, and Java algorithms using Playwright
- ✅ Table of contents on first page
- ✅ Fixed-width fonts optimized for code display
- ✅ Extracts only competition-relevant code (stops at competition barriers)
- ✅ **Comprehensive syntax highlighting** with print-friendly colors
- ✅ Support for all languages or individual language selection
- ✅ Configurable output directory
- ✅ Clean page breaks between algorithms
- ✅ **Print-optimized PDF output** with proper colors and formatting

## Future Todos

### High Priority
1. **Browser-specific print guides**: Document optimal print settings for different browsers
2. **Print preview testing**: Systematic testing across Chrome, Firefox, Safari, and Edge
3. **Enhanced print styling**: Improve readability with better font sizing and spacing

### Medium Priority
4. **Page numbering**: Add optional page numbers to generated documents
5. **Algorithm categorization**: Group algorithms by type (data structures, graphs, etc.) in TOC

### Low Priority
6. **Custom CSS themes**: Allow users to specify custom CSS for different printing preferences
7. **Batch processing**: Support processing multiple algorithm directories simultaneously
8. **Integration with build tools**: Add makefile or script integration for automated documentation generation

## Debugging Tools

For debugging print preview and CSS rendering issues, use the included Playwright-based tools. The same Playwright setup is used for PDF generation:

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