from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
 
def unauthenticated_admin(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated and request.session.get('_auth_user_backend') == 'backend.baseapp.backend.AdminBackend':
			return redirect('administrator')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func
 
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.session.get('_auth_user_backend') == 'backend.baseapp.backend.AdminBackend':
            return view_func(request, *args, **kwargs)
        else:   
            return redirect('adminlogin')

    return wrapper_func