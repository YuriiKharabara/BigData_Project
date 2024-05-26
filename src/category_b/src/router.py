"""
The pages endpoints
"""

from fastapi import APIRouter, Query

from src import service
from src.handle_generic_exceptions import handle_and_raise_generic_exception

pages_router = APIRouter(prefix='/pages')


@handle_and_raise_generic_exception
@pages_router.get("/domains")
def get_domains() -> list:
    """
    Return the list of existing domains for which pages were created.

    :return: (list) - The existing domains for created pages.
    """
    domains = service.get_existing_domains()
    return domains


@handle_and_raise_generic_exception
@pages_router.get("")
def get_pages_by_user_id(user_id: int = Query(..., description="User ID.")) -> list:
    """
    Return all the pages which were created by the user with a specified user ID.

    :param user_id: (int) - The user ID.
    :return: (list) - The pages with specified user ID.
    """
    pages = service.get_pages_by_user_id(user_id)
    return pages


@handle_and_raise_generic_exception
@pages_router.get("/articles")
def get_articles_by_domain(domain: str = Query(..., description="Specified domain")) -> int:
    """
    Return the number of articles created for a specified domain.

    :param domain: (str) - Specified domain.
    :return: (int) - The number of articles.
    """
    articles = service.get_articles_by_domain(domain)
    return articles


@handle_and_raise_generic_exception
@pages_router.get("/page")
def get_page_by_id(page_id: int = Query(..., description="Page ID")) -> dict:
    """
    Return the page with the specified page ID.

    :param page_id: (int) - The page ID.
    :return: (dict) - The given page.
    """
    page = service.get_page_by_id(page_id)
    return page


@handle_and_raise_generic_exception
@pages_router.get("/users")
def get_users(start_time: str = Query(..., description="The start of period"),
              end_time: str = Query(..., description="The end of period")) -> list:
    """
    Return the id, name, and the number of created pages of all the users who created at least one page in a specified
    time range.

    :param start_time: (str) - The start of period.
    :param end_time: (str) - The end of period.
    :return: (list) - The received users.
    """
    users = service.get_users(start_time, end_time)
    return users
