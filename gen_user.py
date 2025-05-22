from faker import Faker
import random

# Khởi tạo Faker để tạo dữ liệu giả
fake = Faker()

# Hàm để tạo ra một lệnh INSERT SQL với nhiều dòng dữ liệu
def generate_insert_statement_user(n):
    print(f"Đang tạo dữ liệu cho bảng user với {n} dòng dữ liệu...")
    values = []
    emails = set()  # Tập hợp để lưu trữ các email đã tạo
    for i in range(1, n + 1):
        # Tạo email duy nhất
        email = ''
        if i <= 10:
            email = f"a{i}@gmail.com"
        else:
            email = fake.email()
        while email in emails:
            email = fake.email()
        emails.add(email)  # Thêm email vào tập hợp
        # Các trường khác
        password = '$2b$10$/lOuHKj63QN/D7Vyc8s0V.m2ZHx6pLzpf0HkfNLufBaUKVsolhH3a' # Mật khẩu đã được mã hóa
        role = 'user'
        isActivated = True
        createdAt = fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S')
        updatedAt = createdAt

        # Thêm giá trị vào danh sách
        values.append(f"('{email}', '{password}', '{role}', {isActivated}, '{createdAt}', '{updatedAt}')")

    # Tạo câu lệnh INSERT duy nhất
    statement = (
        f"INSERT INTO \"user\" (\"email\", \"password\", \"role\", \"isActivated\", \"createdAt\", \"updatedAt\") VALUES \n"
        + ",\n".join(values)
        + ";"
    )
    print(f"Đã tạo {len(values)} dòng dữ liệu cho bảng user.")
    return statement

# Hàm tạo file SQL chứa lệnh INSERT
def create_sql_file_user(n, filename='insert_users.sql'):
    insert_statement = generate_insert_statement_user(n)

    # Tạo file .sql và ghi câu lệnh vào
    with open(filename, 'w') as file:
        file.write(insert_statement + '\n')
    
    print(f"Đã tạo file SQL với {n} dòng dữ liệu. File được lưu tại {filename}.")
