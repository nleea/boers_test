from django.contrib import admin
from src.application.auth_module.models import (
    Person,
    User
)

admin.site.register(Person)
admin.site.register(User)
