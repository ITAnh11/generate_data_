from faker import Faker
import requests
import random
from gen_friend import friends
from gen_post import postIds

# Khởi tạo Faker để tạo dữ liệu giả
fake = Faker()

LIST_EMOJIS = [
    '😀', '😂', '😍', '😎', '😢', '😡', '👍', '👎', '🎉', '❤️', 
    '🔥', '💔', '✨', '🌈', '🌟', '💯', '🙌', '👏', '🙏', '🤔',
]

# Hàm để tạo ra một lệnh INSERT SQL với nhiều dòng dữ liệu
def generate_insert_statement_react(n):

    values = []
    for i in range(1, n + 1):
        for j in friends[i-1]:
            for k in range(1, random.randint(5, 50)):
                userId = i
                postId = random.choice(postIds[j-1])
                createdAt = fake.date_time_between(start_date='-30d', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
        
                type = random.choice(LIST_EMOJIS)
            
                values.append(
                    f"({userId}, {postId}, '{type}', '{createdAt}')"
                )

    # Tạo câu lệnh INSERT duy nhất
    statement = (
        f"INSERT INTO \"react\" (\"userId\", \"postId\", \"type\", \"createdAt\") VALUES \n"
        + ",\n".join(values)
        + ";"
    )
    print(f"Đã tạo {len(values)} dòng dữ liệu cho bảng react.")
    return statement

# Hàm tạo file SQL chứa lệnh INSERT
def create_sql_file_user(n, filename='insert_users.sql'):
    insert_statement = generate_insert_statement_react(n)

    # Tạo file .sql và ghi câu lệnh vào
    with open(filename, 'w') as file:
        file.write(insert_statement + '\n')
    
    print(f"Đã tạo file SQL với {n} dòng dữ liệu. File được lưu tại {filename}.")
