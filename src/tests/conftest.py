import os

from pytest import fixture


@fixture
def test_token():
    return "test_token"


@fixture(scope="function")
def test_environment(test_token):
    os.environ["APP_TOKEN"] = test_token
