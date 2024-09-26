import os
from pathlib import Path
import shutil
import tempfile
from typing import Any
from typing import AsyncGenerator
from typing import Awaitable
from typing import Callable
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Pattern
from typing import Protocol
from typing import Sequence
from typing import Union
from typing import cast

from playwright.async_api import Browser
from playwright.async_api import BrowserContext
from playwright.async_api import BrowserType
from playwright.async_api import Error
from playwright.async_api import Geolocation
from playwright.async_api import HttpCredentials
from playwright.async_api import Page
from playwright.async_api import Playwright
from playwright.async_api import ProxySettings
from playwright.async_api import StorageState
from playwright.async_api import ViewportSize
from playwright.async_api import async_playwright
import pytest
from pytest_playwright.pytest_playwright import _build_artifact_test_folder
from pytest_playwright.pytest_playwright import _create_guid
from pytest_playwright.pytest_playwright import slugify


###


@pytest.fixture(scope='session')
def browser_context_args_async(
    pytestconfig: Any,
    playwright_async: Playwright,
    device: Optional[str],
    base_url: Optional[str],
    _pw_artifacts_folder: tempfile.TemporaryDirectory,
) -> Dict:
    context_args = {}
    if device:
        context_args.update(playwright_async.devices[device])
    if base_url:
        context_args['base_url'] = base_url

    video_option = pytestconfig.getoption('--video')
    capture_video = video_option in ['on', 'retain-on-failure']
    if capture_video:
        context_args['record_video_dir'] = _pw_artifacts_folder.name

    return context_args


@pytest.fixture
async def _artifacts_recorder_async(
    request: pytest.FixtureRequest,
    playwright_async: Playwright,
    pytestconfig: Any,
    _pw_artifacts_folder: tempfile.TemporaryDirectory,
) -> AsyncGenerator['AsyncArtifactsRecorder', None]:
    async_artifacts_recorder = AsyncArtifactsRecorder(
        pytestconfig, request, playwright_async, _pw_artifacts_folder
    )
    yield async_artifacts_recorder
    # If request.node is missing rep_call, then some error happened during execution
    # that prevented teardown, but should still be counted as a failure
    failed = request.node.rep_call.failed if hasattr(request.node, 'rep_call') else True
    await async_artifacts_recorder.did_finish_test(failed)


@pytest.fixture(scope='session')
async def playwright_async() -> AsyncGenerator[Playwright, None]:
    apw = await async_playwright().start()
    yield apw
    await apw.stop()


@pytest.fixture(scope='session')
async def browser_type_async(playwright_async: Playwright, browser_name: str) -> BrowserType:
    return getattr(playwright_async, browser_name)


@pytest.fixture(scope='session')
def launch_browser_async(
    browser_type_launch_args: Dict,
    browser_type_async: BrowserType,
) -> Callable[..., Awaitable[Browser]]:
    async def launch(**kwargs: Dict) -> Browser:
        launch_options = {**browser_type_launch_args, **kwargs}
        browser_async = await browser_type_async.launch(**launch_options)
        return browser_async

    return launch


@pytest.fixture(scope='session')
async def browser_async(
    launch_browser_async: Callable[..., Awaitable[Browser]],
) -> AsyncGenerator[Browser, None]:
    browser_async = await launch_browser_async()
    yield browser_async
    await browser_async.close()


class AsyncCreateContextCallback(Protocol):
    async def __call__(
        self,
        viewport: Optional[ViewportSize] = None,
        screen: Optional[ViewportSize] = None,
        no_viewport: Optional[bool] = None,
        ignore_https_errors: Optional[bool] = None,
        java_script_enabled: Optional[bool] = None,
        bypass_csp: Optional[bool] = None,
        user_agent: Optional[str] = None,
        locale: Optional[str] = None,
        timezone_id: Optional[str] = None,
        geolocation: Optional[Geolocation] = None,
        permissions: Optional[Sequence[str]] = None,
        extra_http_headers: Optional[Dict[str, str]] = None,
        offline: Optional[bool] = None,
        http_credentials: Optional[HttpCredentials] = None,
        device_scale_factor: Optional[float] = None,
        is_mobile: Optional[bool] = None,
        has_touch: Optional[bool] = None,
        color_scheme: Optional[Literal['dark', 'light', 'no-preference', 'null']] = None,
        reduced_motion: Optional[Literal['no-preference', 'null', 'reduce']] = None,
        forced_colors: Optional[Literal['active', 'none', 'null']] = None,
        accept_downloads: Optional[bool] = None,
        default_browser_type: Optional[str] = None,
        proxy: Optional[ProxySettings] = None,
        record_har_path: Optional[Union[str, Path]] = None,
        record_har_omit_content: Optional[bool] = None,
        record_video_dir: Optional[Union[str, Path]] = None,
        record_video_size: Optional[ViewportSize] = None,
        storage_state: Optional[Union[StorageState, str, Path]] = None,
        base_url: Optional[str] = None,
        strict_selectors: Optional[bool] = None,
        service_workers: Optional[Literal['allow', 'block']] = None,
        record_har_url_filter: Optional[Union[str, Pattern[str]]] = None,
        record_har_mode: Optional[Literal['full', 'minimal']] = None,
        record_har_content: Optional[Literal['attach', 'embed', 'omit']] = None,
    ) -> BrowserContext: ...


@pytest.fixture
async def new_context_async(
    browser_async: Browser,
    browser_context_args_async: dict,
    _artifacts_recorder_async: 'AsyncArtifactsRecorder',
    request: pytest.FixtureRequest,
) -> AsyncGenerator[AsyncCreateContextCallback, None]:
    browser_context_args_async = browser_context_args_async.copy()
    context_args_marker = next(request.node.iter_markers('browser_context_args'), None)
    additional_context_args = context_args_marker.kwargs if context_args_marker else {}
    browser_context_args_async.update(additional_context_args)
    acontexts: List[BrowserContext] = []

    async def _new_context_async(**kwargs: Any) -> BrowserContext:
        context_async = await browser_async.new_context(**browser_context_args_async, **kwargs)
        original_close = context_async.close

        async def _close_wrapper(*args: Any, **kwargs: Any) -> None:
            acontexts.remove(context_async)
            await _artifacts_recorder_async.on_will_close_browser_context(context_async)
            await original_close(*args, **kwargs)

        context_async.close = _close_wrapper
        acontexts.append(context_async)
        await _artifacts_recorder_async.on_did_create_browser_context(context_async)
        return context_async

    yield cast(AsyncCreateContextCallback, _new_context_async)
    for context_async in acontexts.copy():
        await context_async.close()


@pytest.fixture
async def context_async(new_context_async: AsyncCreateContextCallback) -> BrowserContext:
    return await new_context_async()


@pytest.fixture
async def page_async(context_async: BrowserContext) -> Page:
    return await context_async.new_page()


###


class AsyncArtifactsRecorder:
    def __init__(
        self,
        pytestconfig: Any,
        request: pytest.FixtureRequest,
        playwright_async: Playwright,
        pw_artifacts_folder: tempfile.TemporaryDirectory,
    ) -> None:
        self._request = request
        self._pytestconfig = pytestconfig
        self._playwright_async = playwright_async
        self._pw_artifacts_folder = pw_artifacts_folder

        self._all_pages: List[Page] = []
        self._screenshots: List[str] = []
        self._traces: List[str] = []
        self._tracing_option = pytestconfig.getoption('--tracing')
        self._capture_trace = self._tracing_option in ['on', 'retain-on-failure']

    async def did_finish_test(self, failed: bool) -> None:
        screenshot_option = self._pytestconfig.getoption('--screenshot')
        capture_screenshot = screenshot_option == 'on' or (
            failed and screenshot_option == 'only-on-failure'
        )
        if capture_screenshot:
            for index, screenshot in enumerate(self._screenshots):
                human_readable_status = 'failed' if failed else 'finished'
                screenshot_path = _build_artifact_test_folder(
                    self._pytestconfig,
                    self._request,
                    f'test-{human_readable_status}-{index+1}.png',
                )
                os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
                shutil.move(screenshot, screenshot_path)
        else:
            for screenshot in self._screenshots:
                os.remove(screenshot)

        if self._tracing_option == 'on' or (failed and self._tracing_option == 'retain-on-failure'):
            for index, trace in enumerate(self._traces):
                trace_file_name = 'trace.zip' if len(self._traces) == 1 else f'trace-{index+1}.zip'
                trace_path = _build_artifact_test_folder(
                    self._pytestconfig, self._request, trace_file_name
                )
                os.makedirs(os.path.dirname(trace_path), exist_ok=True)
                shutil.move(trace, trace_path)
        else:
            for trace in self._traces:
                os.remove(trace)

        video_option = self._pytestconfig.getoption('--video')
        preserve_video = video_option == 'on' or (failed and video_option == 'retain-on-failure')
        if preserve_video:
            for index, page in enumerate(self._all_pages):
                video = page.video
                if not video:
                    continue
                try:
                    video_file_name = (
                        'video.webm' if len(self._all_pages) == 1 else f'video-{index+1}.webm'
                    )
                    await video.save_as(
                        path=_build_artifact_test_folder(
                            self._pytestconfig, self._request, video_file_name
                        )
                    )
                except Error:
                    # Silent catch empty videos.
                    pass
        else:
            for page in self._all_pages:
                # Can be changed to "if page.video" without try/except once https://github.com/microsoft/playwright-python/pull/2410 is released and widely adopted.
                if video_option in ['on', 'retain-on-failure']:
                    try:
                        await page.video.delete()
                    except Error:
                        pass

    async def on_did_create_browser_context(self, context_async: BrowserContext) -> None:
        context_async.on('page', lambda page: self._all_pages.append(page))
        if self._request and self._capture_trace:
            await context_async.tracing.start(
                title=slugify(self._request.node.nodeid),
                screenshots=True,
                snapshots=True,
                sources=True,
            )

    async def on_will_close_browser_context(self, context_async: BrowserContext) -> None:
        if self._capture_trace:
            trace_path = Path(self._pw_artifacts_folder.name) / _create_guid()
            await context_async.tracing.stop(path=trace_path)
            self._traces.append(str(trace_path))
        else:
            await context_async.tracing.stop()

        if self._pytestconfig.getoption('--screenshot') in ['on', 'only-on-failure']:
            for page in context_async.pages:
                try:
                    screenshot_path = Path(self._pw_artifacts_folder.name) / _create_guid()
                    await page.screenshot(
                        timeout=5000,
                        path=screenshot_path,
                        full_page=self._pytestconfig.getoption('--full-page-screenshot'),
                    )
                    self._screenshots.append(str(screenshot_path))
                except Error:
                    pass
