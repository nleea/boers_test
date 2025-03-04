import functools
from abc import ABCMeta
from src.domain.error_handlres import ErrorHandler
from src.domain.exceptions_db import custom_exception_handler
from django.db.transaction import rollback

def format_method(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        try:
            result = method(*args, **kwargs)
            return result
        except Exception as e:
            rollback()
            custom_exception_handler(e, args)
            response = ErrorHandler.handle_error(e,args[0].repository.Model)
            return {"status":response["status"], "data": response["details"]}
    return wrapper


class ServiceMeta(ABCMeta):
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                attrs[attr_name] = format_method(attr_value)
        return super().__new__(cls, name, bases, attrs)