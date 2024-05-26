from fastapi import APIRouter, Query

from src import service
from src.handle_generic_exceptions import handle_and_raise_generic_exception

statistics_router = APIRouter(prefix='/statistics')


@handle_and_raise_generic_exception
@statistics_router.get("/hourly_aggregated_stats")
def get_statistics(
        n: int = Query(..., description="Number of hours to include in the report, excluding the last hour."
                       )):
    """
    Get proper statistics of domains for the last n - 1 hours.

    :param n: (int) - The number of hours.
    :return: (str) - Statistics for the given period.
    """
    statistics = service.get_last_n_hours(n)
    return statistics


@handle_and_raise_generic_exception
@statistics_router.get("/bot_creation_stats")
def get_statistics_by_bot(
        n: int = Query(..., description="Number of hours to include in the report, excluding the last hour."
                       )):
    """
    Get proper statistics for the last n - 1 hours created by bot.

    :param n: (int) - The number of hours.
    :return: (str) - Statistics for the given period with bot.
    """
    statistics = service.get_last_n_hours_by_bots(n)
    return statistics


@handle_and_raise_generic_exception
@statistics_router.get("/top_users")
def get_top_users(
        n: int = Query(..., description="Number of hours to include in the report, excluding the last hour."
                       )):
    """
    Get proper statistics for the last n - 1 hours

    :param n: (int) - The number of hours.
    :return: (str) - Statistics of top-20 users.
    """
    statistics = service.get_top_users(n)
    return statistics
