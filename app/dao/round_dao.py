from entities.round import Round
from db import get_db_connection

def create_round(match_id, round_number):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO rounds (match_id, round_number, round_state)
        VALUES (%s, %s, 'not_started')
        RETURNING round_id, match_id, round_number, round_state, turn_started_at
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
        SELECT round_id, match_id, round_number, round_state, turn_started_at
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
        RETURNING round_id, match_id, round_number, round_state, turn_started_at
    """, (new_state, match_id, round_number))

    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if row:
        return Round(*row)
    return None

def initialize_rounds_for_match(match_id):
    conn = get_db_connection()
    cur = conn.cursor()

    for round_number in range(1, 7):
        cur.execute("""
            INSERT INTO rounds (match_id, round_number, round_state)
            VALUES (%s, %s, 'not_started')
        """, (match_id, round_number))

    conn.commit()
    cur.close()
    conn.close()
