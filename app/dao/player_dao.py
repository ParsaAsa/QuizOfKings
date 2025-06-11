from app.db import get_db_connection
from app.entities.player import Player
from app.db import fetch_all

def get_player_by_id(player_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT player_id, username, email, player_password, signup_date, player_role
        FROM players
        WHERE player_id = %s
    """, (player_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return Player(*row)
    return None

def create_player(username, email, player_password, player_role="normal"):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO players (username, email, player_password, signup_date, player_role)
        VALUES (%s, %s, %s, CURRENT_DATE, %s)
        RETURNING player_id
    """, (username, email, player_password, player_role))
    player_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return player_id

def get_player_by_username(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT player_id, username, email, player_password, signup_date, player_role
        FROM players
        WHERE username = %s
    """, (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return Player(*row)
    return None

def update_player_role(username: str, new_role: str) -> bool:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE players
        SET player_role = %s
        WHERE username = %s
    """, (new_role, username))

    updated = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    return updated > 0


def get_top_players_by_wins(limit=5):
    query = """
        SELECT p.player_id, p.username, p.player_role, COALESCE(wins.win_count, 0) AS wins
        FROM players p
        LEFT JOIN (
            SELECT winner_id, COUNT(*) AS win_count
            FROM matches
            WHERE winner_id IS NOT NULL
            GROUP BY winner_id
        ) wins ON p.player_id = wins.winner_id
        ORDER BY wins DESC
        LIMIT %s
    """
    rows = fetch_all(query, (limit,))
    return [dict(row) for row in rows]