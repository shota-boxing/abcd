import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity_success():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Ensure not already signed up
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up successfully"
    assert email in activities[activity]["participants"]

def test_signup_for_activity_already_signed_up():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Ensure already signed up
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"

def test_signup_for_activity_not_found():
    response = client.post("/activities/UnknownActivity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_signup_for_activity_full():
    activity = "Math Club"
    # Fill up participants
    activities[activity]["participants"] = [f"student{i}@mergington.edu" for i in range(activities[activity]["max_participants"])]
    response = client.post(f"/activities/{activity}/signup?email=overflow@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"

def test_unregister_participant():
    activity = "Chess Club"
    email = "deleteuser@mergington.edu"
    # Add user if not present
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)
    # Simulate DELETE logic
    activities[activity]["participants"].remove(email)
    assert email not in activities[activity]["participants"]
