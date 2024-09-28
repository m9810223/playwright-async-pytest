from playwright.async_api import Page


async def test_page_async(page_async: Page):
    print(f'\n{page_async = }')
    await page_async.goto('https://playwright.dev/')
    assert 'Playwright' in await page_async.title()
