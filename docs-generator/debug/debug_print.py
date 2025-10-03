#!/usr/bin/env python3
"""
Debug script for testing print preview and CSS rendering issues using Playwright.
This allows programmatic testing of browser behavior with generated HTML documents.
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright


async def debug_print_preview(html_file: Path, output_dir: Path = None):
    """Debug print preview behavior for generated HTML documents."""
    if output_dir is None:
        output_dir = Path("debug_output")
    output_dir.mkdir(exist_ok=True)

    async with async_playwright() as p:
        # Test in multiple browsers
        browsers = [
            ("chromium", p.chromium),
            ("firefox", p.firefox),
            ("webkit", p.webkit)
        ]

        for browser_name, browser_type in browsers:
            print(f"\n=== Testing {browser_name.upper()} ===")

            browser = await browser_type.launch()
            page = await browser.new_page()

            # Load the HTML file
            html_path = html_file.absolute()
            await page.goto(f"file://{html_path}")

            print(f"✓ Loaded: {html_file.name}")

            # Test screen rendering
            screen_path = output_dir / f"{browser_name}_screen.png"
            await page.screenshot(path=screen_path, full_page=True)
            print(f"✓ Screen screenshot: {screen_path}")

            # Test print media emulation
            await page.emulate_media(media="print")
            print("✓ Switched to print media")

            # Screenshot of print view
            print_path = output_dir / f"{browser_name}_print.png"
            await page.screenshot(path=print_path, full_page=True)
            print(f"✓ Print screenshot: {print_path}")

            # Generate PDF (Chrome/Chromium only)
            if browser_name == "chromium":
                pdf_path = output_dir / f"{browser_name}_print.pdf"
                await page.pdf(path=pdf_path, format="A4", print_background=True)
                print(f"✓ PDF generated: {pdf_path}")

            # Check for syntax highlighting elements
            highlight_elements = await page.query_selector_all(".highlight")
            print(f"✓ Found {len(highlight_elements)} syntax highlight elements")

            # Check page break elements
            algorithm_pages = await page.query_selector_all(".algorithm-page")
            print(f"✓ Found {len(algorithm_pages)} algorithm pages")

            # Get computed styles for debugging
            if highlight_elements:
                first_highlight = highlight_elements[0]
                styles = await page.evaluate("""
                    element => {
                        const computed = window.getComputedStyle(element);
                        return {
                            color: computed.color,
                            fontWeight: computed.fontWeight,
                            fontStyle: computed.fontStyle,
                            textDecoration: computed.textDecoration,
                            opacity: computed.opacity
                        };
                    }
                """, first_highlight)
                print(f"✓ First highlight element styles: {styles}")

            await browser.close()


async def debug_css_properties(html_file: Path):
    """Debug specific CSS properties and their computed values."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        html_path = html_file.absolute()
        await page.goto(f"file://{html_path}")

        print("\n=== CSS DEBUG INFO ===")

        # Check print media CSS
        await page.emulate_media(media="print")

        # Debug page break properties
        algorithm_pages = await page.query_selector_all(".algorithm-page")
        if algorithm_pages:
            styles = await page.evaluate("""
                elements => elements.map(el => {
                    const computed = window.getComputedStyle(el);
                    return {
                        pageBreakBefore: computed.pageBreakBefore,
                        breakBefore: computed.breakBefore,
                        pageBreakAfter: computed.pageBreakAfter,
                        breakAfter: computed.breakAfter
                    };
                })
            """, algorithm_pages[:3])  # Check first 3 elements

            for i, style in enumerate(styles):
                print(f"Algorithm page {i+1}: {style}")

        # Debug syntax highlighting CSS
        highlight_selectors = [
            ".highlight .k",  # Keywords
            ".highlight .s",  # Strings
            ".highlight .c",  # Comments
            ".highlight .nf", # Functions
        ]

        for selector in highlight_selectors:
            elements = await page.query_selector_all(selector)
            if elements:
                style = await page.evaluate("""
                    element => {
                        const computed = window.getComputedStyle(element);
                        return {
                            color: computed.color,
                            fontWeight: computed.fontWeight,
                            fontStyle: computed.fontStyle,
                            textDecoration: computed.textDecoration,
                            opacity: computed.opacity
                        };
                    }
                """, elements[0])
                print(f"{selector}: {style}")

        await browser.close()


async def main():
    """Main debug function."""
    # Look for generated HTML files
    output_dir = Path("output")
    html_files = list(output_dir.glob("algorithms_*.html"))

    if not html_files:
        print("No HTML files found in output directory. Generate some first:")
        print("  ./update_docs.sh")
        return

    # Test the first HTML file found
    html_file = html_files[0]
    print(f"Debugging: {html_file}")

    await debug_print_preview(html_file)
    await debug_css_properties(html_file)

    print("\n=== DEBUG COMPLETE ===")
    print("Check debug_output/ directory for screenshots and PDFs")
    print("Compare screen vs print screenshots to see differences")


if __name__ == "__main__":
    asyncio.run(main())