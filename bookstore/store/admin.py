from django.contrib import admin
from store import models as m

# ===== customer domain (1–10, 44–48) =====
admin.site.register(m.User)
admin.site.register(m.Role)
admin.site.register(m.UserRole)
admin.site.register(m.Permission)
admin.site.register(m.CustomerProfile)
admin.site.register(m.StaffProfile)
admin.site.register(m.Address)
admin.site.register(m.City)
admin.site.register(m.District)
admin.site.register(m.Notification)
admin.site.register(m.Review)
admin.site.register(m.ReviewImage)
admin.site.register(m.Comment)
admin.site.register(m.Wishlist)
admin.site.register(m.WishlistItem)

# ===== book domain (11–19) =====
admin.site.register(m.Book)
admin.site.register(m.Category)
admin.site.register(m.Author)
admin.site.register(m.BookAuthor)
admin.site.register(m.Publisher)
admin.site.register(m.BookImage)
admin.site.register(m.Tag)
admin.site.register(m.BookTag)
admin.site.register(m.Language)

# ===== staff domain (20–24) =====
admin.site.register(m.Supplier)
admin.site.register(m.Warehouse)
admin.site.register(m.ImportSlip)
admin.site.register(m.ImportDetail)
admin.site.register(m.StockEntry)

# ===== order domain (25–31) =====
admin.site.register(m.Cart)
admin.site.register(m.CartItem)
admin.site.register(m.Order)
admin.site.register(m.OrderDetail)
admin.site.register(m.OrderStatus)
admin.site.register(m.OrderHistory)
admin.site.register(m.ReturnRequest)

# ===== support domain (32–38, 52) =====
admin.site.register(m.Payment)
admin.site.register(m.PaymentMethod)
admin.site.register(m.Transaction)
admin.site.register(m.Shipment)
admin.site.register(m.Carrier)
admin.site.register(m.ShippingRate)
admin.site.register(m.ShippingTrace)
admin.site.register(m.SystemConfig)

# ===== engagement domain (39–43, 49–51) =====
admin.site.register(m.Discount)
admin.site.register(m.Coupon)
admin.site.register(m.UserCoupon)
admin.site.register(m.Campaign)
admin.site.register(m.Banner)
admin.site.register(m.UserBehavior)
admin.site.register(m.RecModel)
admin.site.register(m.RecResult)
