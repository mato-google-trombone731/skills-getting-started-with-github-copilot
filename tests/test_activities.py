from urllib.parse import quote


def test_get_activities(client):
    # Arrange: nothing to prepare — rely on fixture-provided initial state
    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "tester@example.com"
    url = f"/activities/{quote(activity, safe='')}/signup"

    # Act
    resp = client.post(url, params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Signed up {email} for {activity}"

    # Verify participant was added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange: use an existing participant from the seeded data
    activity = "Chess Club"
    existing_email = "michael@mergington.edu"
    url = f"/activities/{quote(activity, safe='')}/signup"

    # Act
    resp = client.post(url, params={"email": existing_email})

    # Assert
    assert resp.status_code == 400


def test_signup_nonexistent_activity(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "noone@example.com"
    url = f"/activities/{quote(activity, safe='')}/signup"

    # Act
    resp = client.post(url, params={"email": email})

    # Assert
    assert resp.status_code == 404


def test_unregister_success_and_missing(client):
    # Arrange
    activity = "Chess Club"
    email = "tempuser@example.com"
    signup_url = f"/activities/{quote(activity, safe='')}/signup"
    unregister_url = f"/activities/{quote(activity, safe='')}/unregister"

    # Act: sign up then unregister
    signup_resp = client.post(signup_url, params={"email": email})
    assert signup_resp.status_code == 200

    unregister_resp = client.post(unregister_url, params={"email": email})

    # Assert: successful unregister
    assert unregister_resp.status_code == 200
    assert unregister_resp.json()["message"] == f"Unregistered {email} from {activity}"

    # Act: try to unregister again
    second_resp = client.post(unregister_url, params={"email": email})

    # Assert: now missing
    assert second_resp.status_code == 404
