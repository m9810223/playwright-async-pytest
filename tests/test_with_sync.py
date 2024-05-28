from playwright.sync_api import Page as SPage


def test_sync_api(page: SPage):
    # access webpage
    page.goto('https://playwright.dev/')
