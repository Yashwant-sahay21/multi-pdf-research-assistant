import sqlite3

DB_PATH = "chat_memory.db"


def get_chat_history(session_id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        WHERE session_id=?
        ORDER BY id ASC
        LIMIT 20
        """,
        (session_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    history = []

    for role, content in rows:

        history.append({
            "role": role,
            "content": content
        })

    return history


def add_message(
    session_id,
    role,
    content
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages (
            session_id,
            role,
            content
        )
        VALUES (?, ?, ?)
        """,
        (
            session_id,
            role,
            content
        )
    )

    conn.commit()
    conn.close()