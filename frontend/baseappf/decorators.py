from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.session.get('_auth_user_backend') == 'backend.teacher.backend.TeacherBackend':
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

 
def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        print(request.user.is_authenticated)
        if request.user.is_authenticated == True and request.session.get('_auth_user_backend') == 'backend.teacher.backend.TeacherBackend':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('logout') 

    return wrapper_func
