import typing as t

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


@pytest.mark.xfail(reason='Not working')
def test_sync_playwright():
    with sync_playwright() as playwright:
        with playwright.chromium.launch() as browser:
            with browser.new_context() as context:
                with context.new_page() as page:
                    page.goto(URL)
                    check_title(page.title())


# https://playwright.dev/python/docs/test-runners#fixtures


def test_is_working_playwright_sync(playwright: SPlaywright):
    print(f'\n{playwright = }')
    assert isinstance(playwright, SPlaywright)


def test_is_working_browser_sync(browser: SBrowser):
    print(f'\n{browser = }')
    assert isinstance(browser, SBrowser)


def test_is_working_browser_name(browser_name: str):
    print(f'\n{browser_name = }')
    assert isinstance(browser_name, str)


def test_is_working_browser_channel(browser_channel: t.Optional[str]):
    print(f'\n{browser_channel = }')
    assert isinstance(browser_channel, str) or browser_channel is None


def test_is_working_context_sync(context: SBrowserContext):
    print(f'\n{context = }')
    assert isinstance(context, SBrowserContext)


def test_is_working_browser_context_args_sync(browser_context_args: dict):
    print(f'\n{browser_context_args = }')
    assert isinstance(browser_context_args, dict)


def test_is_working_page_sync(page: SPage):
    print(f'\n{page = }')
    assert isinstance(page, SPage)


###


@pytest.mark.xfail(reason='Not working')
def test_browser_context_args_sync(browser_context_args: t.Dict):
    print(f'\n{browser_context_args, type(browser_context_args) = }')
    with sync_playwright() as playwright:
        with playwright.chromium.launch() as browser:
            with browser.new_context(**browser_context_args) as context:
                with context.new_page() as page:
                    page.goto(URL)
                    check_title(page.title())


def test_playwright_sync(playwright: SPlaywright):
    print(f'\n{playwright, type(playwright) = }')
    with playwright.chromium.launch() as browser:
        with browser.new_context() as context:
            with context.new_page() as page:
                page.goto(URL)
                check_title(page.title())


def test_browser_type_sync(browser_type: SBrowserType):
    print(f'\n{browser_type, type(browser_type) = }')
    with browser_type.launch() as browser:
        with browser.new_context() as context:
            with context.new_page() as page:
                page.goto(URL)
                check_title(page.title())


def test_launch_browser_sync(launch_browser: t.Callable[..., SBrowser]):
    print(f'\n{launch_browser, type(launch_browser) = }')
    browser = launch_browser()
    with browser.new_context() as context:
        with context.new_page() as page:
            page.goto(URL)
            check_title(page.title())


def test_browser_sync(browser: SBrowser):
    print(f'\n{browser, type(browser) = }')
    with browser.new_context() as context:
        with context.new_page() as page:
            page.goto(URL)
            check_title(page.title())


def test_context_sync(context: SBrowserContext):
    print(f'\n{context = }')
    with context.new_page() as page:
        page.goto(URL)
        check_title(page.title())


def test_page_sync(page: SPage):
    print(f'\n{page = }')
    page.goto(URL)
    check_title(page.title())
