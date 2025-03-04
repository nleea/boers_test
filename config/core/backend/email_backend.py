from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views.decorators.debug import sensitive_variables

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    @sensitive_variables("username", "password")
    def authenticate(self, request, username, password, **kwargs):
        print(username,password)
        try:
            username_kwarg = kwargs.get("username", "")
            user = UserModel.objects.get(
                Q(username__iexact=username)
                | Q(email__iexact=username)
                | Q(email__iexact=username_kwarg)
            )
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return
        except UserModel.MultipleObjectsReturned:
            user = (
                UserModel.objects.filter(
                    Q(username__iexact=username) | Q(email__iexact=username)
                )
                .order_by("id")
                .first()
            )

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user