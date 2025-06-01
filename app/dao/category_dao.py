from app.entities.category import Category
from app.db import get_db_connection

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
