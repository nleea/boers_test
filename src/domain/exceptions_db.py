# En exceptions_db.py
from rest_framework.views import exception_handler
from src.application.auth_module.models.errors import LogBase
from config.core.middlewares.request import RequestMiddleware
import traceback


def custom_exception_handler(exc, args):
    
    obj = args[0]  
    stack_trace = f"{obj.__class__.__module__}.{obj.__class__.__name__}"
    error_code = 500
    error_message = exc

    request = RequestMiddleware.get_request()
    request_path = request.path if request else "No request path available"

    LogBase.objects.create(
            status_code     =   error_code,
            message         =   error_message,
            stack_trace     =   stack_trace,
            request_path    =   request_path
        )
    
    response = {
        "message": error_message,
        "stack_trace":stack_trace
    }

    return response
