
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookstore.settings")
django.setup()

from store.models import User, StaffProfile

print("--- DEBUG STAFF PROFILES ---")
users = User.objects.all()
print(f"Total Users: {users.count()}")
for u in users:
    print(f"User: {u.username} (ID: {u.userID})")

print("\n--- PROFILES ---")
profiles = StaffProfile.objects.all()
print(f"Total StaffProfiles: {profiles.count()}")

for p in profiles:
    # Try accessing raw ID if possible
    raw_id = getattr(p, "userID_id", "N/A")
    try:
        u = p.userID
        print(f"Profile {p.profileID}: User={u.username} (ID: {u.userID}) / RawFK={raw_id} / Code={p.employeeCode}")
    except User.DoesNotExist:
        print(f"Profile {p.profileID}: User DOES NOT EXIST (RawFK={raw_id})")

print("----------------------------")
