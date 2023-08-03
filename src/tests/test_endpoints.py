from unittest import mock

from server import app


def test_index(test_token, test_environment):
    client = app.test_client()

    with client.session_transaction() as session:
        session["token"] = test_token

    response = client.get("/")
    assert response.status_code == 200
    assert response.content_type == "text/html; charset=utf-8"


def test_index_redirect(test_environment):
    client = app.test_client()

    with client.session_transaction() as session:
        session["token"] = None

    response = client.get("/")
    assert response.status_code == 302


def test_login_get(test_environment):
    client = app.test_client()

    response = client.get("/login")
    assert response.status_code == 200
    assert response.content_type == "text/html; charset=utf-8"


def test_login_post(test_token, test_environment):
    client = app.test_client()

    response = client.post("/login", json={"token": test_token})
    assert response.status_code == 200
    assert response.content_type == "application/json"


def test_login_post_bad_token(test_environment):
    client = app.test_client()

    response = client.post("/login", json={"token": "bad_token"})
    assert response.status_code == 400
    assert response.content_type == "application/json"


@mock.patch("app.database_query.DatabaseQuery.query")
def test_ask_query(mock_query: mock.Mock, test_token, test_environment):
    client = app.test_client()

    with client.session_transaction() as session:
        session["token"] = test_token

    mock_query_response = "test"
    mock_query.return_value = mock_query_response
    mock_prompt = "test"

    response = client.post("/ask-query", json={"prompt": mock_prompt})
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json == {"query_result": mock_query_response}
    mock_query.assert_called_once_with(mock_prompt)


def test_ask_query_redirect(test_environment):
    client = app.test_client()

    with client.session_transaction() as session:
        session["token"] = None

    response = client.post("/ask-query", json={"prompt": "test"})
    assert response.status_code == 302


def test_logout(test_token, test_environment):
    client = app.test_client()

    with client.session_transaction() as session:
        session["token"] = test_token

    response = client.get("/logout")
    assert response.status_code == 200
    assert response.content_type == "application/json"
    print(session)
    assert not session.get("token")
