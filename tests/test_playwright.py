import typing as t

from playwright.async_api import Browser
from playwright.async_api import BrowserContext
from playwright.async_api import BrowserType
from playwright.async_api import Page
from playwright.async_api import Playwright
from playwright.async_api import async_playwright
import pytest


URL = 'https://playwright.dev/'


def check_title(title):
    assert 'Playwright' in title


@pytest.mark.asyncio
async def test_async_playwright():
    async with async_playwright() as playwright:
        async with await playwright.chromium.launch() as browser:
            async with await browser.new_context() as context:
                async with await context.new_page() as page:
                    await page.goto(URL)
                    check_title(await page.title())


# https://playwright.dev/python/docs/test-runners#fixtures


@pytest.mark.asyncio
async def test_is_working_playwright_async(playwright_async: Playwright):
    print(f'\n{playwright_async = }')
    assert type(playwright_async) == Playwright


@pytest.mark.asyncio
async def test_is_working_browser_async(browser_async: Browser):
    print(f'\n{browser_async = }')
    assert type(browser_async) == Browser


@pytest.mark.asyncio
async def test_is_working_browser_name(browser_name: str):
    print(f'\n{browser_name = }')
    assert isinstance(browser_name, str)


@pytest.mark.asyncio
async def test_is_working_browser_channel(browser_channel: t.Optional[str]):
    print(f'\n{browser_channel = }')
    assert isinstance(browser_channel, str) or browser_channel is None


@pytest.mark.asyncio
async def test_is_working_context_async(context_async: BrowserContext):
    print(f'\n{context_async = }')
    assert type(context_async) == BrowserContext


@pytest.mark.asyncio
async def test_is_working_browser_context_args_async(browser_context_args_async: dict):
    print(f'\n{browser_context_args_async = }')
    assert isinstance(browser_context_args_async, dict)


@pytest.mark.asyncio
async def test_is_working_page_async(page_async: Page):
    print(f'\n{page_async = }')
    assert type(page_async) == Page


###


@pytest.mark.asyncio
async def test_browser_context_args_async(browser_context_args_async: t.Dict):
    print(f'\n{browser_context_args_async, type(browser_context_args_async) = }')
    async with async_playwright() as playwright:
        async with await playwright.chromium.launch() as browser:
            async with await browser.new_context(**browser_context_args_async) as context:
                async with await context.new_page() as page:
                    await page.goto(URL)
                    check_title(await page.title())


@pytest.mark.asyncio
async def test_playwright_async(playwright_async: Playwright):
    print(f'\n{playwright_async, type(playwright_async) = }')
    async with await playwright_async.chromium.launch() as browser:
        async with await browser.new_context() as context:
            async with await context.new_page() as page:
                await page.goto(URL)
                check_title(await page.title())


@pytest.mark.asyncio
async def test_browser_type_async(browser_type_async: BrowserType):
    print(f'\n{browser_type_async, type(browser_type_async) = }')
    async with await browser_type_async.launch() as browser:
        async with await browser.new_context() as context:
            async with await context.new_page() as page:
                await page.goto(URL)
                check_title(await page.title())


@pytest.mark.asyncio
async def test_launch_browser_async(launch_browser_async: t.Callable[..., t.Awaitable[Browser]]):
    print(f'\n{launch_browser_async, type(launch_browser_async) = }')
    browser = await launch_browser_async()
    async with await browser.new_context() as context:
        async with await context.new_page() as page:
            await page.goto(URL)
            check_title(await page.title())


@pytest.mark.asyncio
async def test_browser_async(browser_async: Browser):
    print(f'\n{browser_async, type(browser_async) = }')
    async with await browser_async.new_context() as context:
        async with await context.new_page() as page:
            await page.goto(URL)
            check_title(await page.title())


@pytest.mark.asyncio
async def test_context_async(context_async: BrowserContext):
    print(f'\n{context_async = }')
    async with await context_async.new_page() as page:
        await page.goto(URL)
        check_title(await page.title())


@pytest.mark.asyncio
async def test_page_async(page_async: Page):
    print(f'\n{page_async = }')
    await page_async.goto(URL)
    check_title(await page_async.title())
