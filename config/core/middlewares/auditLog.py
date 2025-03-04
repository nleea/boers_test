from django.utils.deprecation import MiddlewareMixin
import threading

class AuditMiddleware(MiddlewareMixin):
    _thread_local = threading.local()

    def process_request(self, request):
        if hasattr(request, 'user'):
            self._thread_local.current_user = request.user
        else:
            self._thread_local.current_user = None

    @classmethod
    def get_current_user(cls):
        return getattr(cls._thread_local, 'current_user', None)