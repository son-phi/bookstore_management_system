from django.shortcuts import render, redirect
from django.utils import timezone
from store.models import User
from .auth_helpers import login_user, logout_user, get_current_user

def register(request):
    if request.method == "GET":
        return render(request, "customer/register.html")

    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "").strip()
    email = request.POST.get("email", "").strip()
    phone = request.POST.get("phone", "").strip()

    if not username or not password:
        return render(request, "customer/register.html", {"error": "username/password required"})

    # simple uniqueness check
    if User.objects.filter(username=username).exists():
        return render(request, "customer/register.html", {"error": "username exists"})

    user = User.objects.create(
        username=username,
        password=password,  # demo only
        email=email,
        phone=phone,
        lastLogin=timezone.now(),
        isActive=True,
    )
    login_user(request, user)
    return redirect("/profile/")

def login(request):
    if request.method == "GET":
        return render(request, "customer/login.html")

    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "").strip()

    try:
        user = User.objects.get(username=username, password=password, isActive=True)
    except User.DoesNotExist:
        return render(request, "customer/login.html", {"error": "invalid credentials"})

    user.lastLogin = timezone.now()
    user.save(update_fields=["lastLogin"])
    login_user(request, user)
    return redirect("/books/")

def logout(request):
    logout_user(request)
    return redirect("/books/")

def whoami(request):
    user = get_current_user(request)
    return render(request, "customer/whoami.html", {"user": user})
