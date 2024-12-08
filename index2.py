from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import sys
import json
import re
import time as py_time

sys.stdout.reconfigure(encoding='utf-8')

# Khởi tạo trình duyệt
driver = webdriver.Chrome()

# Truy cập vào trang web
driver.get('https://www.threads.net/?xmt=AQGzu0Sm7KW8H5BukuX5_i9RqHdzM3WfUvwmWjCZ7QkYmbQ')
WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, 'div'))
)

# Lưu dữ liệu các bài viết
post_data = []

def get_data_from_page():
    # Lấy HTML trang sau khi tải xong
    html_content = driver.page_source

    # Phân tích HTML với BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all('div', class_='x78zum5')
    print(f"Số lượng bài viết thu thập được: {len(elements)}")

    if elements:
        for index, element in enumerate(elements):
            try:
                username = element.find('span', class_='x6s0dn4').text.strip()
                img = element.find('img', class_='xl1xv1r').get('src').strip()

                time_element = element.find('time', class_='x1rg5ohu')
                if time_element:
                    # Lấy giá trị văn bản trong thẻ time
                    time_str = time_element.text.strip()

                    try:
                        # Kiểm tra nếu time_str có dạng "h hours ago"
                        match = re.match(r"(\d+)h(\d+) hours ago", time_str)
                        if match:
                            hours = int(match.group(1))
                            minutes = int(match.group(2))
                            current_time = datetime.now()
                            time = current_time - timedelta(hours=hours, minutes=minutes)
                        else:
                            # Nếu không phải dạng "h hours ago", xử lý dữ liệu khác
                            time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.000Z')
                    except ValueError:
                        print(f"Dữ liệu thời gian không hợp lệ: {time_str}")
                        time = None
                else:
                    print(f"Không tìm thấy thẻ <a> với class 'x1i10hfl' trong phần tử {index + 1}")
                    time = None  # Nếu không có thẻ <a> với class, gán time là None

                # Xử lý content và comment (kiểm tra sự tồn tại trước khi lấy dữ liệu)
                content = element.find('div', class_='x1a6qonq')
                content_text = content.text.strip() if content else "No content"

                comment = element.find('span', class_='x1lliihq')
                comment_text = comment.text.strip() if comment else "No comments"

                post_data.append({
                    "author": username,
                    "image": img,
                    "time": time.isoformat() if time else None,  # Lưu ngày giờ theo định dạng ISO nếu có
                    "content": content_text,
                    "comment": comment_text,
                })

            except Exception as e:
                print(f"Không thể xử lý Element {index + 1}: {e}")
    else:
        print("Không tìm thấy phần tử nào với class 'x78zum5'.")

# Cuộn trang và lấy dữ liệu
def scroll_and_crawl():
    scroll_pause_time = 2  # Thời gian dừng lại sau mỗi lần cuộn để dữ liệu tải hoàn toàn
    last_height = driver.execute_script("return document.body.scrollHeight")  # Chiều cao trang ban đầu

    while True:
        get_data_from_page()  # Lấy dữ liệu từ trang hiện tại

        # Cuộn xuống dưới trang
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        py_time.sleep(scroll_pause_time)

        # Tính toán chiều cao trang mới
        new_height = driver.execute_script("return document.body.scrollHeight")

        # Nếu chiều cao không thay đổi, nghĩa là đã cuộn đến cuối trang
        if new_height == last_height:
            break
        last_height = new_height  # Cập nhật chiều cao trang

# Bắt đầu quá trình cuộn và thu thập dữ liệu
scroll_and_crawl()

# Lưu dữ liệu vào file JSON sau khi thu thập xong
with open('postsIT_data.json', 'w', encoding='utf-8') as f:
    json.dump(post_data, f, ensure_ascii=False, indent=4)

# Đóng trình duyệt sau khi hoàn thành
