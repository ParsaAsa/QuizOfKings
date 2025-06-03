from app.entities.round import Round
from app.db import get_db_connection

def create_round(match_id, round_number):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO rounds (match_id, round_number, round_state)
        VALUES (%s, %s, 'not_started')
        RETURNING match_id, round_number, round_state, turn_started_at, category_id
    """, (match_id, round_number))

    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return Round(*row)

def get_round(match_id, round_number):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT match_id, round_number, round_state, turn_started_at, category_id
        FROM rounds
        WHERE match_id = %s AND round_number = %s
    """, (match_id, round_number))

    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return Round(*row)
    return None

def update_round_state(match_id, round_number, new_state):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE rounds
        SET round_state = %s
        WHERE match_id = %s AND round_number = %s
        RETURNING match_id, round_number, round_state, turn_started_at, category_id
    """, (new_state, match_id, round_number))

    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if row:
        return Round(*row)
    return None


def set_round_category(match_id, round_number, category_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE rounds
        SET category_id = %s
        WHERE match_id = %s AND round_number = %s
        RETURNING match_id, round_number, round_state, turn_started_at, category_id
    """, (category_id, match_id, round_number))

    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if row:
        return Round(*row)
    return None
