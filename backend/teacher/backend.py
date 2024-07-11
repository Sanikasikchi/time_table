from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from .models import Teacher
  

class TeacherBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        customer_id = kwargs['username']
        password = kwargs['password']
        try:
            user = Teacher.objects.filter(email__contains=customer_id)[:1]
            user = user[0]
            if check_password(password, user.password) is True:
                return user
        # except user.DoesNotExist:
        except:
            print('TeacherBackend')
            pass

    def get_user(self, user_id):
        try:
            return Teacher.objects.get(pk=user_id)
        except Teacher.DoesNotExist:
            return None
