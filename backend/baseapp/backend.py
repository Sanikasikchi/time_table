from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


class AdminBackend(ModelBackend):
    
    def authenticate(self, request, **kwargs):
        email = kwargs["username"]
        password = kwargs["password"]
        try:
            print('AdminBackend')
            user = User.objects.filter(email__contains=email.lower())[:1]
            user = user[0] 
            if check_password(password, user.password) is True:
                return user
            print('AdminBackend2')
        # except user.DoesNotExist:
        except:
            print('AdminBackend3')
            pass

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
