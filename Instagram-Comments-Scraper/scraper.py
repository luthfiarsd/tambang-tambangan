from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
import excel_exporter  # Assuming this is a custom module for exporting to Excel

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# Open Instagram login page
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(2)

# Log in with your credentials
username = driver.find_element(By.NAME, "username")
username.send_keys("dan.den.don_")  # Replace with your actual username
password = driver.find_element(By.NAME, "password")
password.send_keys("danish")  # Replace with your actual password
password.submit()

time.sleep(10)  # Adjust as needed based on network speed and page load times

# Open the Instagram post URL passed as an argument
driver.get(sys.argv[1])
time.sleep(4)

# Load comments
try:
    # Use a more robust CSS selector for the "Load more comments" button
    load_more_comment = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".XQXOT.pafy4.rhwb6.LFGsT._4EzTm")
        )
    )

    i = 0
    while load_more_comment.is_displayed() and i < int(sys.argv[2]):
        load_more_comment.click()
        time.sleep(7)
        load_more_comment = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".XQXOT.pafy4.rhwb6.LFGsT._4EzTm")
            )
        )
        print("Loaded more comments ", i)
        i += 1
except Exception as e:
    print(e)

# Extract usernames and comments
user_names = []
user_comments = []
comments = driver.find_elements(By.CLASS_NAME, "_6lAjh")

for comment in comments:
    username = comment.find_element(By.CLASS_NAME, "sqdOP.yWX7d._8A5w5.ZIAjV")
    content = comment.find_element(By.CLASS_NAME, "C4VMK").text.strip()
    user_names.append(username.text)
    user_comments.append(content)

# Assuming your export function is in excel_exporter module
excel_exporter.export(user_names, user_comments)

# Close the WebDriver session
driver.close()
