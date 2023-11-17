from django.contrib.auth.backends import ModelBackend
from .models import UsersProfile
from django.contrib.auth import get_user_model


class PoliceIDBackend(ModelBackend):
    def authenticate(
            self,
            request,
            police_id=None,
            password=None,
            username=None,
            **kwargs
            ):
        User = get_user_model()

        try:
            if (
                User.objects.filter(username=username).exists() and
                User.objects.get(username=username).is_superuser
            ):
                user = User.objects.get(username=username)
            else:
                user_profile = UsersProfile.objects.get(police_id=police_id)
                user = user_profile.user

            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
