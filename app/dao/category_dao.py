from app.entities.category import Category
from app.db import get_db_connection
import random
from app.db import fetch_all

def create_category(title: str) -> Category:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO category (title)
        VALUES (%s)
        RETURNING category_id, title
    """, (title,))
    row = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return Category(category_id=row[0], title=row[1])

def get_category_by_title(title: str) -> Category:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT category_id, title FROM category WHERE title = %s
    """, (title,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return Category(category_id=row[0], title=row[1])
    return None

def get_random_unused_categories(match_id, limit=3):
    query = """
        SELECT category_id, title
        FROM category
        WHERE category_id NOT IN (
            SELECT DISTINCT category_id
            FROM rounds
            WHERE match_id = %s AND category_id IS NOT NULL
        )
        ORDER BY RANDOM()
        LIMIT %s
    """
    rows = fetch_all(query, (match_id, limit))
    return [dict(row) for row in rows]

def get_all_categories():
    query = """
        SELECT category_id, title
        FROM category
        ORDER BY title
    """
    rows = fetch_all(query)
    return [dict(row) for row in rows]