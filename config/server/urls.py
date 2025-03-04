"""
URL configuration for base_project_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
import environ

env = environ.Env()
base_prefix = "api/schema/"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('src.application.auth_module.api.urls')),
]

ENV = env("ENV")

if ENV == "prod":
    urlpatterns += [    
        path(f'{base_prefix}', SpectacularAPIView.as_view(), name='schema'),
        path(f'{base_prefix}/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')
    ]
else:
    urlpatterns += [    
        path(f'{base_prefix}', SpectacularAPIView.as_view(), name='schema'),
        path(f'{base_prefix}/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')
    ]


urlpatterns += [path('api/swagger/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')]