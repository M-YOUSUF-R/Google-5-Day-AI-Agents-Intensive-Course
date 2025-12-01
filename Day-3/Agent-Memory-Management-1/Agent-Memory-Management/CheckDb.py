import sqlite3

def check_data_in_db(db_name:str="my_agent_data.db"):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        result = cursor.execute(
            "select app_name, session_id, author, content from events"
        )
        print([_[0] for _ in result.description])
        for each in result.fetchall():
            print(each)

check_data_in_db()
