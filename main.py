from gen_user import generate_insert_statement_user
from gen_userprofile import generate_insert_statement_userprofile
from gen_post import generate_insert_statement_post
from gen_friend import generate_insert_statement_friend_request, generate_insert_statement_friend
from gen_message import generate_insert_statement_message
from gen_user import create_sql_file_user
from gen_userprofile import create_sql_file_userprofile
from gen_post import create_sql_file_post
from gen_friend import create_sql_file_friend

import time


# Hàm tạo file SQL chứa lệnh INSERT
def create_sql_file(n, filename):
    insert_statement_user = generate_insert_statement_user(n)
    insert_statement_userprofile = generate_insert_statement_userprofile(n)
    insert_statement_friend_request = generate_insert_statement_friend_request(n)
    insert_statement_friend = generate_insert_statement_friend(n)
    isert_statement_post = generate_insert_statement_post(n)
    insert_statement_message = generate_insert_statement_message(n)
    

    # Tạo file .sql và ghi câu lệnh vào
    with open(filename, 'w') as file:
        file.write(insert_statement_user + '\n')
        file.write(insert_statement_userprofile + '\n')
        file.write(insert_statement_friend_request + '\n')
        file.write(insert_statement_friend + '\n')
        file.write(isert_statement_post + '\n')
        file.write(insert_statement_message + '\n')
    
    print(f"Đã tạo file SQL với {n} dòng dữ liệu. File được lưu tại {filename}.")


number_user = 1000


start_time = time.time()
# create_sql_file_user(number_user, 'data/insert_users.sql')
# create_sql_file_userprofile(number_user, 'data/insert_userprofile.sql')
# create_sql_file_friend(number_user, 'data/insert_friend.sql')
# create_sql_file_post(number_user, 'data/insert_post.sql')
create_sql_file(number_user, 'data/data.sql')
end_time = time.time()
print(f"Thời gian thực hiện: {end_time - start_time} giây")