"""
The service module
"""
import logging
from src.cassandra_db import session


def get_existing_domains() -> list:
    """
    Retrieve all unique domains for which pages have been created.

    :return: (list) - The list of unique domains for created pages.
    """
    query = "SELECT DISTINCT domain FROM pages_by_domain;"
    try:
        rows = session.execute(query)
        domains = [row.domain for row in rows]
        return domains
    except Exception as e:
        logging.error(f"Error retrieving domains: {e}")
        return []


def get_pages_by_user_id(user_id: int) -> list:
    """
    Retrieve all pages created by a specific user.

    :param user_id: (int) - The user ID.
    :return: (list) - The list of pages created by the specific user.
    """
    query = "SELECT * FROM pages_by_user WHERE user_id = %s;"
    try:
        rows = session.execute(query, [user_id])
        pages = [
            {'page_id': row.page_id, 'domain': row.domain, 'title': row.title, 'created_at': row.created_at} for
            row in rows]
        return pages
    except Exception as e:
        logging.error(f"Error retrieving pages for user {user_id}: {e}")
        return []


def get_articles_by_domain(domain: str) -> int:
    """
    Count the number of articles created for a specific domain.

    :param domain: (str) - The specified domain.
    :return: The number of articles for the domain.
    """
    query = "SELECT COUNT(*) AS article_count FROM pages_by_domain WHERE domain = %s;"
    try:
        row = session.execute(query, [domain]).one()
        return row.article_count
    except Exception as e:
        logging.error(f"Error counting articles for domain {domain}: {e}")
        return 0


def get_page_by_id(page_id: int) -> dict:
    """
    Retrieve details of a page given its ID.

    :param page_id: (int) - The page ID.
    :return: (list) - The given page.
    """
    query = "SELECT * FROM page_details WHERE page_id = %s;"
    try:
        row = session.execute(query, [page_id]).one()
        if row:
            return {'page_id': row.page_id, 'domain': row.domain, 'title': row.title, 'user_id': row.user_id}
    except Exception as e:
        logging.error(f"Error retrieving page with ID {page_id}: {e}")
    return {}


def get_users(start_time: str, end_time: str) -> list:
    """
    Retrieve all users who created at least one page within a specified time range.

    :param start_time: (str) - The start time of period.
    :param end_time: (str) - The end time of period.
    :return: (list) - The list of users with created pages in this time range.
    """
    query = "SELECT * FROM user_activity WHERE period_start >= %s AND period_end <= %s ALLOW FILTERING;"
    try:
        rows = session.execute(query, [start_time, end_time])
        users = [{'user_id': row.user_id, 'start_time': row.period_start, 'end_time': row.period_end,
                  'pages_count': row.pages_count} for row in rows]
        return users
    except Exception as e:
        logging.error(f"Error retrieving users between {start_time} and {end_time}: {e}")
        return []
