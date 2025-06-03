from app.db import get_db_connection
from app.entities.player_answer import PlayerAnswer
from app.db import get_db_connection
from app.dao.match_dao import get_match_by_id
from app.dao.player_dao import get_player_by_username

def initial_questions(match_id: int, round_number: int) -> list[PlayerAnswer]:
    conn = get_db_connection()
    cur = conn.cursor()

    # Get category_id from round
    cur.execute("""
        SELECT category_id FROM rounds
        WHERE match_id = %s AND round_number = %s
    """, (match_id, round_number))
    row = cur.fetchone()
    if not row:
        raise ValueError("Round not found")
    category_id = row[0]

    # Get 3 distinct confirmed questions
    cur.execute("""
        SELECT question_id FROM questions
        WHERE category_id = %s AND confirmed IS TRUE
        ORDER BY RANDOM()
        LIMIT 3
    """, (category_id,))
    question_ids = [r[0] for r in cur.fetchall()]
    if len(question_ids) < 3:
        raise ValueError("Not enough confirmed questions in this category")

    # Get both players from the match
    cur.execute("""
        SELECT player1_username, player2_username FROM matches
        WHERE match_id = %s
    """, (match_id,))
    row = cur.fetchone()
    if not row:
        raise ValueError("Match not found")
    usernames = [row[0], row[1]]

    # Get player_ids from usernames
    cur.execute("""
        SELECT username, player_id FROM players
        WHERE username IN %s
    """, (tuple(usernames),))
    player_ids = {r[0]: r[1] for r in cur.fetchall()}

    if len(player_ids) != 2:
        raise ValueError("One or both players not found")

    inserted_answers = []
    for i, qid in enumerate(question_ids, start=1):
        for username in usernames:
            player_id = player_ids[username]
            cur.execute("""
                INSERT INTO player_answer (
                    match_id, round_number, question_id, question_number, player_id
                ) VALUES (%s, %s, %s, %s, %s)
                RETURNING match_id, round_number, question_id, question_number, player_id, player_answer
            """, (match_id, round_number, qid, i, player_id))
            row = cur.fetchone()
            inserted_answers.append(PlayerAnswer(*row))

    conn.commit()
    cur.close()
    conn.close()
    return inserted_answers

def submit_answer_if_null(match_id, round_number, question_number, answer, username):
    conn = get_db_connection()
    cur = conn.cursor()

    # Get player_id from username
    cur.execute("SELECT player_id FROM players WHERE username = %s", (username,))
    result = cur.fetchone()
    if not result:
        raise ValueError("Player not found")
    player_id = result[0]

    # Check if the answer already exists and is not NULL
    cur.execute("""
        SELECT player_answer FROM player_answer
        WHERE match_id = %s AND round_number = %s AND question_number = %s AND player_id = %s
    """, (match_id, round_number, question_number, player_id))
    row = cur.fetchone()

    if row is None:
        raise ValueError("Answer record not found")
    if row[0] is not None:
        return False  # Already answered

    # Update with new answer
    cur.execute("""
        UPDATE player_answer
        SET player_answer = %s
        WHERE match_id = %s AND round_number = %s AND question_number = %s AND player_id = %s
    """, (answer, match_id, round_number, question_number, player_id))

    conn.commit()
    cur.close()
    conn.close()
    return True
