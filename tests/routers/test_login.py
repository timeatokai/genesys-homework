def test_login_success(test_client, unique_username, unique_email):
    # create user
    user_data = {"name": unique_username, "email": unique_email, "password": "pass"}
    test_client.post("/users/create", json=user_data)

    response = test_client.post(
        "/token",
        data={"username": unique_username, "password": "pass"},
    )
    resp = response.json()

    assert response.status_code == 200, resp


def test_login_incorrect_user(test_client, unique_username):
    response = test_client.post(
        "/token",
        data={"username": unique_username, "password": "pass"},
    )
    resp = response.json()

    assert response.status_code == 401, resp
    assert resp == {"detail": "Incorrect username or password"}


def test_login_incorrect_password(test_client, unique_username, unique_email):
    # create user
    user_data = {"name": unique_username, "email": unique_email, "password": "pass"}
    test_client.post("/users/create", json=user_data)

    response = test_client.post(
        "/token",
        data={"username": unique_username, "password": "incorrect_pass"},
    )
    resp = response.json()

    assert response.status_code == 401, resp
    assert resp == {"detail": "Incorrect username or password"}
