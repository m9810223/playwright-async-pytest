from playwright.sync_api import Page


def test_page_async(page: Page):
    print(f'\n{page = }')
    page.goto('https://playwright.dev/')
    assert 'Playwright' in page.title()
