from faker import Faker
import random

# Khởi tạo Faker để tạo dữ liệu giả
fake = Faker()
def generate_random_image(width=400, height=300):
    return f"https://picsum.photos/id/{random.randint(1, 1000)}/{width}/{height}"

# Hàm để tạo ra một lệnh INSERT SQL với nhiều dòng dữ liệu
def generate_insert_statement_userprofile(n):
    print(f"Đang tạo dữ liệu cho bảng user_profile với {n} dòng dữ liệu...")
    values = []
    usernames = set()  # Tập hợp để lưu trữ các username đã tạo
    for i in range(1, n + 1):
        name = fake.name()
        
        # Tạo username duy nhất
        username = fake.user_name()
        while username in usernames:
            username = fake.user_name()
        usernames.add(username)  # Thêm username vào tập hợp
        
        phone = fake.phone_number()
        dob = fake.date_of_birth(minimum_age=1, maximum_age=70).strftime('%Y-%m-%d')
        urlPublicAvatar = generate_random_image()
        # Giả sử pathAvatar là một chuỗi rỗng hoặc có thể tạo một đường dẫn ngẫu nhiên
        pathAvatar = ''
        userId = i
        
        # Thêm giá trị vào danh sách
        values.append(f"('{name}', '{username}', '{phone}', '{dob}', '{urlPublicAvatar}', '{pathAvatar}', {userId})")

    # Tạo câu lệnh INSERT duy nhất
    statement = (
        f"INSERT INTO \"user_profile\" (\"name\", \"username\", \"phone\", \"dob\", \"urlPublicAvatar\", \"pathAvatar\", \"userId\") VALUES \n"
        + ",\n".join(values)
        + ";"
    )
    print(f"Đã tạo {len(values)} dòng dữ liệu cho bảng user_profile.")
    return statement
    
# Hàm tạo file SQL chứa lệnh INSERT
def create_sql_file_userprofile(n, filename):
    insert_statement = generate_insert_statement_userprofile(n)

    # Tạo file .sql và ghi câu lệnh vào
    with open(filename, 'w') as file:
        file.write(insert_statement + '\n')
    
    print(f"Đã tạo file SQL với {n} dòng dữ liệu. File được lưu tại {filename}.")
