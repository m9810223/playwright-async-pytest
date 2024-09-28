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

---

```py
# tests/async/conftest.py

import pytest


# install anyio
# install uvloop
@pytest.fixture(
    scope='session',
    params=[
        # https://anyio.readthedocs.io/en/stable/testing.html#specifying-the-backends-to-run-on
        pytest.param(('asyncio', {'use_uvloop': True}), id='asyncio+uvloop'),
        pytest.param(('asyncio', {'use_uvloop': False}), id='asyncio'),
        # pytest.param(('trio', {'restrict_keyboard_interrupt_to_checkpoints': True}), id='trio'),
    ],
    autouse=True,
)
def anyio_backend(request):
    return request.param

```

```py
# tests/async/test_for_readme.py

from playwright.async_api import Page


async def test_page_async(page_async: Page):
    print(f'\n{page_async = }')
    await page_async.goto('https://playwright.dev/')
    assert 'Playwright' in await page_async.title()

```
