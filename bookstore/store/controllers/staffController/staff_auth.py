from django.shortcuts import redirect
from django.http import HttpRequest
from store.controllers.customerController.auth_helpers import get_current_user
from store.models import StaffProfile

def staff_login_required(view_func):
    def _wrapped(request: HttpRequest, *args, **kwargs):
        user = get_current_user(request)
        if not user:
            return redirect("/login/")

        # Debug log
        print(f"Staff Auth Check: User={user.username} (ID={user.userID})")
        
        # Check profile exists (explicit lookup)
        has_profile = StaffProfile.objects.filter(userID=user).exists()
        print(f" -> Has StaffProfile? {has_profile}")

        if not has_profile:
            # không phải staff
            return redirect("/books/")

        request.current_user = user
        return view_func(request, *args, **kwargs)
    return _wrapped
