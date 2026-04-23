import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


def test_get_activities_returns_activity_list(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity in data
    assert isinstance(data[expected_activity]["participants"], list)
    assert data[expected_activity]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "teststudent@example.com"
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_unregister_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "teststudent@example.com"
    if email not in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].append(email)

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_duplicate_signup_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = activities[activity_name]["participants"][0]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()
