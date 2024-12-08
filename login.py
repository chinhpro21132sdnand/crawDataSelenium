from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Khởi tạo trình duyệt
driver = webdriver.Chrome()  # Hoặc bạn có thể sử dụng Firefox, Edge, v.v.

# Truy cập trang đăng nhập
driver.get("https://www.threads.net/login")

# Chờ trang tải xong (hoặc có thể thay bằng WebDriverWait)
time.sleep(2)  # Hoặc dùng WebDriverWait nếu muốn chính xác hơn

# Tìm và điền thông tin vào các trường đăng nhập
username_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "x1i10hfl"))
)  
username_field.send_keys("Phamtienchinh4@gmail.com")  # Thay 'your_username' bằng tên đăng nhập của bạn

password_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "x1i10hfl"))  # Thay x1i10hfl bằng class chính xác của trường mật khẩu
)
password_field.send_keys("Tienchinh1.")  # Thay 'your_password' bằng mật khẩu của bạn

# Tìm nút đăng nhập và nhấn vào đó
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div/div/div[1]/div[1]/div[3]/form/div/div[1]/div[2]/div[2]")))  # Đảm bảo nút đăng nhập có thể click
login_button.click()

# Đợi một chút để trang web tải sau khi đăng nhập
time.sleep(5)
cookies = driver.get_cookies()  # Lấy tất cả cookies hiện tại trong trình duyệt

# Lưu cookies vào tệp
with open("cookies.json", "w") as cookie_file:
    json.dump(cookies, cookie_file)
# Kiểm tra nếu đăng nhập thành công (Ví dụ kiểm tra URL hoặc một phần tử đặc biệt)
print(f"URL hiện tại: {driver.current_url}")

# Tiến hành các thao tác khác sau khi đăng nhập
# driver.get("https://www.example.com/after_login") # Ví dụ trang sau khi đăng nhập

# Đảm bảo không đóng trình duyệt ngay lập tức 
input("Nhấn Enter để đóng trình duyệt...")

# Đóng trình duyệt
driver.quit()
