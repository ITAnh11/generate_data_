from faker import Faker
import requests
import random
from gen_friend import friends
from gen_post import postIds

# Khởi tạo Faker để tạo dữ liệu giả
fake = Faker()
PEXELS_API_KEY='CNppo8oxrvcYTlNBPy1L9h1OtAXrn0596FJkbyTBG2idzIl89zCK7VSX'
VIDEO_URLS = []

def generate_random_image(width=400, height=300):
    return f"https://picsum.photos/id/{random.randint(1, 1000)}/{width}/{height}"

def fetch_video_urls_from_pexels(query='nature', per_page=15):
    print("Đang gọi API Pexels để lấy video...")
    url = f'https://api.pexels.com/videos/search?query={query}&per_page={per_page}'
    headers = {
        'Authorization': PEXELS_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        video_urls = []
        for video in data['videos']:
            # Lấy video chất lượng trung bình
            video_file = next((f for f in video['video_files'] if f['quality'] == 'sd' and f['file_type'] == 'video/mp4'), None)
            if video_file:
                video_urls.append(video_file['link'])
        return video_urls
    else:
        print(f"Lỗi khi gọi Pexels API: {response.status_code}")
        return []

# Hàm random URL video
def generate_random_video(list_video_urls):
    if list_video_urls:
        return random.choice(list_video_urls)
    else:
        # fallback nếu không gọi được API
        return 'https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4'


# Hàm để tạo ra một lệnh INSERT SQL với nhiều dòng dữ liệu
def generate_insert_statement_message(n):
    print(f"Đang tạo dữ liệu cho bảng user với {n} dòng dữ liệu...")
    VIDEO_URLS = fetch_video_urls_from_pexels()

    for i, friend in enumerate(friends):
        print(f"Người dùng {i+1} có {len(friend)} bạn bè.")
    values = []
    for i in range(1, n + 1):
        for j in friends[i-1]:
            for k in range(1, random.randint(5, 100)):
                senderId = i
                receiverId = j
                createdAt = fake.date_time_between(start_date='-30d', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
                status = random.choice(['sent', 'read'])
                is_reply_post = random.choices([True, False], weights=[0.1, 0.9])[0]
                postId = None
                mediaUrl = ''
                text = ''
                type = None  # Initialize type to avoid UnboundLocalError
                if is_reply_post:
                    type = 'text'
                    postId = random.choice(postIds[j-1])
                    text = fake.sentence(nb_words=random.randint(5, 10))
                else:
                    type = random.choices(['text', 'image', 'video'], weights=[0.7, 0.2, 0.1])[0]
                    if type == 'image':
                        mediaUrl = generate_random_image()
                    elif type == 'video':
                        mediaUrl = generate_random_video(VIDEO_URLS)
                    else:
                        text = fake.sentence(nb_words=random.randint(5, 10))
                # Use NULL for postId if it is None
                postId_value = f"'{postId}'" if postId is not None else "NULL"
                
                values.append(
                    f"({senderId}, {receiverId}, '{type}', '{text}', '{mediaUrl}', '{createdAt}', '{status}', {postId_value})"
                )

    # Tạo câu lệnh INSERT duy nhất
    statement = (
        f"INSERT INTO \"message\" (\"senderId\", \"receiverId\", \"type\", \"text\", \"mediaUrl\", \"createdAt\", \"status\", \"postId\") VALUES \n"
        + ",\n".join(values)
        + ";"
    )
    print(f"Đã tạo {len(values)} dòng dữ liệu cho bảng message.")
    return statement

# Hàm tạo file SQL chứa lệnh INSERT
def create_sql_file_user(n, filename='insert_users.sql'):
    insert_statement = generate_insert_statement_message(n)

    # Tạo file .sql và ghi câu lệnh vào
    with open(filename, 'w') as file:
        file.write(insert_statement + '\n')
    
    print(f"Đã tạo file SQL với {n} dòng dữ liệu. File được lưu tại {filename}.")
