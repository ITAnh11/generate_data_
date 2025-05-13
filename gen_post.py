from faker import Faker
import random
import requests

# Khởi tạo Faker để tạo dữ liệu giả
fake = Faker()

PEXELS_API_KEY='CNppo8oxrvcYTlNBPy1L9h1OtAXrn0596FJkbyTBG2idzIl89zCK7VSX'
VIDEO_URLS = []
postIds = []

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
def generate_insert_statement_post(n):
    print(f"Đang tạo dữ liệu cho bảng post với {n} dòng dữ liệu...")
    VIDEO_URLS = fetch_video_urls_from_pexels()

    values = []
    for i in range(1, n + 1):
        list_my_postId = []
        length = random.randint(5, 100)
        for j in range(1, length):
            list_my_postId.append(i * length + j)
            type=random.choices(['image', 'video'], weights=[0.7, 0.3])[0]
            if type == 'image':
                userId = i
                caption = fake.sentence(nb_words=random.randint(5, 10))
                urlPublicImage = generate_random_image()
                pathImage = ''
                urlPublicVideo = ''
                publicIdVideo = ''
                hlsUrlVideo = ''
                createdAt = fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S')
                updatedAt = createdAt

            else:
                url_video = generate_random_video(VIDEO_URLS)
                userId = i
                caption = fake.sentence(nb_words=random.randint(5, 10))
                urlPublicImage = ''
                pathImage = ''
                urlPublicVideo = url_video
                publicIdVideo = ''
                hlsUrlVideo = url_video
                createdAt = fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S')
                updatedAt = createdAt

            postIds.append(list_my_postId) 
            values.append(f"('{caption}', '{type}', '{urlPublicImage}', '{pathImage}', '{urlPublicVideo}', '{publicIdVideo}', '{hlsUrlVideo}', '{createdAt}', '{updatedAt}', {userId})")

     # Tạo câu lệnh INSERT duy nhất
    statement = (
        f"INSERT INTO \"post\" (\"caption\", \"type\", \"urlPublicImage\", \"pathImage\", \"urlPublicVideo\", \"publicIdVideo\", \"hlsUrlVideo\", \"createdAt\", \"updatedAt\", \"userId\") VALUES \n"
        + ",\n".join(values)
        + ";"
    )
    print(f"Đã tạo {len(values)} dòng dữ liệu cho bảng post.")
    return statement
            

# Hàm tạo file SQL chứa lệnh INSERT
def create_sql_file_post(n, filename='insert_users.sql'):
    insert_statement = generate_insert_statement_post(n)

    # Tạo file .sql và ghi câu lệnh vào
    with open(filename, 'w') as file:
        file.write(insert_statement + '\n')
    
    print(f"Đã tạo file SQL với {n} dòng dữ liệu. File được lưu tại {filename}.")
