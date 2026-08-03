import asyncio
from playwright.async_api import async_playwright


async def main():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True)

        page = await browser.new_page()

        await page.goto(
    "https://example.com",
    wait_until="domcontentloaded",
    timeout=30000
)

        print("Title:", await page.title())

        print("URL:", page.url)

        await browser.close()


asyncio.run(main())