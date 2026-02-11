import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app
import src.app

client = TestClient(app)

# Store initial activities state for test isolation
INITIAL_ACTIVITIES = deepcopy(src.app.activities)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities state before each test to ensure test isolation"""
    src.app.activities.clear()
    src.app.activities.update(deepcopy(INITIAL_ACTIVITIES))

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("description" in v and "participants" in v for v in data.values())

def test_signup_and_remove_participant():
    # Get an activity name
    response = client.get("/activities")
    activities = response.json()
    activity_name = next(iter(activities))
    email = "testuser@mergington.edu"

    # Sign up
    signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup.status_code == 200
    assert f"Signed up {email}" in signup.json()["message"]

    # Try duplicate signup
    dup = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert dup.status_code == 400
    assert "already signed up" in dup.json()["detail"]

    # Remove participant
    remove = client.delete(f"/activities/{activity_name}/signup?email={email}")
    assert remove.status_code == 200
    assert f"removed from {activity_name}" in remove.json()["message"]

    # Remove non-existent participant
    remove2 = client.delete(f"/activities/{activity_name}/signup?email={email}")
    assert remove2.status_code == 404
    assert "Participant not found" in remove2.json()["detail"]
