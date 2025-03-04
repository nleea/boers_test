from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    createdAt = models.DateField(auto_now_add=True, blank=True, null= True)
    updateAt = models.DateField(auto_now=True, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.pk)

    class Meta:
        abstract = True
        ordering = ['id']

class Person(BaseModel):
    fullname = models.CharField(max_length=150, blank=False, default="")
    email = models.EmailField(_("email address"), blank=False, default="")

    class Meta:
        verbose_name = "Persons"
        verbose_name_plural = "Persons"


class User(AbstractUser, BaseModel):
    username = models.CharField(blank=False, null=False, unique=True, max_length=256)
    password = models.CharField(max_length=100)
    person = models.ForeignKey(
        Person, on_delete=models.SET_NULL, blank=True, null=True, db_index=True
    )
    token = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Users"
        verbose_name_plural = "Users"
