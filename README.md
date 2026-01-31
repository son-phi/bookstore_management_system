# Bookstore Management System

Hướng dẫn cài đặt và chạy dự án Bookstore Management System.

## Yêu cầu hệ thống

- Python 3.8 trở lên
- pip (Python package installer)

## Các bước cài đặt

### 1. Cài đặt thư viện

Mở terminal tại thư mục `bookstore_management_system` và chạy lệnh sau để cài đặt Django:

```bash
pip install django
```

*(Lưu ý: Nếu bạn dùng virtual environment, hãy kích hoạt nó trước khi cài đặt)*

### 2. Di chuyển vào thư mục dự án

```bash
cd bookstore
```

(Thư mục chứa file `manage.py`)

### 3. Khởi tạo Database

Chạy các lệnh sau để tạo cấu trúc cơ sở dữ liệu:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Khởi tạo dữ liệu mẫu (Seed Data)

Dự án có sẵn script để tạo dữ liệu mẫu (Sách, Tác giả, Category, Địa chỉ, etc.):

```bash
python manage.py seed_data
```

*Lệnh này cũng sẽ tạo sẵn các User và Address mẫu cho bạn.*

### 5. Chạy Server

Khởi động server phát triển:

```bash
python manage.py runserver
```

Truy cập trang web tại: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Các tài khoản mẫu (nếu có từ seed_data)

Mặc định `seed_data` tạo dữ liệu ngẫu nhiên. Bạn có thể tự đăng ký tài khoản mới tại trang `/register/`.

### Lưu ý cho Staff
Để truy cập các chức năng quản lý (Staff), User cần có `StaffProfile`. Bạn có thể dùng admin hoặc shell để gán StaffProfile cho một user bất kỳ.

Ví dụ dùng Shell để tạo Staff:
```bash
python manage.py shell
```

```python
from store.models import User, StaffProfile
# Lấy user đầu tiên hoặc user bạn vừa tạo
u = User.objects.get(username="ten_user_cua_ban")
# Tạo profile nhân viên
StaffProfile.objects.create(userID=u, employeeCode="EMP001", department="Sales")
exit()
```
Sau đó đăng nhập lại user đó để thấy menu Staff.
