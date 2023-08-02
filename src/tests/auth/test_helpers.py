from unittest import mock

from app.auth.helpers import login_required


@mock.patch("app.auth.helpers.TokenAuthentication.is_authenticated")
def test_login_required(mock_is_authenticated: mock.Mock):
    mock_is_authenticated.return_value = True

    @login_required
    def test_func():
        return "test"

    assert test_func() == "test"
    mock_is_authenticated.assert_called_once()


@mock.patch("app.auth.helpers.url_for")
@mock.patch("app.auth.helpers.redirect")
@mock.patch("app.auth.helpers.flash")
@mock.patch("app.auth.helpers.TokenAuthentication.is_authenticated")
def test_login_required_failure(
    mock_is_authenticated: mock.Mock,
    mock_flash: mock.Mock,
    mock_redirect: mock.Mock,
    mock_url_for: mock.Mock,
):
    mock_redirect_result = "redirect"
    mock_redirect.return_value = mock_redirect_result
    mock_is_authenticated.return_value = False

    @login_required
    def test_func():
        return "test"

    assert test_func() == mock_redirect_result
    mock_flash.assert_called_once()
    mock_redirect.assert_called_once()
    mock_url_for.assert_called_once()
