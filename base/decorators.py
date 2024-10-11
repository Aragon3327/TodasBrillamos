from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and getattr(request.user, 'es_admin', False):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('logout')
    return _wrapped_view
