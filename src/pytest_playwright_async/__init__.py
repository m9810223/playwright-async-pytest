import os
import sys
import typing as t

import pytest
import pytest_asyncio
from playwright.async_api import Browser
from playwright.async_api import BrowserContext
from playwright.async_api import BrowserType
from playwright.async_api import Error
from playwright.async_api import Page
from playwright.async_api import Playwright
from playwright.async_api import async_playwright
from pytest_playwright.pytest_playwright import VSCODE_PYTHON_EXTENSION_ID
from pytest_playwright.pytest_playwright import _build_artifact_test_folder
from pytest_playwright.pytest_playwright import _is_debugger_attached
from pytest_playwright.pytest_playwright import artifacts_folder
from pytest_playwright.pytest_playwright import slugify


@pytest.fixture(scope='session')
def browser_type_launch_args_async(pytestconfig: t.Any) -> t.Dict:
    launch_options = {}
    headed_option = pytestconfig.getoption('--headed')
    if headed_option:
        launch_options['headless'] = False
    elif VSCODE_PYTHON_EXTENSION_ID in sys.argv[0] and _is_debugger_attached():
        # When the VSCode debugger is attached, then launch the browser headed by default
        launch_options['headless'] = False
    browser_channel_option = pytestconfig.getoption('--browser-channel')
    if browser_channel_option:
        launch_options['channel'] = browser_channel_option
    slowmo_option = pytestconfig.getoption('--slowmo')
    if slowmo_option:
        launch_options['slow_mo'] = slowmo_option
    return launch_options


@pytest.fixture(scope='session')
def browser_context_args_async(
    pytestconfig: t.Any,
    playwright_async: Playwright,
    device: t.Optional[str],
    base_url: t.Optional[str],
) -> t.Dict:
    context_args = {}
    if device:
        context_args.update(playwright_async.devices[device])
    if base_url:
        context_args['base_url'] = base_url

    video_option = pytestconfig.getoption('--video')
    capture_video = video_option in ['on', 'retain-on-failure']
    if capture_video:
        context_args['record_video_dir'] = artifacts_folder.name

    return context_args


@pytest_asyncio.fixture(scope='session')
async def playwright_async() -> t.AsyncGenerator[Playwright, None]:
    pw = await async_playwright().start()
    yield pw
    await pw.stop()


@pytest.fixture(scope='session')
def browser_type_async(playwright_async: Playwright, browser_name: str) -> BrowserType:
    return getattr(playwright_async, browser_name)


@pytest.fixture(scope='session')
def launch_browser_async(
    browser_type_launch_args_async: dict,
    browser_type_async: BrowserType,
) -> t.Callable[..., t.Awaitable[Browser]]:
    async def launch(**kwargs: dict) -> Browser:
        launch_options = {**browser_type_launch_args_async, **kwargs}
        browser = await browser_type_async.launch(**launch_options)
        return browser

    return launch


@pytest_asyncio.fixture(scope='session')
async def browser_async(
    launch_browser_async: t.Callable[..., t.Awaitable[Browser]]
) -> t.AsyncGenerator[Browser, None]:
    browser = await launch_browser_async()
    yield browser
    await browser.close()
    artifacts_folder.cleanup()


@pytest_asyncio.fixture
async def context_async(
    browser_async: Browser,
    browser_context_args_async: t.Dict,
    pytestconfig: t.Any,
    request: pytest.FixtureRequest,
) -> t.AsyncGenerator[BrowserContext, None]:
    pages: t.List[Page] = []
    context = await browser_async.new_context(**browser_context_args_async)
    context.on('page', lambda page: pages.append(page))

    tracing_option = pytestconfig.getoption('--tracing')
    capture_trace = tracing_option in ['on', 'retain-on-failure']
    if capture_trace:
        await context.tracing.start(
            title=slugify(request.node.nodeid),
            screenshots=True,
            snapshots=True,
            sources=True,
        )

    yield context

    # If request.node is missing rep_call, then some error happened during execution
    # that prevented teardown, but should still be counted as a failure
    failed = request.node.rep_call.failed if hasattr(request.node, 'rep_call') else True

    if capture_trace:
        retain_trace = tracing_option == 'on' or (failed and tracing_option == 'retain-on-failure')
        if retain_trace:
            trace_path = _build_artifact_test_folder(pytestconfig, request, 'trace.zip')
            await context.tracing.stop(path=trace_path)
        else:
            await context.tracing.stop()

    screenshot_option = pytestconfig.getoption('--screenshot')
    capture_screenshot = screenshot_option == 'on' or (
        failed and screenshot_option == 'only-on-failure'
    )
    if capture_screenshot:
        for index, page in enumerate(pages):
            human_readable_status = 'failed' if failed else 'finished'
            screenshot_path = _build_artifact_test_folder(
                pytestconfig, request, f'test-{human_readable_status}-{index+1}.png'
            )
            try:
                await page.screenshot(timeout=5000, path=screenshot_path)
            except Error:
                pass

    await context.close()

    video_option = pytestconfig.getoption('--video')
    preserve_video = video_option == 'on' or (failed and video_option == 'retain-on-failure')
    if preserve_video:
        for page in pages:
            video = page.video
            if not video:
                continue
            try:
                video_path = video.path()
                file_name = os.path.basename(video_path)
                await video.save_as(
                    path=_build_artifact_test_folder(pytestconfig, request, file_name)
                )
            except Error:
                # Silent catch empty videos.
                pass


@pytest_asyncio.fixture
async def page_async(context_async: BrowserContext) -> t.AsyncGenerator[Page, None]:
    page = await context_async.new_page()
    yield page
