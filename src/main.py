from app.database_query import DatabaseQuery


def main():
    while True:
        text_input = input("User: ")
        database_query = DatabaseQuery()
        response = database_query.query(text_input)
        print(f"Agent: {response}")


if __name__ == '__main__':
    main()
