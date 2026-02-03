from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction

from store.models import Book, Author, BookAuthor, Publisher, Tag, BookTag, BookImage, Category


class Command(BaseCommand):
    help = "Seed initial data: categories + books + authors + etc."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")

        # 0) Categories
        cats_data = [
            {"name": "Fiction", "slug": "fiction"},
            {"name": "Non-Fiction", "slug": "non-fiction"},
            {"name": "Science", "slug": "science"},
            {"name": "History", "slug": "history"},
            {"name": "Self-Help", "slug": "self-help"},
        ]
        categories = {}
        for c in cats_data:
            obj, _ = Category.objects.get_or_create(
                slug=c["slug"],
                defaults={"name": c["name"]}
            )
            categories[c["name"]] = obj
        
        # 1) Authors
        authors_data = [
            {"name": "Haruki Murakami", "bio": "Japanese writer.", "photoUrl": "https://example.com/murakami.jpg"},
            {"name": "George Orwell", "bio": "English novelist.", "photoUrl": "https://example.com/orwell.jpg"},
            {"name": "J.K. Rowling", "bio": "British author.", "photoUrl": "https://example.com/rowling.jpg"},
            {"name": "Yuval Noah Harari", "bio": "Historian and author.", "photoUrl": "https://example.com/harari.jpg"},
            {"name": "Dale Carnegie", "bio": "American writer.", "photoUrl": "https://example.com/carnegie.jpg"},
        ]

        authors = {}
        for a in authors_data:
            obj, _ = Author.objects.get_or_create(
                name=a["name"],
                defaults={"bio": a["bio"], "photoUrl": a["photoUrl"]},
            )
            authors[obj.name] = obj

        # 2) Books
        # Mapped to category names
        books_data = [
            {"title": "Norwegian Wood", "isbn": "9780375704024", "price": Decimal("12.50"), "stock": 50,
             "description": "A nostalgic story of loss and sexuality.", "category": "Fiction"},
            {"title": "Kafka on the Shore", "isbn": "9781400079278", "price": Decimal("14.00"), "stock": 40,
             "description": "A metaphysical mind-bender crossing realities.", "category": "Fiction"},
            {"title": "1984", "isbn": "9780451524935", "price": Decimal("10.99"), "stock": 80,
             "description": "A dystopian novel about surveillance and control.", "category": "Fiction"},
            {"title": "Animal Farm", "isbn": "9780451526342", "price": Decimal("8.99"), "stock": 90,
             "description": "A political satire of revolution and corruption.", "category": "Fiction"},
            {"title": "Harry Potter and the Sorcerer's Stone", "isbn": "9780590353427", "price": Decimal("11.99"), "stock": 120,
             "description": "A young wizard discovers his destiny.", "category": "Fiction"},
            {"title": "Harry Potter and the Chamber of Secrets", "isbn": "9780439064873", "price": Decimal("12.99"), "stock": 110,
             "description": "Mystery deepens at Hogwarts.", "category": "Fiction"},
            {"title": "Sapiens", "isbn": "9780062316110", "price": Decimal("16.50"), "stock": 70,
             "description": "A brief history of humankind.", "category": "History"},
            {"title": "Homo Deus", "isbn": "9780062464316", "price": Decimal("17.50"), "stock": 65,
             "description": "A look into the future of humanity.", "category": "History"},
            {"title": "How to Win Friends and Influence People", "isbn": "9780671027032", "price": Decimal("9.99"), "stock": 100,
             "description": "Classic self-improvement and communication.", "category": "Self-Help"},
            {"title": "The Art of Public Speaking", "isbn": "9781439164491", "price": Decimal("10.50"), "stock": 55,
             "description": "Fundamentals of effective public speaking.", "category": "Self-Help"},
        ]

        books = {}
        for b in books_data:
            cat = categories.get(b.get("category"))
            obj, created = Book.objects.get_or_create(
                isbn=b["isbn"],
                defaults={
                    "title": b["title"],
                    "price": b["price"],
                    "stock": b["stock"],
                    "description": b["description"],
                    "categoryID": cat,
                },
            )
            
            # update category if needed
            if not created and cat:
                if obj.categoryID != cat:
                    obj.categoryID = cat
                    obj.save(update_fields=["categoryID"])

            books[obj.isbn] = obj

        # 3) BookAuthor links
        links = [
            ("9780375704024", "Haruki Murakami", "Author"),
            ("9781400079278", "Haruki Murakami", "Author"),
            ("9780451524935", "George Orwell", "Author"),
            ("9780451526342", "George Orwell", "Author"),
            ("9780590353427", "J.K. Rowling", "Author"),
            ("9780439064873", "J.K. Rowling", "Author"),
            ("9780062316110", "Yuval Noah Harari", "Author"),
            ("9780062464316", "Yuval Noah Harari", "Author"),
            ("9780671027032", "Dale Carnegie", "Author"),
            ("9781439164491", "Dale Carnegie", "Author"),
        ]

        created_links = 0
        for isbn, author_name, role in links:
            book = books[isbn]
            author = authors[author_name]
            _, created = BookAuthor.objects.get_or_create(
                bookID=book,
                authorID=author,
                defaults={"role": role},
            )
            if created:
                created_links += 1

        # 4) Publishers
        publishers_data = [
            {"name": "Vintage", "address": "New York, USA", "website": "https://example.com/vintage"},
            {"name": "Penguin Books", "address": "London, UK", "website": "https://example.com/penguin"},
            {"name": "Scholastic", "address": "New York, USA", "website": "https://example.com/scholastic"},
            {"name": "Harper", "address": "New York, USA", "website": "https://example.com/harper"},
        ]
        for p in publishers_data:
            Publisher.objects.get_or_create(
                name=p["name"],
                defaults={"address": p["address"], "website": p["website"]},
            )

        # 5) Tags
        tags_data = [
            {"name": "Fiction", "colorCode": "#6c757d"},
            {"name": "Classic", "colorCode": "#0d6efd"},
            {"name": "Dystopian", "colorCode": "#dc3545"},
            {"name": "Fantasy", "colorCode": "#198754"},
            {"name": "Self-Help", "colorCode": "#ffc107"},
            {"name": "History", "colorCode": "#6610f2"},
            {"name": "Bestseller", "colorCode": "#dc3545"},
        ]
        tags = {}
        for t in tags_data:
            obj, _ = Tag.objects.get_or_create(
                name=t["name"],
                defaults={"colorCode": t["colorCode"]},
            )
            tags[obj.name] = obj

        # 6) BookTag
        book_tag_map = [
            ("9780375704024", ["Fiction", "Classic"]),
            ("9781400079278", ["Fiction"]),
            ("9780451524935", ["Classic", "Dystopian"]),
            ("9780451526342", ["Classic", "Dystopian"]),
            ("9780590353427", ["Fantasy", "Fiction", "Bestseller"]),
            ("9780439064873", ["Fantasy", "Fiction", "Bestseller"]),
            ("9780062316110", ["History", "Bestseller"]),
            ("9780062464316", ["History"]),
            ("9780671027032", ["Self-Help", "Bestseller"]),
            ("9781439164491", ["Self-Help"]),
        ]
        created_book_tags = 0
        for isbn, tag_names in book_tag_map:
            book = books[isbn]
            for tn in tag_names:
                tag = tags[tn]
                _, created = BookTag.objects.get_or_create(bookID=book, tagID=tag)
                if created:
                    created_book_tags += 1

        # 7) BookImage
        created_images = 0
        for isbn, book in books.items():
            thumb_url = f"https://picsum.photos/seed/{isbn}-thumb/400/600"
            extra_url = f"https://picsum.photos/seed/{isbn}-1/400/600"

            _, created1 = BookImage.objects.get_or_create(
                bookID=book,
                url=thumb_url,
                defaults={"isThumbnail": True},
            )
            _, created2 = BookImage.objects.get_or_create(
                bookID=book,
                url=extra_url,
                defaults={"isThumbnail": False},
            )
            created_images += int(created1) + int(created2)
        # 8) Staff User & Role
        from store.models import City, District, Address, User, Role, UserRole, StaffProfile
        # from django.contrib.auth.hashers import make_password # Custom auth uses plain text
        from django.utils import timezone

        self.stdout.write("Seeding Staff User...")
        
        # Create 'Staff' role
        staff_role, _ = Role.objects.get_or_create(
            name="Staff",
            defaults={"description": "Employee with access to warehouse and order management."}
        )

        # Create 'staff' user
        staff_user, created = User.objects.get_or_create(
            username="staff",
            defaults={
                "email": "staff@bookstore.com",
                "phone": "0909000001",
                "password": "1234", # stored as plain text per auth_controller
                "isActive": True,
                "lastLogin": timezone.now()
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created user: {staff_user.username}"))
        else:
            # Update password if user already exists to ensure it matches requirement
            staff_user.password = "1234"
            staff_user.save()
            self.stdout.write(f"Updated user: {staff_user.username}")

        # Assign Role
        UserRole.objects.get_or_create(
            userID=staff_user,
            roleID=staff_role,
            defaults={"assignedDate": timezone.now()}
        )

        # Create Staff Profile
        StaffProfile.objects.get_or_create(
            userID=staff_user,
            defaults={
                "employeeCode": "EMP001",
                "department": "Warehouse"
            }
        )

        # 9) Addresses
        self.stdout.write("Seeding Addresses...")
        hcm, _ = City.objects.get_or_create(name="Ho Chi Minh City", defaults={"code": "HCM"})
        hn, _ = City.objects.get_or_create(name="Ha Noi", defaults={"code": "HN"})

        # Districts
        districts_hcm = ["District 1", "District 3", "District 7", "Tan Binh", "Phu Nhuan"]
        hcm_objs = [District.objects.get_or_create(cityID=hcm, name=d)[0] for d in districts_hcm]

        # Districts
        districts_hn = ["Ba Dinh", "Hoan Kiem", "Cau Giay", "Dong Da"]
        hn_objs = [District.objects.get_or_create(cityID=hn, name=d)[0] for d in districts_hn]

        # Assign addresses to users
        all_districts = hcm_objs + hn_objs
        import random
        users = User.objects.all()
        created_addr = 0
        for u in users:
            # Create 1-2 addresses for each user
            for i in range(random.randint(1, 2)):
                dist = random.choice(all_districts)
                Address.objects.create(
                    userID=u,
                    street=f"Street {random.randint(1, 999)}",
                    districtID=dist,
                    isDefault=(i==0)
                )
                created_addr += 1

        self.stdout.write(self.style.SUCCESS("Seed completed ✅"))
        self.stdout.write(f"- Categories: {Category.objects.count()}")
        self.stdout.write(f"- Books: {Book.objects.count()}")
        self.stdout.write(f"- Addresses: {Address.objects.count()}")

        # 10) Carriers and Rates
        from store.models import Carrier, ShippingRate
        self.stdout.write("Seeding Carriers...")
        
        carriers_data = [
            {"name": "Giao Hàng Nhanh (GHN)", "apiKey": "ghn_demo_key", "hotline": "19001234"},
            {"name": "Giao Hàng Tiết Kiệm (GHTK)", "apiKey": "ghtk_demo_key", "hotline": "18005555"},
            {"name": "Viettel Post", "apiKey": "vtp_demo_key", "hotline": "19008095"},
        ]

        for c_data in carriers_data:
            carrier, created = Carrier.objects.get_or_create(
                name=c_data["name"],
                defaults={
                    "apiKey": c_data["apiKey"],
                    "hotline": c_data["hotline"]
                }
            )
            
            # Create Dummy Rates
            zones = ["Inner City", "Outer City", "National"]
            base_prices = {
                "Giao Hàng Nhanh (GHN)": 30000,
                "Giao Hàng Tiết Kiệm (GHTK)": 25000,
                "Viettel Post": 35000
            }
            
            price = base_prices.get(carrier.name, 30000)
            
            for zone in zones:
                ShippingRate.objects.get_or_create(
                    carrierID=carrier,
                    zone=zone,
                    minWeight=0.0,
                    defaults={"price": price}
                )
        self.stdout.write(f"- Carriers: {Carrier.objects.count()}")

