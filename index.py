from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import json
import re
import time as py_time
import sys
sys.stdout.reconfigure(encoding='utf-8')
# Khởi tạo trình duyệt
driver = webdriver.Chrome()

# Truy cập vào trang web
driver.get('https://www.threads.net/')
WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, 'div'))
)

# Thêm cookies vào trình duyệt
with open("cookies.json", "r") as cookie_file:
    cookies = json.load(cookie_file)
    print(cookies,'cookies')

for cookie in cookies:
    driver.add_cookie(cookie)

# Làm mới trang để cookies có hiệu lực
driver.refresh()

# Lưu dữ liệu các bài viết
post_data = []

def get_data_from_page():
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all('div', class_='x1iyjqo2')
    print(f"Số lượng bài viết thu thập được: {len(elements)}")

    if elements:
        for index, element in enumerate(elements):
            try:
                username = element.find('span', class_='x1lliihq').text.strip()
                img = element.find('img', class_='xl1xv1r').get('src').strip()

                time_element = element.find('time', class_='x1rg5ohu')
                if time_element:
                    time_str = time_element.text.strip()
                    match = re.match(r"(\d+)h (\d+) minutes ago", time_str)
                    if match:
                        hours = int(match.group(1))
                        minutes = int(match.group(2))
                        current_time = datetime.now()
                        time = current_time - timedelta(hours=hours, minutes=minutes)
                    else:
                        match = re.match(r"(\d+) hours ago", time_str)
                        if match:
                            hours = int(match.group(1))
                            current_time = datetime.now()
                            time = current_time - timedelta(hours=hours)
                        else:
                            time = time_str
                else:
                    time = None

                content = element.find('div', class_='x1a6qonq')
                content_text = content.text.strip() if content else "No content"

                comment = element.find('div', class_='x6s0dn4')
                comment_text = comment.text.strip() if comment else "No comments"

                post_data.append({
                    "author": username,
                    "image": img,
                    "time": time if time else None,
                    "content": content_text,
                    "comment": comment_text,
                })

            except Exception as e:
                print(f"Không thể xử lý Element {index + 1}: {e}")

def scroll_and_crawl():
    scroll_pause_time = 3  # Tăng thời gian dừng sau mỗi lần cuộn
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        get_data_from_page()
        driver.execute_script("window.scrollTo(10, document.body.scrollHeight);")
        py_time.sleep(scroll_pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

scroll_and_crawl()

# Lưu dữ liệu vào file JSON
with open('postsIT_data3.json', 'w', encoding='utf-8') as f:
    json.dump(post_data, f, ensure_ascii=False, indent=4)

driver.quit()
