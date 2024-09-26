"""
https://playwright.dev/python/docs/writing-tests#first-test
"""

import re

from playwright.async_api import Page
from playwright.async_api import expect


async def test_has_title(page_async: Page):
    await page_async.goto('https://playwright.dev/')

    # Expect a title "to contain" a substring.
    await expect(page_async).to_have_title(re.compile('Playwright'))


async def test_get_started_link(page_async: Page):
    await page_async.goto('https://playwright.dev/')

    # Click the get started link.
    await page_async.get_by_role('link', name='Get started').click()

    # Expects page to have a heading with the name of Installation.
    await expect(page_async.get_by_role('heading', name='Installation')).to_be_visible()
