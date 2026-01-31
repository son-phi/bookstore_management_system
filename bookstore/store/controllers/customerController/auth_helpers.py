from typing import Optional
from django.http import HttpRequest
from store.models import User

SESSION_USER_KEY = "store_user_id"

def get_current_user(request: HttpRequest) -> Optional[User]:
    user_id = request.session.get(SESSION_USER_KEY)
    if not user_id:
        return None
    try:
        return User.objects.get(userID=user_id)
    except User.DoesNotExist:
        return None

def login_user(request: HttpRequest, user: User) -> None:
    request.session[SESSION_USER_KEY] = user.userID

def logout_user(request: HttpRequest) -> None:
    request.session.pop(SESSION_USER_KEY, None)

def customer_login_required(view_func):
    def _wrapped(request: HttpRequest, *args, **kwargs):
        user = get_current_user(request)
        if not user:
            # redirect login
            from django.shortcuts import redirect
            return redirect("/login/")
        request.current_user = user
        return view_func(request, *args, **kwargs)
    return _wrapped
