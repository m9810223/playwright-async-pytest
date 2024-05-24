# Playwright Async Pytest -- ASYNC Pytest plugin for Playwright

[![pypi](https://img.shields.io/pypi/v/pytest_playwright_async.svg)](https://pypi.python.org/pypi/pytest_playwright_async)

There an official playwright plugin for pytest: [PyPI](https://pypi.org/project/pytest-playwright/) / [playwright-pytest](https://github.com/microsoft/playwright-pytest) / [intro](https://playwright.dev/python/docs/intro).
But if you need an async version, here is it!

## Installation

```shell
pip install pytest-playwright-async
```

## Example

[Here](https://github.com/m9810223/playwright-async-pytest/blob/master/tests) you can find more examples.

```py
# tests/conftest.py
import asyncio

import pytest_asyncio


@pytest_asyncio.fixture(scope='session')
def event_loop():  # https://pytest-asyncio.readthedocs.io/en/latest/reference/fixtures.html#fixtures
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

```

```py
# tests/test_for_readme.py
from playwright.async_api import Page
import pytest


@pytest.mark.asyncio
async def test_page_async(page_async: Page):
    print(f'\n{page_async = }')
    await page_async.goto('https://playwright.dev/')
    assert 'Playwright' in await page_async.title()

```
