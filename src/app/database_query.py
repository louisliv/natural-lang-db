from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit


class DatabaseQuery:
    def __init__(self) -> None:
        self.db = SQLDatabase.from_uri("sqlite:///database/sqlite-sakila.db")
        self.llm = OpenAI(temperature=0, verbose=False)
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        self.agent_executor = create_sql_agent(
            llm=self.llm,
            toolkit=self.toolkit,
            verbose=False,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )

    def query(self, prompt: str) -> str:
        try:
            result = self.agent_executor.run(prompt)
        except Exception as e:
            result = "This query could not be completed with this question. Please try again."

        return result
