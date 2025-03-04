# urls.py

from django.urls import path, include

urlpatterns = [
    path('', include('src.application.auth_module.api.views.person.urls'), name='person'),
    path('', include('src.application.auth_module.api.views.user.urls'), name='user'),
    path('', include('src.application.auth_module.api.views.auth.urls'),name='auth'),
]
