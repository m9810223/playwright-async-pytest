import typing as t

from playwright.async_api import Browser
from playwright.async_api import BrowserContext
from playwright.async_api import BrowserType
from playwright.async_api import Page
from playwright.async_api import Playwright
from playwright.async_api import async_playwright
from playwright.sync_api import Browser as SBrowser
from playwright.sync_api import BrowserContext as SBrowserContext
from playwright.sync_api import BrowserType as SBrowserType
from playwright.sync_api import Page as SPage
from playwright.sync_api import Playwright as SPlaywright
from playwright.sync_api import sync_playwright
import pytest


URL = 'https://playwright.dev/'


def check_title(title):
    assert 'Playwright' in title


async def test_async_playwright():
    async with async_playwright() as playwright:
        async with await playwright.chromium.launch() as browser:
            async with await browser.new_context() as context:
                async with await context.new_page() as page:
                    await page.goto(URL)
                    check_title(await page.title())


@pytest.mark.skip(reason='Not working')
def test_sync_playwright():
    with sync_playwright() as playwright:
        with playwright.chromium.launch() as browser:
            with browser.new_context() as context:
                with context.new_page() as page:
                    page.goto(URL)
                    check_title(page.title())


# https://playwright.dev/python/docs/test-runners#fixtures


async def test_is_working_playwright_async(playwright_async: Playwright):
    print(f'\n{playwright_async = }')
    assert isinstance(playwright_async, Playwright)


def test_is_working_playwright_sync(playwright: SPlaywright):
    print(f'\n{playwright = }')
    assert isinstance(playwright, SPlaywright)


async def test_is_working_browser_async(browser_async: Browser):
    print(f'\n{browser_async = }')
    assert isinstance(browser_async, Browser)


def test_is_working_browser_sync(browser: SBrowser):
    print(f'\n{browser = }')
    assert isinstance(browser, SBrowser)


async def test_is_working_browser_name_async(browser_name: str):
    print(f'\n{browser_name = }')
    assert isinstance(browser_name, str)


def test_is_working_browser_name(browser_name: str):
    print(f'\n{browser_name = }')
    assert isinstance(browser_name, str)


async def test_is_working_browser_channel_async(browser_channel: t.Optional[str]):
    print(f'\n{browser_channel = }')
    assert isinstance(browser_channel, str) or browser_channel is None


def test_is_working_browser_channel(browser_channel: t.Optional[str]):
    print(f'\n{browser_channel = }')
    assert isinstance(browser_channel, str) or browser_channel is None


async def test_is_working_context_async(context_async: BrowserContext):
    print(f'\n{context_async = }')
    assert isinstance(context_async, BrowserContext)


def test_is_working_context_sync(context: SBrowserContext):
    print(f'\n{context = }')
    assert isinstance(context, SBrowserContext)


async def test_is_working_browser_context_args_async(browser_context_args_async: dict):
    print(f'\n{browser_context_args_async = }')
    assert isinstance(browser_context_args_async, dict)


def test_is_working_browser_context_args_sync(browser_context_args: dict):
    print(f'\n{browser_context_args = }')
    assert isinstance(browser_context_args, dict)


async def test_is_working_page_async(page_async: Page):
    print(f'\n{page_async = }')
    assert isinstance(page_async, Page)


def test_is_working_page_sync(page: SPage):
    print(f'\n{page = }')
    assert isinstance(page, SPage)


###


async def test_browser_context_args_async(browser_context_args_async: t.Dict):
    print(f'\n{browser_context_args_async, type(browser_context_args_async) = }')
    async with async_playwright() as playwright:
        async with await playwright.chromium.launch() as browser:
            async with await browser.new_context(**browser_context_args_async) as context:
                async with await context.new_page() as page:
                    await page.goto(URL)
                    check_title(await page.title())


@pytest.mark.skip(reason='Not working')
def test_browser_context_args_sync(browser_context_args: t.Dict):
    print(f'\n{browser_context_args, type(browser_context_args) = }')
    with sync_playwright() as playwright:
        with playwright.chromium.launch() as browser:
            with browser.new_context(**browser_context_args) as context:
                with context.new_page() as page:
                    page.goto(URL)
                    check_title(page.title())


async def test_playwright_async(playwright_async: Playwright):
    print(f'\n{playwright_async, type(playwright_async) = }')
    async with await playwright_async.chromium.launch() as browser:
        async with await browser.new_context() as context:
            async with await context.new_page() as page:
                await page.goto(URL)
                check_title(await page.title())


def test_playwright_sync(playwright: SPlaywright):
    print(f'\n{playwright, type(playwright) = }')
    with playwright.chromium.launch() as browser:
        with browser.new_context() as context:
            with context.new_page() as page:
                page.goto(URL)
                check_title(page.title())


async def test_browser_type_async(browser_type_async: BrowserType):
    print(f'\n{browser_type_async, type(browser_type_async) = }')
    async with await browser_type_async.launch() as browser:
        async with await browser.new_context() as context:
            async with await context.new_page() as page:
                await page.goto(URL)
                check_title(await page.title())


def test_browser_type_sync(browser_type: SBrowserType):
    print(f'\n{browser_type, type(browser_type) = }')
    with browser_type.launch() as browser:
        with browser.new_context() as context:
            with context.new_page() as page:
                page.goto(URL)
                check_title(page.title())


async def test_launch_browser_async(launch_browser_async: t.Callable[..., t.Awaitable[Browser]]):
    print(f'\n{launch_browser_async, type(launch_browser_async) = }')
    browser = await launch_browser_async()
    async with await browser.new_context() as context:
        async with await context.new_page() as page:
            await page.goto(URL)
            check_title(await page.title())


def test_launch_browser_sync(launch_browser: t.Callable[..., SBrowser]):
    print(f'\n{launch_browser, type(launch_browser) = }')
    browser = launch_browser()
    with browser.new_context() as context:
        with context.new_page() as page:
            page.goto(URL)
            check_title(page.title())


async def test_browser_async(browser_async: Browser):
    print(f'\n{browser_async, type(browser_async) = }')
    async with await browser_async.new_context() as context:
        async with await context.new_page() as page:
            await page.goto(URL)
            check_title(await page.title())


def test_browser_sync(browser: SBrowser):
    print(f'\n{browser, type(browser) = }')
    with browser.new_context() as context:
        with context.new_page() as page:
            page.goto(URL)
            check_title(page.title())


async def test_context_async(context_async: BrowserContext):
    print(f'\n{context_async = }')
    async with await context_async.new_page() as page:
        await page.goto(URL)
        check_title(await page.title())


def test_context_sync(context: SBrowserContext):
    print(f'\n{context = }')
    with context.new_page() as page:
        page.goto(URL)
        check_title(page.title())


async def test_page_async(page_async: Page):
    print(f'\n{page_async = }')
    await page_async.goto(URL)
    check_title(await page_async.title())


def test_page_sync(page: SPage):
    print(f'\n{page = }')
    page.goto(URL)
    check_title(page.title())
