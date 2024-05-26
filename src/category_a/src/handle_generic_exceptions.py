import functools
from fastapi import HTTPException


def handle_and_raise_generic_exception(func):
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except Exception as e:
            if isinstance(e, HTTPException):
                raise
    return sync_wrapper
