from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def pytest_configure(config):
    config.addinivalue_line("markers", "anyio: run test with AnyIO")


import pytest


@pytest.fixture
def anyio_backend():
    return "asyncio"
