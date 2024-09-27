import asyncio

import nest_asyncio  # pip install nest-asyncio
import pytest


@pytest.fixture(scope='session', autouse=True)
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    nest_asyncio._patch_loop(loop)  # *
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
# pip install anyio
def anyio_backend():
    return 'asyncio'
