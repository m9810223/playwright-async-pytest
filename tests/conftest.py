import asyncio

import nest_asyncio
import pytest


@pytest.fixture(scope='session', autouse=True)
def event_loop():  # https://pytest-asyncio.readthedocs.io/en/latest/reference/fixtures.html#fixtures
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    nest_asyncio._patch_loop(loop)  # *
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
def anyio_backend():
    return 'asyncio'
