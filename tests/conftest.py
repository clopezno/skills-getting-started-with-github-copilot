"""Pytest configuration and fixtures for test isolation"""
import pytest
from copy import deepcopy
import src.app

# Store initial activities state for test isolation
INITIAL_ACTIVITIES = deepcopy(src.app.activities)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities state before each test to ensure test isolation"""
    src.app.activities.clear()
    src.app.activities.update(deepcopy(INITIAL_ACTIVITIES))
