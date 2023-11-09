from django.contrib.auth.backends import ModelBackend
from .models import UsersProfile
from django.contrib.auth import get_user_model


class OfficerIDBackend(ModelBackend):
    def authenticate(self, request, officer_id=None, password=None, **kwargs):
        User = get_user_model()

        try:
            # Get the UserProfile object with the given officer_id
            user_profile = UsersProfile.objects.get(officer_id=officer_id)
            user = user_profile.user  # Access the related User object from UserProfile

            if user.check_password(password):
                return user  # Return the User if the password matches
        except User.DoesNotExist:
            return None  # If no user is found, return None
