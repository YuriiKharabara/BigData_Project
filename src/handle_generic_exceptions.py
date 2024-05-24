import functools
import inspect

from fastapi import HTTPException


def handle_and_raise_generic_exception(func):
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except Exception as e:
            if isinstance(e, HTTPException):
                raise

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except Exception as e:
            if isinstance(e, HTTPException):
                raise

    # Check if the function is asynchronous (async)
    if inspect.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper
