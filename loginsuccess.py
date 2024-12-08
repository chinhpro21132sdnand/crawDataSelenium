from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import sys

# Cấu hình để hỗ trợ in ký tự Unicode
sys.stdout.reconfigure(encoding='utf-8')

# Hàm lưu cookie vào file
def save_cookies(driver, filename):
    cookies = driver.get_cookies()
    if cookies:
        with open(filename, "w") as cookie_file:
            json.dump(cookies, cookie_file, indent=4)
        print("Cookie đã được lưu.")
    else:
        print("Không lấy được cookie.")

# Hàm nạp cookie từ file
def load_cookies(driver, filename):
    try:
        with open(filename, "r") as cookie_file:
            cookies = json.load(cookie_file)
        for cookie in cookies:
            if 'sameSite' not in cookie:
                cookie['sameSite'] = 'None'
            driver.add_cookie(cookie)
        print("Cookie đã được nạp.")
    except FileNotFoundError:
        print(f"Không tìm thấy file cookie: {filename}")

# Khởi tạo trình duyệt
driver = webdriver.Chrome()

# Truy cập trang đăng nhập
driver.get("https://www.threads.net/")
time.sleep(5)  # Đợi trang tải xong để lấy cookie

# Lưu cookie vào file
cookie_filename = "www.threads.net_23-11-2024.json"
save_cookies(driver, cookie_filename)

# Thêm cookie từ file
load_cookies(driver, cookie_filename)

# Làm mới trang để cookie có hiệu lực
driver.refresh()

# Kiểm tra đăng nhập
try:
    WebDriverWait(driver, 10).until(
         EC.presence_of_element_located((By.CSS_SELECTOR, "div.x1ypdohk"))
    )
    print("Đăng nhập thành công!")
except Exception as e:
    print(f"Không thể đăng nhập tự động. Lỗi: {e}")

# Đợi 3 phút trước khi đóng trình duyệt
time.sleep(3 * 60)

# Đóng trình duyệt
driver.quit()
