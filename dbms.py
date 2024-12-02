import sqlite3

# Create the Users table and update the Todo table to include user_id
conn = sqlite3.connect('todo.db')

create_users_query = """
CREATE TABLE IF NOT EXISTS Users (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE,
  password TEXT
);
"""

alter_todo_query = """
CREATE TABLE IF NOT EXISTS Todo (
  id INTEGER PRIMARY KEY,
  text TEXT,
  complete BOOLEAN,
  user_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES Users (id)
);
"""

conn.execute(create_users_query)
conn.execute(alter_todo_query)
conn.close()


def execute_query(sql_query, params=()):
    """
    Function to execute SQL commands.
    :return: Returns values if SELECT command is used
    """
    with sqlite3.connect("todo.db") as con:
        cur = con.cursor()
        result = cur.execute(sql_query, params)
        con.commit()
    return result


def create_user(username, password):
    """
    Add a new user to the database.
    """
    sql_query = "INSERT INTO Users (username, password) VALUES (?, ?)"
    execute_query(sql_query, (username, password))


def authenticate_user(username, password):
    """
    Authenticate user credentials.
    """
    sql_query = "SELECT * FROM Users WHERE username = ? AND password = ?"
    return execute_query(sql_query, (username, password)).fetchone()


def add_todo_item(text, user_id):
    """
    Add a todo item linked to a specific user.
    """
    sql_query = "INSERT INTO Todo (text, complete, user_id) VALUES (?, 0, ?)"
    execute_query(sql_query, (text, user_id))


def mark_complete(id):
    """
    Mark a todo item as complete.
    """
    sql_query = "UPDATE Todo SET complete = 1 WHERE id = ?"
    execute_query(sql_query, (id,))


def get_complete(user_id):
    """
    Get all completed todo items for a user.
    """
    sql_query = "SELECT * FROM Todo WHERE complete = 1 AND user_id = ?"
    return execute_query(sql_query, (user_id,)).fetchall()


def get_incomplete(user_id):
    """
    Get all incomplete todo items for a user.
    """
    sql_query = "SELECT * FROM Todo WHERE complete = 0 AND user_id = ?"
    return execute_query(sql_query, (user_id,)).fetchall()


def get_todo_by_id(id, user_id):
    """
    Get a specific todo item by ID and user_id.
    """
    sql_query = "SELECT * FROM Todo WHERE id = ? AND user_id = ?"
    return execute_query(sql_query, (id, user_id)).fetchone()


def update_todo_item(id, new_text):
    """
    Update the text of a todo item.
    """
    sql_query = "UPDATE Todo SET text = ? WHERE id = ?"
    execute_query(sql_query, (new_text, id))
