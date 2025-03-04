
from threading import local

_local = local()

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _local.request = request
        response = self.get_response(request)
        return response

    @staticmethod
    def get_request():
        return getattr(_local, 'request', None)

