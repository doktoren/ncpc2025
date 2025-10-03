#!/usr/bin/env python3
"""
Interactive debugging script for manual testing with Playwright.
Opens browsers with generated HTML for manual inspection.
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright


async def interactive_debug(html_file: Path, browser_name: str = "chromium"):
    """Open browser interactively for manual debugging."""
    async with async_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = await browser_type.launch(headless=False, slow_mo=1000)

        context = await browser.new_context()
        page = await context.new_page()

        # Load the HTML file
        html_path = html_file.absolute()
        await page.goto(f"file://{html_path}")

        print(f"Opened {html_file.name} in {browser_name}")
        print("Browser window is open for manual inspection.")
        print("\nUseful commands to test in browser console:")
        print("  window.print()  // Open print dialog")
        print("  document.querySelector('.highlight').style  // Check highlight styles")
        print("\nPress Enter to continue or Ctrl+C to exit...")

        try:
            input()  # Wait for user input

            # Switch to print media for comparison
            await page.emulate_media(media="print")
            print("Switched to print media. Check the visual changes.")
            print("Press Enter to close...")
            input()

        except KeyboardInterrupt:
            print("\nClosing browser...")

        await browser.close()


async def compare_browsers(html_file: Path):
    """Open the same HTML file in multiple browsers for comparison."""
    async with async_playwright() as p:
        browsers = []

        # Launch all browsers
        for browser_name in ["chromium", "firefox", "webkit"]:
            try:
                browser_type = getattr(p, browser_name)
                browser = await browser_type.launch(headless=False)
                context = await browser.new_context()
                page = await context.new_page()

                html_path = html_file.absolute()
                await page.goto(f"file://{html_path}")

                browsers.append((browser_name, browser))
                print(f"✓ Opened in {browser_name}")

            except Exception as e:
                print(f"✗ Failed to open {browser_name}: {e}")

        if browsers:
            print(f"\nOpened {html_file.name} in {len(browsers)} browsers")
            print("Compare rendering differences manually.")
            print("Press Enter to close all browsers...")

            try:
                input()
            except KeyboardInterrupt:
                pass

            # Close all browsers
            for browser_name, browser in browsers:
                await browser.close()
                print(f"Closed {browser_name}")


def main():
    """Main interactive function."""
    # Look for generated HTML files
    output_dir = Path("output")
    html_files = list(output_dir.glob("algorithms_*.html"))

    if not html_files:
        print("No HTML files found in output directory. Generate some first:")
        print("  ./update_docs.sh")
        return

    print("Available HTML files:")
    for i, file in enumerate(html_files):
        print(f"  {i+1}. {file.name}")

    try:
        choice = int(input(f"\nSelect file (1-{len(html_files)}): ")) - 1
        if choice < 0 or choice >= len(html_files):
            print("Invalid choice")
            return
    except (ValueError, KeyboardInterrupt):
        print("Cancelled")
        return

    html_file = html_files[choice]

    print("\nDebugging options:")
    print("1. Single browser (interactive)")
    print("2. Compare multiple browsers")

    try:
        option = input("Choose option (1 or 2): ")
    except KeyboardInterrupt:
        print("Cancelled")
        return

    if option == "1":
        browser = input("Browser (chromium/firefox/webkit) [chromium]: ").strip() or "chromium"
        asyncio.run(interactive_debug(html_file, browser))
    elif option == "2":
        asyncio.run(compare_browsers(html_file))
    else:
        print("Invalid option")


if __name__ == "__main__":
    main()