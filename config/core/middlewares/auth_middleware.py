"""
File in which we have the middleware for Django for Authenticating API requests
"""
import json
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import (
    InvalidToken,
    AuthenticationFailed,
    TokenBackendError,
    TokenError,
    exceptions,
)
from django.contrib.auth import get_user_model
import os
import re

User = get_user_model()

# Get JWT secret key
SECRET_KEY = os.environ.get("SECRET_OR_KEY")


class CustomMiddleware(MiddlewareMixin):

    """
    Custom Middleware Class to process a request before it reached the endpoint
    """

    def process_request(self, request):
        """
        Custom middleware handler to check authentication for a user with JWT authentication
        :param request: Request header containing authorization tokens
        :type request: Django Request Object
        :return: HTTP Response if authorization fails, else None
        """
        routes_free = [
            "/auth/login/",
            "/auth/register/",
            "/api/swagger/",
            "/favicon.ico",
            "/api/schema/",
            "/admin",
            "/auth/forget_password/",
            "/auth/change_password"
        ]

        match = re.search("|".join(routes_free), request.path)
        if match:
            return None

        jwt_token: str = request.headers.get("authorization", None)
        
        # If token Exists
        if jwt_token:
            try:
                tokenUser, _ = JWTAuthentication.authenticate(
                    JWTAuthentication(), request
                )
                user = tokenUser

                if not tokenUser.is_authenticated:
                    return HttpResponse(
                        json.dumps("Unauthorized"),
                        content_type="application/json",
                        status=401,
                    )

                if not user:
                    return HttpResponse(
                        json.dumps("Unauthorized"),
                        content_type="application/json",
                        status=401,
                    )

                request.user = tokenUser
                return None
            except (
                InvalidToken,
                AuthenticationFailed,
                TokenBackendError,
                TokenError,
                exceptions.ValidationError,
                exceptions.APIException,
                exceptions.PermissionDenied,
            ):
                return HttpResponse(
                        json.dumps("Unauthorized"),
                        content_type="application/json",
                        status=401,
                    )
            except Exception as e:
                return HttpResponse(e.args, status=400)
        else:
            return HttpResponse(
                        json.dumps("Unauthorized"),
                        content_type="application/json",
                        status=401,
                    )
