from datetime import datetime, timedelta


def test_create_user_success(test_client, unique_username, unique_email):
    user_data = {"name": unique_username, "email": unique_email, "password": "pass"}

    response = test_client.post("/users/create", json=user_data)
    resp = response.json()

    assert response.status_code == 200, resp
    assert resp["name"] == user_data["name"]
    assert resp["email"] == user_data["email"]
    assert datetime.strptime(
        resp["last_login"], "%Y-%m-%dT%H:%M:%S.%f"
    ) - datetime.now() < timedelta(milliseconds=10)


def test_create_user_existing_username(test_client, unique_username, unique_email):
    user_data = {"name": unique_username, "email": unique_email, "password": "pass"}
    existing_user = user_data.copy()
    existing_user["email"] = f"test.{unique_email}"

    test_client.post("/users/create", json=user_data)
    response = test_client.post("/users/create", json=existing_user)
    resp = response.json()

    assert response.status_code == 400
    assert response.json() == {"detail": "Name already in use"}


def test_create_user_existing_email(test_client, unique_username, unique_email):
    user_data = {"name": unique_username, "email": unique_email, "password": "pass"}
    existing_user = user_data.copy()
    existing_user["name"] = f"test {unique_username}"

    test_client.post("/users/create", json=user_data)
    response = test_client.post("/users/create", json=existing_user)
    resp = response.json()

    assert response.status_code == 400, resp
    assert resp == {"detail": "Email already registered"}


def test_update_user_success(test_client, unique_username, unique_email):
    user_data = {"name": unique_username, "email": unique_email, "password": "pass"}
    existing_user = user_data.copy()
    existing_user["name"] = f"test {unique_username}"

    user_id = test_client.post("/users/create", json=existing_user).json()["id"]
    response = test_client.put(f"/users/{user_id}", json=user_data)
    resp = response.json()

    assert response.status_code == 200, resp
    assert resp["name"] == user_data["name"]
    assert resp["email"] == user_data["email"]
    assert datetime.strptime(
        resp["last_login"], "%Y-%m-%dT%H:%M:%S.%f"
    ) - datetime.now() < timedelta(milliseconds=10)


def test_update_user_nonexistent_user(test_client, unique_username, unique_email):
    user_data = {"name": unique_username, "email": unique_email, "password": "pass"}

    response = test_client.put(f"/users/{-1}", json=user_data)
    resp = response.json()

    assert response.status_code == 404, resp
    assert resp == {"detail": "User ID not in database"}


def test_update_user_success(test_client, unique_username, unique_email):
    user_data = {"name": unique_username, "email": unique_email, "password": "pass"}
    existing_user = user_data.copy()
    existing_user["name"] = f"test {unique_username}"

    user_id = test_client.post("/users/create", json=existing_user).json()["id"]
    response = test_client.put(f"/users/{user_id}", json=user_data)
    resp = response.json()

    assert response.status_code == 200, resp
    assert resp["name"] == user_data["name"]
    assert resp["email"] == user_data["email"]
    assert datetime.strptime(
        resp["last_login"], "%Y-%m-%dT%H:%M:%S.%f"
    ) - datetime.now() < timedelta(milliseconds=10)


def test_delete_user(test_client, unique_username, unique_email):
    user_data = {"name": unique_username, "email": unique_email, "password": "pass"}

    user_id = test_client.post("/users/create", json=user_data).json()["id"]
    response = test_client.delete(f"/users/{user_id}")
    resp = response.json()

    assert response.status_code == 200, resp


def test_delete_user_nonexistent_user(test_client):
    response = test_client.delete(f"/users/{-1}")
    resp = response.json()

    assert response.status_code == 404, resp
    assert resp == {"detail": "User ID not in database"}


def test_list_users(test_client):
    response = test_client.get("/users/list")
    resp = response.json()

    assert response.status_code == 200, resp
