
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from src.application.auth_module.api.views.auth.views import AuthView

router = DefaultRouter()
router.register(r'auth', AuthView, basename='auth')

urlpatterns = [
    path('', include(router.urls))
]