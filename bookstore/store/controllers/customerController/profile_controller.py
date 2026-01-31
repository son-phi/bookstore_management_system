from django.shortcuts import render, redirect
from store.models import Address, City, CustomerProfile, Order, StaffProfile, District
from .auth_helpers import customer_login_required

@customer_login_required
def profile_view(request):
    user = request.current_user
    profile = CustomerProfile.objects.filter(userID=user).first()
    staff_profile = StaffProfile.objects.filter(userID=user).first()
    addresses = Address.objects.filter(userID=user).select_related("districtID__cityID")
    orders = Order.objects.filter(userID=user).order_by("-orderID")
    return render(request, "customer/profile.html", {
        "user": user,
        "profile": profile,
        "staff_profile": staff_profile,
        "addresses": addresses,
        "orders": orders
    })

@customer_login_required
def profile_update(request):
    user = request.current_user
    if request.method == "GET":
        return redirect("/profile/")

    # Only update basic fields in User (table doesn't have profile fields here)
    user.email = request.POST.get("email", user.email)
    user.phone = request.POST.get("phone", user.phone)
    user.save(update_fields=["email", "phone"])
    return redirect("/profile/")

@customer_login_required
def address_add(request):
    user = request.current_user
    if request.method == "GET":
        # Get all districts, ordered by City then District Name
        districts = District.objects.select_related("cityID").order_by("cityID__name", "name")
        return render(request, "customer/address_add.html", {"districts": districts})

    street = request.POST.get("street", "").strip()
    district_id = request.POST.get("district_id", "").strip()
    is_default = bool(request.POST.get("isDefault"))

    if not street or not district_id:
        districts = District.objects.select_related("cityID").order_by("cityID__name", "name")
        return render(request, "customer/address_add.html", {"districts": districts, "error": "street/district required"})

    district = District.objects.get(districtID=int(district_id))

    if is_default:
        Address.objects.filter(userID=user, isDefault=True).update(isDefault=False)

    Address.objects.create(userID=user, street=street, districtID=district, isDefault=is_default)
    return redirect("/profile/")
