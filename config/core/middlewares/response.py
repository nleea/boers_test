from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
import json
import re
import logging


class CustomResponseMiddleware(MiddlewareMixin):
    def process_response(self, request, response):

        if 'application/json' in response['Content-Type']:

            status_validos = [200,201,202,203,204,205,206,207,208,226]
            
            try:
                value = json.loads(response.content)
                if (response.status_code in status_validos):
                    data    = value
                    errors  = None
                else:     
                    data    = None
                    errors  = value

            except json.JSONDecodeError:
                data = None
                errors = None

            
            custom_response = {
                'status': response.status_code,
                'errors': errors,
                'data': data,   
                'method': request.method,
                'url': request.get_full_path()
            }

            return JsonResponse(custom_response, status=response.status_code)

        return response
