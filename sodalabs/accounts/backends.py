from sodalabs.accounts.models import Musiphile

class ModelBackend(object):
    """
    Override built in django backend so I can authenticate against email and password.
    """
    def authenticate(self, musiphile_email=None, password=None):
        try:
            user = Musiphile.objects.get(musiphile_email=musiphile_email)
            if user.check_password(password):
                return user

        except Musiphile.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            return Musiphile.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
