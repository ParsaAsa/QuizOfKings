from app.db import get_db_connection
from app.entities.question import Question
from app.entities.question_accept import QuestionAccept
from typing import Optional
from app.db import fetch_all
def get_question_by_id(question_id: int) -> Question | None:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT question_id, question_text, right_option, difficulty,
               confirmed, option_A, option_B, option_C, option_D,
               category_id, author_id
        FROM questions
        WHERE question_id = %s
    """, (question_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return Question(*row)
    return None

def create_question(question: Question, player_role: str) -> Question:
    conn = get_db_connection()
    cur = conn.cursor()

    confirmed = True if player_role in ("admin", "manager") else None

    cur.execute("""
        INSERT INTO questions (
            question_text, right_option, difficulty,
            confirmed, option_A, option_B, option_C, option_D,
            category_id, author_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING question_id, question_text, right_option, difficulty,
                  confirmed, option_A, option_B, option_C, option_D,
                  category_id, author_id
    """, (
        question.question_text, question.right_option, question.difficulty,
        confirmed, question.option_A, question.option_B,
        question.option_C, question.option_D,
        question.category_id, question.author_id
    ))

    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return Question(*row)

def update_question(question: Question) -> Optional[Question]:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE questions SET
            question_text = %s,
            right_option = %s,
            difficulty = %s,
            option_A = %s,
            option_B = %s,
            option_C = %s,
            option_D = %s,
            category_id = %s
        WHERE question_id = %s
        RETURNING question_id, question_text, right_option, difficulty,
                  confirmed, option_A, option_B, option_C, option_D,
                  category_id, author_id
    """, (
        question.question_text, question.right_option, question.difficulty,
        question.option_A, question.option_B,
        question.option_C, question.option_D,
        question.category_id, question.question_id
    ))

    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return Question(*row) if row else None


    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return Question(*row) if row else None

def delete_question(question_id: int, player) -> bool:
    conn = get_db_connection()
    cur = conn.cursor()

    if player.player_role in ["admin", "manager"]:
        cur.execute("DELETE FROM questions WHERE question_id = %s RETURNING question_id", (question_id,))
    else:
        # Normal users can delete only their own unconfirmed questions
        cur.execute("""
            DELETE FROM questions
            WHERE question_id = %s AND author_id = %s AND confirmed IS NULL
            RETURNING question_id
        """, (question_id, player.player_id))

    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return row is not None

def accept_question(question_id: int, player_id: int, confirmed: bool) -> Optional[QuestionAccept]:
    conn = get_db_connection()
    cur = conn.cursor()

    # Get player role
    cur.execute("SELECT player_role FROM players WHERE player_id = %s", (player_id,))
    player_row = cur.fetchone()
    if not player_row or player_row[0] == 'normal':
        cur.close()
        conn.close()
        raise PermissionError("Only admins or managers can accept questions")

    # Get question and its author
    cur.execute("SELECT author_id FROM questions WHERE question_id = %s", (question_id,))
    q_row = cur.fetchone()
    if not q_row:
        cur.close()
        conn.close()
        raise ValueError("Question not found")

    author_id = q_row[0]
    if author_id == player_id:
        cur.close()
        conn.close()
        raise PermissionError("You cannot accept your own question")

    # Update question confirmed status
    cur.execute("""
        UPDATE questions
        SET confirmed = %s
        WHERE question_id = %s
    """, (confirmed, question_id))

    # Insert into question_accept
    cur.execute("""
        INSERT INTO question_accept (question_id, player_id, confirmed)
        VALUES (%s, %s, %s)
        ON CONFLICT (question_id, player_id) DO UPDATE SET confirmed = EXCLUDED.confirmed
        RETURNING question_id, player_id, confirmed
    """, (question_id, player_id, confirmed))

    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return QuestionAccept(*row)

def get_unconfirmed_questions():
    query = """
        SELECT q.question_id, q.question_text, q.right_option, q.difficulty,
               q.confirmed, q.option_A, q.option_B, q.option_C, q.option_D,
               q.category_id, q.author_id, c.title as category_title,
               p.username as author_username
        FROM questions q
        JOIN category c ON q.category_id = c.category_id
        JOIN players p ON q.author_id = p.player_id
        WHERE q.confirmed IS NULL
        ORDER BY q.question_id DESC
    """
    rows = fetch_all(query)
    return [dict(row) for row in rows]

def get_questions_for_round(match_id: int, round_number: int, player_id: int):
    query = """
        SELECT q.question_id, q.question_text, q.option_A, q.option_B, q.option_C, q.option_D,
               q.right_option, pa.question_number
        FROM player_answer pa
        JOIN questions q ON pa.question_id = q.question_id
        WHERE pa.match_id = %s AND pa.round_number = %s AND pa.player_id = %s AND pa.player_answer is null
        ORDER BY pa.question_number ASC
    """
    rows = fetch_all(query, (match_id, round_number, player_id))
    return [dict(row) for row in rows]
