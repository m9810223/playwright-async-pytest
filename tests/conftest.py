import asyncio
import asyncio.events as events
from contextlib import contextmanager
import os
import threading

import pytest_asyncio


def _patch_loop(loop):  # nest_asyncio
    """Patch loop to make it reentrant."""

    def run_until_complete(self, future):
        with manage_run(self):
            f = asyncio.ensure_future(future, loop=self)
            if f is not future:
                f._log_destroy_pending = False
            while not f.done():
                self._run_once()
                if self._stopping:
                    break
            if not f.done():
                raise RuntimeError('Event loop stopped before Future completed.')  # noqa: TRY003
            return f.result()

    @contextmanager
    def manage_run(self):
        """Set up the loop for running."""
        self._check_closed()
        old_thread_id = self._thread_id
        old_running_loop = events._get_running_loop()
        try:
            self._thread_id = threading.get_ident()
            events._set_running_loop(self)
            self._num_runs_pending += 1
            if self._is_proactorloop:
                if self._self_reading_future is None:
                    self.call_soon(self._loop_self_reading)
            yield
        finally:
            self._thread_id = old_thread_id
            events._set_running_loop(old_running_loop)
            self._num_runs_pending -= 1
            if self._is_proactorloop:
                if self._num_runs_pending == 0 and self._self_reading_future is not None:
                    ov = self._self_reading_future._ov
                    self._self_reading_future.cancel()
                    if ov is not None:
                        self._proactor._unregister(ov)
                    self._self_reading_future = None

    def _check_running(self):
        """Do not throw exception if loop is already running."""
        pass

    if hasattr(loop, '_nest_patched'):
        return
    if not isinstance(loop, asyncio.BaseEventLoop):
        raise ValueError("Can't patch loop of type %s" % type(loop))  # noqa: TRY004
    cls = loop.__class__
    cls.run_until_complete = run_until_complete
    cls._check_running = _check_running
    cls._num_runs_pending = 1 if loop.is_running() else 0
    cls._is_proactorloop = os.name == 'nt' and issubclass(cls, asyncio.ProactorEventLoop)
    cls._nest_patched = True


@pytest_asyncio.fixture(scope='session')
def event_loop():  # https://pytest-asyncio.readthedocs.io/en/latest/reference/fixtures.html#fixtures
    loop = asyncio.get_event_loop_policy().new_event_loop()
    _patch_loop(loop)
    yield loop
    loop.close()
