from app.db import get_db_connection
from app.entities.match import Match
from datetime import datetime
from app.db import get_db_connection

def create_match_request(player1_username, player2_username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO matches (
            player1_username,
            player2_username,
            match_state,
            start_time,
            end_time,
            winner_username,
            accepted
        ) VALUES (%s, %s, 'not_started', NULL, NULL, NULL, NULL)
        RETURNING match_id
    """, (player1_username, player2_username))
    match_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return match_id

def accept_match_request(match_id, player2_username):
    conn = get_db_connection()
    cur = conn.cursor()

    # Check if match exists, accepted is null and player2 matches
    cur.execute("""
        SELECT accepted, player2_username FROM matches
        WHERE match_id = %s
    """, (match_id,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return False, "Match not found"

    accepted, db_player2 = row
    if accepted is not None:
        cur.close()
        conn.close()
        return False, "Match already accepted or rejected"
    if db_player2 != player2_username:
        cur.close()
        conn.close()
        return False, "You are not authorized to accept this match"

    # Accept match: set accepted=true, match_state=on_going, start_time=now()
    cur.execute("""
        UPDATE matches
        SET accepted = TRUE,
            match_state = 'on_going',
            start_time = CURRENT_TIMESTAMP
        WHERE match_id = %s
    """, (match_id,))

    conn.commit()
    cur.close()
    conn.close()
    return True, "Match accepted"
