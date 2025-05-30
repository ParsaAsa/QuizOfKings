from app.db import get_db_connection
from app.entities.player import Player

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
