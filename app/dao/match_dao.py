from app.db import get_db_connection
from app.entities.match import Match
from datetime import datetime
from app.db import get_db_connection
from typing import Optional

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

def accept_match_request(match_id, player2_username, accept):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT accepted, player2_username FROM matches
        WHERE match_id = %s
    """, (match_id,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return False, "Match not found"

    accepted_status, db_player2 = row
    if accepted_status is not None:
        cur.close()
        conn.close()
        return False, "Match already accepted or rejected"

    if db_player2 != player2_username:
        cur.close()
        conn.close()
        return False, "You are not authorized to accept or reject this match"

    if accept:
        cur.execute("""
            UPDATE matches
            SET accepted = TRUE,
                match_state = 'on_going',
                start_time = CURRENT_TIMESTAMP
            WHERE match_id = %s AND accepted IS NULL AND player2_username = %s
        """, (match_id, player2_username))
        conn.commit()
        msg = "Match accepted"
    else:
        cur.execute("""
            UPDATE matches
            SET accepted = false
            WHERE match_id = %s AND accepted IS NULL AND player2_username = %s
        """, (match_id, player2_username))
        conn.commit()
        msg = "Match rejected"


    cur.close()
    conn.close()
    return True, msg

def get_match_by_id(match_id: int) -> Optional[Match]:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT match_id, player1_username, player2_username, match_state,
               start_time, end_time, winner_username, accepted
        FROM matches
        WHERE match_id = %s
    """, (match_id,))

    row = cur.fetchone()
    print(len(row), row)
    cur.close()
    conn.close()

    print("Row:", row)
    print("Match fields:", Match.__annotations__)
    print("Expected field count:", len(Match.__annotations__))
    print("Row length:", len(row))

    if row:
        return Match(*row)
    return None
