#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    """Fetch one page of users given a page size and offset."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """Generator that lazily fetches paginated data using one loop."""
    offset = 0
    while True:  # ✅ only one loop
        page = paginate_users(page_size, offset)
        if not page:
            return  # stop when no rows left
        yield page
        offset += page_size
