from app.db import get_db_connection
from app.entities.match import Match
from datetime import datetime
from typing import Optional
from app.db import fetch_all, fetch_one, execute_query
from flask import jsonify

def create_match_request(player1_username, player2_username):
    conn = get_db_connection()
    cur = conn.cursor()

    # Get player IDs from usernames
    cur.execute("SELECT player_id FROM players WHERE username = %s", (player1_username,))
    row1 = cur.fetchone()
    if not row1:
        cur.close()
        conn.close()
        raise ValueError("Player1 not found")
    player1_id = row1[0]

    cur.execute("SELECT player_id FROM players WHERE username = %s", (player2_username,))
    row2 = cur.fetchone()
    if not row2:
        cur.close()
        conn.close()
        raise ValueError("Player2 not found")
    player2_id = row2[0]

    # Insert match
    cur.execute("""
        INSERT INTO matches (
            player1_id,
            player2_id,
            match_state,
            start_time,
            end_time,
            winner_id,
            accepted
        ) VALUES (%s, %s, 'not_started', NULL, NULL, NULL, NULL)
        RETURNING match_id
    """, (player1_id, player2_id))

    match_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return match_id

def accept_match_request(match_id, player2_username, accept):
    conn = get_db_connection()
    cur = conn.cursor()

    # Get player2_id from username
    cur.execute("SELECT player_id FROM players WHERE username = %s", (player2_username,))
    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        return False, "Player not found"
    player2_id = row[0]

    cur.execute("""
        SELECT accepted, player2_id FROM matches
        WHERE match_id = %s
    """, (match_id,))
    result = cur.fetchone()
    if not result:
        cur.close()
        conn.close()
        return False, "Match not found"

    accepted_status, db_player2_id = result
    if accepted_status is not None:
        cur.close()
        conn.close()
        return False, "Match already accepted or rejected"

    if db_player2_id != player2_id:
        cur.close()
        conn.close()
        return False, "You are not authorized to accept or reject this match"

    if accept:
        cur.execute("""
            UPDATE matches
            SET accepted = TRUE,
                match_state = 'on_going',
                start_time = CURRENT_TIMESTAMP
            WHERE match_id = %s AND accepted IS NULL AND player2_id = %s
        """, (match_id, player2_id))
        msg = "Match accepted"
    else:
        cur.execute("""
            UPDATE matches
            SET accepted = FALSE
            WHERE match_id = %s AND accepted IS NULL AND player2_id = %s
        """, (match_id, player2_id))
        msg = "Match rejected"

    conn.commit()
    cur.close()
    conn.close()
    return True, msg

def get_match_by_id(match_id: int) -> Optional[Match]:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT match_id, player1_id, player2_id, match_state,
               start_time, end_time, winner_id, accepted
        FROM matches
        WHERE match_id = %s
    """, (match_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return Match(*row)
    return None

def update_match_state(match_id: int, state: str):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE matches
        SET match_state = %s
        WHERE match_id = %s
    """, (state, match_id))

    conn.commit()
    cur.close()
    conn.close()

# Get all ongoing matches for a player (as player1 or player2)
def get_ongoing_matches_by_username(username):
    query = """
        SELECT m.*, p1.username AS player1_username, p2.username AS player2_username
        FROM matches m
        JOIN players p1 ON m.player1_id = p1.player_id
        JOIN players p2 ON m.player2_id = p2.player_id
        WHERE m.match_state = 'on_going'
          AND (p1.username = %s OR p2.username = %s)
    """
    return [dict(row) for row in fetch_all(query, (username, username))]

# Get all done matches for a player
def get_done_matches_by_username(username):
    query = """
        SELECT m.*, p1.username AS player1_username, p2.username AS player2_username
        FROM matches m
        JOIN players p1 ON m.player1_id = p1.player_id
        JOIN players p2 ON m.player2_id = p2.player_id
        WHERE m.match_state = 'done'
          AND (p1.username = %s OR p2.username = %s)
    """
    return [dict(row) for row in fetch_all(query, (username, username))]

# Get all match requests (accept is null) for a player
def get_match_requests_by_username(username):
    query = """
        SELECT m.*, p1.username AS player1_username, p2.username AS player2_username
        FROM matches m
        JOIN players p1 ON m.player1_id = p1.player_id
        JOIN players p2 ON m.player2_id = p2.player_id
        WHERE m.accepted IS NULL
          AND p2.username = %s
    """
    return [dict(row) for row in fetch_all(query, (username,))]
