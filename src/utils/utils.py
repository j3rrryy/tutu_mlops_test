from functools import wraps

from sqlalchemy.exc import SQLAlchemyError

from exceptions import DatabaseException


def database_exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as exc:
            raise DatabaseException(exc)

    return wrapper
