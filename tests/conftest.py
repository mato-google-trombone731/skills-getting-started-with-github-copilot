import copy
import pytest
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture(scope="module")
def client():
    """Provide a TestClient for the FastAPI `app` defined in `src.app`."""
    with TestClient(app_module.app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the module-level `activities` dict in `src.app` before/after each test.

    This preserves the original dict object reference but restores its contents,
    so tests can mutate `activities` without affecting other tests.
    """
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))
