from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Configure the WebDriver (Make sure you have the correct path to your WebDriver)
driver = webdriver.Chrome()

# Open Instagram and login
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(3)

# Log in to Instagram
username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")

username_input.send_keys("forminingpurpose")
password_input.send_keys("anjaymabar")
password_input.send_keys(Keys.RETURN)

# Wait for the login process to complete
time.sleep(5)

# Navigate to the Instagram post
post_url = "https://www.instagram.com/folkative/p/C6Xz_-BP8Fo/"
driver.get(post_url)
time.sleep(3)

# Click on the comments to expand (if necessary)
try:
    comments_expander = driver.find_element(
        By.XPATH, '//button[contains(text(), "View all comments")]'
    )
    comments_expander.click()
    time.sleep(2)
except:
    pass

# Load all comments by scrolling
while True:
    try:
        load_more_button = driver.find_element(
            By.XPATH, '//button[contains(text(), "Load more comments")]'
        )
        load_more_button.click()
        time.sleep(2)
    except:
        break

# Extract comments
comments_elements = driver.find_elements(By.XPATH, '//div[@role="dialog"]//li//span')
comments = [comment.text for comment in comments_elements]

# Close the driver
driver.quit()

# Save comments to an Excel file using pandas
comments_df = pd.DataFrame(comments, columns=["Comment"])
comments_df.to_excel("instagram_comments.xlsx", index=False)

print("Comments have been saved to instagram_comments.xlsx")
