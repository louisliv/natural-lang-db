from unittest import mock

import pytest

from app.database_query import DatabaseQuery, ERROR_MESSAGE


@mock.patch("app.database_query.OpenAI")
@mock.patch("app.database_query.SQLDatabase")
@mock.patch("app.database_query.create_sql_agent")
@mock.patch("app.database_query.SQLDatabaseToolkit")
def test_database_query_init(
    mock_sql_database_toolkit,
    mock_create_sql_agent,
    mock_sql_database,
    mock_open_ai,
):
    setattr(mock_sql_database, "from_uri", mock.Mock())

    database_query = DatabaseQuery()

    assert database_query.db == mock_sql_database.from_uri.return_value
    assert database_query.llm == mock_open_ai.return_value
    assert database_query.toolkit == mock_sql_database_toolkit.return_value
    assert database_query.agent_executor == mock_create_sql_agent.return_value


@mock.patch("app.database_query.OpenAI")
@mock.patch("app.database_query.SQLDatabase")
@mock.patch("app.database_query.create_sql_agent")
@mock.patch("app.database_query.SQLDatabaseToolkit")
def test_database_query_query(
    mock_sql_database_toolkit,
    mock_create_sql_agent,
    mock_sql_database,
    mock_open_ai,
):
    mock_sql_agent = mock.MagicMock()
    mock_response = "Test response"
    mock_sql_agent.run.return_value = mock_response
    mock_create_sql_agent.return_value = mock_sql_agent
    mock_prompt = "prompt"

    setattr(mock_sql_database, "from_uri", mock.Mock())

    result = DatabaseQuery().query(mock_prompt)

    assert result == mock_response
    mock_sql_agent.run.assert_called_once_with(mock_prompt)


@mock.patch("app.database_query.OpenAI")
@mock.patch("app.database_query.SQLDatabase")
@mock.patch("app.database_query.create_sql_agent")
@mock.patch("app.database_query.SQLDatabaseToolkit")
def test_database_query_query_failure(
    mock_sql_database_toolkit,
    mock_create_sql_agent,
    mock_sql_database,
    mock_open_ai,
):
    mock_sql_agent = mock.MagicMock()
    mock_sql_agent.run.side_effect = Exception("Error")
    mock_create_sql_agent.return_value = mock_sql_agent
    mock_prompt = "prompt"

    setattr(mock_sql_database, "from_uri", mock.Mock())

    result = DatabaseQuery().query(mock_prompt)

    assert result == ERROR_MESSAGE
    mock_sql_agent.run.assert_called_once_with(mock_prompt)
