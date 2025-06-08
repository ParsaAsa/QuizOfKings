from app.db import get_db_connection
from app.entities.player_stat import PlayerStat
from app.dao.player_dao import get_player_by_username
from typing import Optional

def get_player_stat_by_username(username: str) -> Optional[PlayerStat]:
    player = get_player_by_username(username)
    if not player:
        return None

    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch total_matches and wins
    cur.execute("""
        SELECT total_matches, wins
        FROM player_stat
        WHERE player_id = %s
    """, (player.player_id,))
    row = cur.fetchone()
    total_matches = row[0] if row else 0
    wins = row[1] if row else 0

    # Calculate accuracy
    cur.execute("""
        SELECT
            COUNT(*) FILTER (WHERE pa.player_answer = q.right_option)::FLOAT /
            NULLIF(COUNT(*), 0) AS accuracy
        FROM player_answer pa
        JOIN questions q ON pa.question_id = q.question_id
        WHERE pa.player_id = %s
          AND pa.player_answer IS NOT NULL;
    """, (player.player_id,))
    acc_row = cur.fetchone()
    accuracy = acc_row[0] if acc_row and acc_row[0] is not None else 0.0

    cur.close()
    conn.close()

    return PlayerStat(
        player_id=player.player_id,
        total_matches=total_matches,
        wins=wins,
        accuracy=accuracy
    )
