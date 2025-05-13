from faker import Faker
import random

# Khởi tạo Faker để tạo dữ liệu giả
fake = Faker()
friend_requests = []
friends = [[] for _ in range(1002)]  # Khởi tạo danh sách bạn bè cho mỗi người dùng

# Hàm để tạo ra một lệnh INSERT SQL với nhiều dòng dữ liệu
def generate_insert_statement_friend_request(n):
    print(f"Đang tạo dữ liệu cho bảng friend_request với {n} dòng dữ liệu...")
    ###############
    values = []
    friend_request_set = set()  # Tập hợp để lưu trữ các yêu cầu kết bạn đã tạo
    
    for i in range(1, n):
        for j in range(1, random.randint(5, 40)):
            status = random.choices(
                        ['accepted', 'pending', 'rejected'], 
                        weights=[60, 30, 10], 
                        k=1
                    )[0]
            createdAt = fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S')
            senderId = i
            receiverId = random.randint(1, n)
            
            while senderId == receiverId or (senderId, receiverId) in friend_request_set:
                receiverId = random.randint(1, n)
            
            friend_request_set.add((senderId, receiverId))
            friend_request_set.add((receiverId, senderId))  # Đảm bảo không có yêu cầu kết bạn ngược lại
            friend_requests.append((senderId, receiverId, status, createdAt))  # Lưu vào danh sách friend_requests
                
            
            # Thêm giá trị vào danh sách
            values.append(f"('{status}', '{createdAt}', {senderId}, {receiverId})")

    # Tạo câu lệnh INSERT duy nhất
    statement = (
        f"INSERT INTO \"friend_request\" (\"status\", \"createdAt\", \"senderId\", \"receiverId\") VALUES \n"
        + ",\n".join(values)
        + ";"
    )
    print(f"Đã tạo {len(values)} dòng dữ liệu cho bảng friend_request.")
    return statement

def generate_insert_statement_friend(n):
    print(f"Đang tạo dữ liệu cho bảng friend với {n} dòng dữ liệu...")
    
    values = []
    # Duyệt qua danh sách friend_requests để tạo dữ liệu cho bảng friend
    for req in friend_requests:
        senderId, receiverId, status, createdAt = req
        
        if status == 'accepted':
            # Nếu trạng thái là accepted, thêm vào bảng friend
            userId = senderId
            friendId = receiverId
            createdAt = fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S')

            values.append(f"({userId}, {friendId}, '{createdAt}')")
            values.append(f"({friendId}, {userId}, '{createdAt}')")
            
            # Add friendId to the user's friend list
            friends[userId-1].append(friendId)
            friends[friendId-1].append(userId)
    
    print(f"Đã tạo {len(values)//2} dòng dữ liệu cho bảng friend.")
    # Tạo câu lệnh INSERT duy nhất
    statement = (
        f"INSERT INTO \"friend\" (\"userId\", \"friendId\", \"createdAt\") VALUES \n"
        + ",\n".join(values)
        + ";"
    )
    print(f"Đã tạo {len(values)//2} dòng dữ liệu cho bảng friend.")
    return statement

# Hàm tạo file SQL chứa lệnh INSERT
def create_sql_file_friend(n, filename):
    insert_statement_friend_request = generate_insert_statement_friend_request(n)
    insert_statement_friend = generate_insert_statement_friend(n)

    # Tạo file .sql và ghi câu lệnh vào
    with open(filename, 'w') as file:
        file.write(insert_statement_friend_request + '\n')
        file.write(insert_statement_friend + '\n')
    
    print(f"Đã tạo file SQL với {n} dòng dữ liệu. File được lưu tại {filename}.")


