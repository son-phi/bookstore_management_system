
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookstore.settings")
django.setup()

from store.models import City, District

print("Seeding Districts...")

# Ensure Cities exist
hcm, _ = City.objects.get_or_create(name="Ho Chi Minh City", defaults={"code": "HCM"})
hn, _ = City.objects.get_or_create(name="Ha Noi", defaults={"code": "HN"})

# Create Districts for HCM
districts_hcm = ["District 1", "District 3", "District 7", "Tan Binh", "Phu Nhuan"]
for d in districts_hcm:
    District.objects.get_or_create(cityID=hcm, name=d)

# Create Districts for HN
districts_hn = ["Ba Dinh", "Hoan Kiem", "Cau Giay", "Dong Da"]
for d in districts_hn:
    District.objects.get_or_create(cityID=hn, name=d)

print("Done.")
