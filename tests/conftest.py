import asyncio

import pytest_asyncio


@pytest_asyncio.fixture(scope='session')
def event_loop():  # https://pytest-asyncio.readthedocs.io/en/latest/reference/fixtures.html#fixtures
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
