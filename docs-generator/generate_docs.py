#!/usr/bin/env python3
"""
Generate printable algorithm documentation for programming competitions.

Creates 6 PDF documents optimized for printing:
- algorithms_python.pdf (competition code only)
- algorithms_python_extra.pdf (includes dev tests)
- algorithms_cpp.pdf (competition code only)
- algorithms_cpp_extra.pdf (includes dev tests)
- algorithms_java.pdf (competition code only)
- algorithms_java_extra.pdf (includes dev tests)

Each document includes:
- Table of contents on first page
- Each algorithm starting on a new page
- Fixed-width fonts and competition-optimized formatting
- Comprehensive syntax highlighting
"""

import asyncio
import importlib.util
from pathlib import Path


class Algorithm:
    """Represents an algorithm with its metadata and content."""

    def __init__(self, name: str, filename: str, content: str, competition_content: str) -> None:
        self.name = name
        self.filename = filename
        self.content = content
        self.competition_content = competition_content  # Content up to competition barrier


class DocumentGenerator:
    """Generates printable algorithm documentation."""

    # Language-specific file extensions and comment styles
    LANGUAGE_CONFIG = {
        'python': {
            'extension': '.py',
            'comment_style': '#',
            'competition_barrier': "# Don't write tests below during competition.",
            'typing_marker': "# Don't use annotations during contest"
        },
        'cpp': {
            'extension': '.cpp',
            'comment_style': '//',
            'competition_barrier': "// Don't write tests below during competition.",
            'typing_marker': None
        },
        'java': {
            'extension': '.java',
            'comment_style': '//',
            'competition_barrier': "// Don't write tests below during competition.",
            'typing_marker': None
        }
    }

    def __init__(self, language: str, source_dir: Path, output_dir: Path):
        self.language = language
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.config = self.LANGUAGE_CONFIG[language]

    def extract_algorithms(self, include_dev_tests: bool = False) -> list[Algorithm]:
        """Extract algorithms from source directory."""
        algorithms = []
        pattern = f"*{self.config['extension']}"

        for file_path in sorted(self.source_dir.glob(pattern)):
            # Skip non-algorithm files
            if file_path.name.startswith('.') or file_path.name in ['CLAUDE.md', 'README.md']:
                continue

            algorithm_name = file_path.stem
            content = file_path.read_text(encoding='utf-8')

            # Extract competition content (up to barrier)
            competition_content = self._extract_competition_content(content)

            final_content = competition_content if not include_dev_tests else content

            algorithms.append(Algorithm(
                name=algorithm_name,
                filename=file_path.name,
                content=content,
                competition_content=final_content
            ))

        return algorithms

    def _extract_competition_content(self, content: str) -> str:
        """Extract content up to the competition barrier."""
        lines = content.splitlines()
        competition_lines = []

        for line in lines:
            if self.config['competition_barrier'] in line:
                break
            competition_lines.append(line)

        return '\n'.join(competition_lines)

    def generate_html(self, algorithms: list[Algorithm]) -> str:
        """Generate complete HTML document."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Algorithm Reference - {self.language.title()}</title>
    <style>
{self._generate_css()}
    </style>
</head>
<body>
    <!-- Table of Contents -->
    <div class="toc-page">
        <h1>Algorithm Reference - {self.language.title()}</h1>
        <div class="toc-content">
{self._generate_toc(algorithms)}
        </div>
    </div>

    <!-- Algorithm pages -->
{self._generate_algorithm_pages(algorithms)}
</body>
</html>"""

    def _generate_css(self) -> str:
        """Generate CSS for print optimization."""
        return """        body {
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 9pt;
            line-height: 1.2;
            margin: 0;
            padding: 0;
            color: #000;
            background: #fff;
        }

        @media print {
            @page {
                size: A4;
                margin: 0.5cm;
            }

            body {
                font-size: 9pt;
            }

            .toc-page {
                page-break-after: always;
                page-break-inside: avoid;
            }

            .blank-page {
                page-break-after: always;
                height: 100vh;
            }

            .algorithm-page {
                page-break-before: always;
            }

            .algorithm-page:last-child {
                page-break-after: auto;
                break-after: auto;
            }

            .no-break {
                page-break-inside: avoid;
            }

            /* Chrome print color preservation */
            * {
                -webkit-print-color-adjust: exact !important;
                color-adjust: exact !important;
                print-color-adjust: exact !important;
            }

            /* Print-optimized syntax highlighting with darker colors */
            .c { color: #408040 !important; font-style: italic !important; } /* Comment - dark green */
            .c1 { color: #408040 !important; font-style: italic !important; } /* Comment.Single */
            .cm { color: #408040 !important; font-style: italic !important; } /* Comment.Multiline */
            .cp { color: #805000 !important; } /* Comment.Preproc - dark orange */
            .cpf { color: #805000 !important; } /* Comment.PreprocFile - dark orange */
            .k { color: #000080 !important; font-weight: bold !important; } /* Keyword - dark blue */
            .kd { color: #000080 !important; font-weight: bold !important; } /* Keyword.Declaration */
            .kn { color: #000080 !important; font-weight: bold !important; } /* Keyword.Namespace */
            .kc { color: #000080 !important; font-weight: bold !important; } /* Keyword.Constant */
            .kt { color: #800040 !important; } /* Keyword.Type - dark magenta */
            .s { color: #800000 !important; } /* String - dark red */
            .sa { color: #800000 !important; } /* String.Affix */
            .sd { color: #800000 !important; font-style: italic !important; } /* String.Doc */
            .si { color: #800000 !important; font-weight: bold !important; } /* String.Interpol */
            .na { color: #606020 !important; } /* Name.Attribute - dark olive */
            .nf { color: #0000cc !important; font-weight: bold !important; } /* Name.Function - blue */
            .fm { color: #0000cc !important; font-weight: bold !important; } /* Name.Function.Magic */
            .nc { color: #660066 !important; font-weight: bold !important; } /* Name.Class - purple */
            .nn { color: #660066 !important; font-weight: bold !important; } /* Name.Namespace */
            .ne { color: #800000 !important; font-weight: bold !important; } /* Name.Exception */
            .nd { color: #660066 !important; } /* Name.Decorator */
            .nb { color: #006600 !important; font-weight: bold !important; } /* Name.Builtin - green */
            .bp { color: #006600 !important; font-weight: bold !important; } /* Name.Builtin.Pseudo */
            .o { color: #666666 !important; } /* Operator - dark gray */
            .ow { color: #660066 !important; font-weight: bold !important; } /* Operator.Word */
            .mi { color: #666666 !important; } /* Number.Integer */
            .mf { color: #666666 !important; } /* Number.Float */
            .n { color: #000000 !important; } /* Name - black */
            .p { color: #000000 !important; } /* Punctuation */
            .w { color: #888888 !important; } /* Text.Whitespace */
        }

        @media screen {
            body {
                max-width: 21cm;
                margin: 0 auto;
                padding: 2cm;
                background: #f5f5f5;
            }

            .toc-page, .blank-page, .algorithm-page {
                page-break-after: unset !important;
                page-break-before: unset !important;
                page-break-inside: unset !important;
                break-after: unset !important;
                break-before: unset !important;
                break-inside: unset !important;
            }
        }

        h1 {
            font-size: 14pt;
            margin: 0 0 0.5em 0;
            text-align: center;
            font-weight: bold;
        }

        h2 {
            font-size: 14pt;
            margin: 1.5em 0 0.5em 0;
            font-weight: bold;
            border-bottom: 1px solid #333;
            padding-bottom: 0.2em;
        }

        .toc-content {
            font-size: 9pt;
        }

        .toc-item {
            margin: 0.1em 0;
            padding: 0.05em 0;
            border-bottom: 1px dotted #ccc;
        }

        .toc-name {
            font-weight: bold;
        }

        .blank-page {
            /* Height set in print media query only */
        }

        .algorithm-header {
            margin-bottom: 1em;
        }

        .algorithm-filename {
            font-size: 9pt;
            color: #666;
            margin-bottom: 0.5em;
        }

        pre {
            margin: 0;
            padding: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: inherit;
            font-size: inherit;
            line-height: inherit;
        }

        code {
            font-family: inherit;
            font-size: inherit;
        }

        /* Syntax highlighting classes */
        .highlight { background: transparent; }
        .c { color: #408080; font-style: italic } /* Comment */
        .c1 { color: #408080; font-style: italic } /* Comment.Single */
        .cm { color: #408080; font-style: italic } /* Comment.Multiline */
        .cp { color: #BC7A00 } /* Comment.Preproc */
        .cpf { color: #BC7A00 } /* Comment.PreprocFile */
        .k { color: #008000; font-weight: bold } /* Keyword */
        .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
        .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
        .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
        .kt { color: #B00040 } /* Keyword.Type */
        .o { color: #666666 } /* Operator */
        .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
        .n { color: #000000 } /* Name */
        .na { color: #7D9029 } /* Name.Attribute */
        .nb { color: #008000 } /* Name.Builtin */
        .bp { color: #008000 } /* Name.Builtin.Pseudo */
        .nf { color: #0000FF } /* Name.Function */
        .fm { color: #0000FF } /* Name.Function.Magic */
        .nc { color: #0000FF; font-weight: bold } /* Name.Class */
        .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
        .ne { color: #D2413A; font-weight: bold } /* Name.Exception */
        .nd { color: #AA22FF } /* Name.Decorator */
        .s { color: #BA2121 } /* String */
        .sa { color: #BA2121 } /* String.Affix */
        .sd { color: #BA2121; font-style: italic } /* String.Doc */
        .si { color: #BB6688; font-weight: bold } /* String.Interpol */
        .mi { color: #666666 } /* Number.Integer */
        .mf { color: #666666 } /* Number.Float */
        .p { color: #000000 } /* Punctuation */
        .w { color: #bbbbbb } /* Text.Whitespace */"""

    def _generate_toc(self, algorithms: list[Algorithm]) -> str:
        """Generate table of contents."""
        toc_items = []

        for algorithm in algorithms:
            name_formatted = algorithm.name.replace('_', ' ').title()
            toc_items.append(f"""            <div class="toc-item">
                <span class="toc-name">{name_formatted}</span>
            </div>""")

        return '\n'.join(toc_items)

    def _generate_algorithm_pages(self, algorithms: list[Algorithm]) -> str:
        """Generate all algorithm pages."""
        pages = []

        for algorithm in algorithms:
            content = self._format_code(algorithm.competition_content)
            name_formatted = algorithm.name.replace('_', ' ').title()

            pages.append(f"""    <div class="algorithm-page">
        <div class="algorithm-header">
            <h2>{name_formatted}</h2>
            <div class="algorithm-filename">{algorithm.filename}</div>
        </div>
        <pre><code>{content}</code></pre>
    </div>""")

        return '\n'.join(pages)

    def _format_code(self, code: str) -> str:
        """Format code with syntax highlighting."""
        try:
            from pygments import highlight
            from pygments.lexers import get_lexer_by_name
            from pygments.formatters import HtmlFormatter

            lexer_name = {
                'python': 'python3',
                'cpp': 'cpp',
                'java': 'java'
            }[self.language]

            lexer = get_lexer_by_name(lexer_name)
            formatter = HtmlFormatter(nowrap=True, classprefix='')

            return highlight(code, lexer, formatter)
        except ImportError:
            # Fallback if pygments not available
            return self._escape_html(code)

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&#x27;'))

    async def generate_pdf(self, algorithms: list[Algorithm], output_file: Path) -> None:
        """Generate PDF documentation using Playwright."""
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            print("Error: playwright not available. Install with: uv pip install playwright")
            print("Then run: uv run playwright install")
            return

        # Generate HTML content
        html_content = self.generate_html(algorithms)

        # Create temporary HTML file
        temp_html = output_file.parent / f"temp_{output_file.stem}.html"
        temp_html.write_text(html_content, encoding='utf-8')

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()

                # Load the HTML file
                await page.goto(f"file://{temp_html.absolute()}")

                # Wait for content to be ready
                await page.wait_for_load_state('networkidle')

                # Generate PDF
                await page.pdf(
                    path=str(output_file),
                    format='A4',
                    margin={
                        'top': '0.5cm',
                        'bottom': '0.5cm',
                        'left': '0.5cm',
                        'right': '0.5cm'
                    },
                    print_background=True,
                    prefer_css_page_size=True
                )

                await browser.close()

        finally:
            # Clean up temporary file
            if temp_html.exists():
                temp_html.unlink()


async def generate_documentation(generator: DocumentGenerator, algorithms_basic: list[Algorithm],
                                 algorithms_extra: list[Algorithm], language: str, output_dir: Path) -> tuple[str, list[Path], int]:
    """Generate PDF documentation for a single language (both basic and extra versions)."""
    output_file_basic = output_dir / f"algorithms_{language}.pdf"
    output_file_extra = output_dir / f"algorithms_{language}_extra.pdf"

    await generator.generate_pdf(algorithms_basic, output_file_basic)
    await generator.generate_pdf(algorithms_extra, output_file_extra)

    return language, [output_file_basic, output_file_extra], len(algorithms_basic)


async def main():
    """Main entry point."""
    # Setup paths
    output_dir = Path('./output')
    output_dir.mkdir(exist_ok=True)

    # Always generate for all languages
    languages = ['python', 'cpp', 'java']
    results = []

    for language in languages:
        source_dir = Path('..') / language
        if not source_dir.exists():
            print(f"Warning: Source directory '{source_dir}' not found, skipping {language}")
            continue

        # Generate documentation
        generator = DocumentGenerator(language, source_dir, output_dir)
        algorithms_basic = generator.extract_algorithms(include_dev_tests=False)
        algorithms_extra = generator.extract_algorithms(include_dev_tests=True)

        if not algorithms_basic:
            print(f"Warning: No algorithm files found in '{source_dir}', skipping {language}")
            continue

        # Generate PDF documentation (both basic and extra)
        result = await generate_documentation(generator, algorithms_basic, algorithms_extra, language, output_dir)
        results.append(result)

    # Print summary
    if results:
        print(f"Generated documentation for {len(results)} languages:")
        for language, output_files, count in results:
            for output_file in output_files:
                suffix = "_extra" if "_extra" in output_file.name else ""
                test_type = "with dev tests" if suffix else "competition only"
                print(f"  {language}{suffix}: {output_file} ({count} algorithms, {test_type})")
    else:
        print("No documentation generated")
        return 1

    if importlib.util.find_spec("pygments") is not None:
        print("Syntax highlighting: enabled")
    else:
        print("Syntax highlighting: disabled (pygments not available)")

    return 0


if __name__ == '__main__':
    exit(asyncio.run(main()))