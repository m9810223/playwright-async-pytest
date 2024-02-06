import typing as t

import pytest
from playwright.async_api import Browser
from playwright.async_api import BrowserContext
from playwright.async_api import BrowserType
from playwright.async_api import Page
from playwright.async_api import Playwright
from playwright.async_api import async_playwright


URL = 'https://playwright.dev/'
TITLE = 'Fast and reliable end-to-end testing for modern web apps | Playwright'


@pytest.mark.asyncio
async def test_async_playwright():
    async with async_playwright() as playwright:
        async with await playwright.chromium.launch() as browser:
            async with await browser.new_context() as context:
                async with await context.new_page() as page:
                    await page.goto(URL, wait_until='networkidle')
                    assert await page.title() == TITLE


@pytest.mark.asyncio
async def test_my_app_is_working(  # https://playwright.dev/python/docs/test-runners#fixtures
    playwright_async: Playwright,
    browser_async: Browser,
    browser_name: str,
    browser_channel: t.Optional[str],
    context_async: BrowserContext,
    browser_context_args_async: dict,
    page_async: Page,
):
    print(f"\n{playwright_async = }")
    assert type(playwright_async) == Playwright

    print(f"\n{browser_async = }")
    assert type(browser_async) == Browser

    print(f"\n{browser_name = }")

    print(f"\n{browser_channel = }")

    print(f"\n{context_async = }")
    assert type(context_async) == BrowserContext

    print(f"\n{browser_context_args_async = }")

    print(f"\n{page_async = }")
    assert type(page_async) == Page


@pytest.mark.asyncio
async def test_browser_type_launch_args_async(browser_type_launch_args_async: t.Dict):
    print(f"\n{browser_type_launch_args_async, type(browser_type_launch_args_async) = }")
    async with async_playwright() as playwright:
        async with await playwright.chromium.launch(**browser_type_launch_args_async) as browser:
            async with await browser.new_context() as context:
                async with await context.new_page() as page:
                    await page.goto(URL, wait_until='networkidle')
                    assert await page.title() == TITLE


@pytest.mark.asyncio
async def test_browser_context_args_async(browser_context_args_async: t.Dict):
    print(f"\n{browser_context_args_async, type(browser_context_args_async) = }")
    async with async_playwright() as playwright:
        async with await playwright.chromium.launch() as browser:
            async with await browser.new_context(**browser_context_args_async) as context:
                async with await context.new_page() as page:
                    await page.goto(URL, wait_until='networkidle')
                    assert await page.title() == TITLE


@pytest.mark.asyncio
async def test_playwright_async(playwright_async: Playwright):
    print(f"\n{playwright_async, type(playwright_async) = }")
    async with await playwright_async.chromium.launch() as browser:
        async with await browser.new_context() as context:
            async with await context.new_page() as page:
                await page.goto(URL, wait_until='networkidle')
                assert await page.title() == TITLE


@pytest.mark.asyncio
async def test_browser_type_async(browser_type_async: BrowserType):
    print(f"\n{browser_type_async, type(browser_type_async) = }")
    async with await browser_type_async.launch() as browser:
        async with await browser.new_context() as context:
            async with await context.new_page() as page:
                await page.goto(URL, wait_until='networkidle')
                assert await page.title() == TITLE


@pytest.mark.asyncio
async def test_launch_browser_async(launch_browser_async: t.Callable[..., t.Awaitable[Browser]]):
    print(f"\n{launch_browser_async, type(launch_browser_async) = }")
    browser = await launch_browser_async()
    async with await browser.new_context() as context:
        async with await context.new_page() as page:
            await page.goto(URL, wait_until='networkidle')
            assert await page.title() == TITLE


@pytest.mark.asyncio
async def test_browser_async(browser_async: Browser):
    print(f"\n{browser_async, type(browser_async) = }")
    async with await browser_async.new_context() as context:
        async with await context.new_page() as page:
            await page.goto(URL, wait_until='networkidle')
            assert await page.title() == TITLE


@pytest.mark.asyncio
async def test_context_async(context_async: BrowserContext):
    print(f"\n{context_async = }")
    async with await context_async.new_page() as page:
        await page.goto(URL, wait_until='networkidle')
        assert await page.title() == TITLE


@pytest.mark.asyncio
async def test_page_async(page_async: Page):
    print(f"\n{page_async = }")
    await page_async.goto(URL, wait_until='networkidle')
    assert await page_async.title() == TITLE
