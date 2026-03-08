"""
Automated screenshot capture for FastAPI assignment.
Run this AFTER starting the server: uvicorn main:app --reload
"""
import asyncio
import sys

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Playwright not installed. Run: pip install playwright")
    print("Then run: playwright install chromium")
    sys.exit(1)


BASE_URL = "http://127.0.0.1:8000"

# 3 endpoints to screenshot (customize as needed)
URLS = [
    ("/products", "screenshot_1_products.png"),
    ("/products/category/Electronics", "screenshot_2_category.png"),
    ("/store/summary", "screenshot_3_store_summary.png"),
]


async def capture_screenshots():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})

        for path, filename in URLS:
            url = BASE_URL + path
            try:
                await page.goto(url, wait_until="networkidle")
                await page.screenshot(path=filename)
                print(f"OK Saved: {filename}")
            except Exception as e:
                print(f"Failed {path}: {e}")
                print("  Make sure the server is running: uvicorn main:app --reload")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(capture_screenshots())
    print("\nDone! Check the PNG files in this folder.")
