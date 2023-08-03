from unittest import mock

from flask.wrappers import Request

from app.auth.token_authentication import TokenAuthentication


def test_is_authenticated(test_token, test_environment):
    with mock.patch("app.auth.token_authentication.session", dict()) as mock_session:
        mock_session["token"] = test_token

        mock_request = Request.from_values()

        token_authentication = TokenAuthentication(mock_request)

        result = token_authentication.is_authenticated()

        assert result == True


def test_is_authenticated_token_from_headers(test_token, test_environment):
    mock_request = Request.from_values(headers={"Authorization": f"Token {test_token}"})

    token_authentication = TokenAuthentication(mock_request)

    result = token_authentication.is_authenticated()

    assert result == True


def test_is_authenticated_no_token(test_token, test_environment):
    with mock.patch("app.auth.token_authentication.session", dict()) as mock_session:
        mock_session["token"] = None

        mock_request = Request.from_values()

        token_authentication = TokenAuthentication(mock_request)

        result = token_authentication.is_authenticated()

        assert result == None


def test_is_authorised(test_token, test_environment):
    mock_request = Request.from_values(method="POST", json={"token": test_token})

    token_authentication = TokenAuthentication(mock_request)

    result = token_authentication.is_authorised()

    assert result == True


def test_is_authorised_wrong_token(test_environment):
    mock_request = Request.from_values(method="POST", json={"token": "bad_token"})

    token_authentication = TokenAuthentication(mock_request)

    result = token_authentication.is_authorised()

    assert result == False


def test_is_authorised_non_post(test_token, test_environment):
    mock_request = Request.from_values(method="GET", json={"token": test_token})

    token_authentication = TokenAuthentication(mock_request)

    result = token_authentication.is_authorised()

    assert result == False


def test_is_valid_token(test_token, test_environment):
    mock_request = Request.from_values(method="GET", json={"token": test_token})

    token_authentication = TokenAuthentication(mock_request)

    result = token_authentication._is_valid_token(test_token)

    assert result == True


def test_is_valid_token_no_token(test_token, test_environment):
    mock_request = Request.from_values(method="GET", json={"token": test_token})

    token_authentication = TokenAuthentication(mock_request)

    result = token_authentication._is_valid_token(None)

    assert result == False


def test_is_valid_token_bad_token(test_token, test_environment):
    mock_request = Request.from_values(method="GET", json={"token": test_token})

    token_authentication = TokenAuthentication(mock_request)

    result = token_authentication._is_valid_token("bad_token")

    assert result == False
