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
