from asyncio import wait
import os
import random
import time
import re
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style

def print_header():
    print(Fore.BLUE + "         Shopee LiveBot BY.================== SOEGIDEV ================")
    print(Fore.BLUE + "         ")
    print("======Start======")

def setup_selenium(proxy_address=None):
    # Set path to Chrome WebDriver
    chrome_driver_path = r'../chromedriver.exe'

    # Configure Chrome options
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
  
    # Add proxy settings if provided
    if proxy_address:
        options.add_argument(f'--proxy-server={proxy_address}')

    # Specify the Chrome WebDriver executable path using Service
    service = webdriver.chrome.service.Service(executable_path=r'chromedriver.exe')

    # Launch browser
    bot = webdriver.Chrome(service=service, options=options)
    # Clear cache and cookies
    bot.delete_all_cookies()
    return bot

def generate_tracking_id(length=12):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_random_viewer():
    return random.randint(1, 100)

#https://id.shp.ee/42LRN3q
def input_data():
    try:
        user_id = input('(#) USER ID Anda : ')
        session_id = input('(#) Masukkan Session ID Live Anda : ')
        loop_count = int(input('(#) Jumlah Viewers: '))
        print("======== TOTAL VIEWERS =======")
        if loop_count <= 0:
            raise ValueError("Angka Viewers Harus Positif.")
        viewer = generate_random_viewer()
        tracking_id = generate_tracking_id()
        link_live = f"https://live.shopee.co.id/share?from=live&session={session_id}&share_user_id={user_id}&stm_medium=referral&stm_source=rw&uls_trackid={tracking_id}&viewer={viewer}#copy_link"
        return loop_count, link_live
    except ValueError as err:
        print("Invalid input:", err)
        return input_data()

def navigate_to_link(browser, link):
    try:
        browser.get(link)
    except Exception as err:
        print("Error Navigasi:", err)

def click_element(browser, selector, success_message=None):
    try:
        element = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, selector)))
        element.click()
        if success_message:
            print(success_message)
    except Exception as err:
        print("An error occurred while clicking the element:", err)

def get_viewer_count(browser, xpath):
    try:
        viewer_element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        viewer_text = viewer_element.text.strip()
        viewer_count = int(re.search(r'\d+', viewer_text).group())
        return viewer_count
    except Exception as err:
        print("Gagal Ambil Total Viewers:", err)
        return 0

print_header()
loop_count, link_live = input_data()
browser = setup_selenium()

# Loop to add viewers
for _ in range(loop_count):
    navigate_to_link(browser, 'https://shopee.co.id/buyer/login/qr')
    wait = WebDriverWait(browser, 60)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.shopee-avatar__img')))
    navigate_to_link(browser, link_live)
    
    # Get current viewer count
    current_viewer_count = get_viewer_count(browser, '//*[@id="share-scroll-container"]/div/div/div[3]/div[2]/div[2]/div[2]')
    print(Fore.GREEN + "Jumlah Viewer Sekarang ::>", current_viewer_count)
    
    # Add logic to increment viewer count if needed
    new_viewer_count = current_viewer_count + 100  # Corrected this line
    
    # Click the element to add viewer (if applicable)
    click_element(browser, '//*[@id="__next"]/div/div[2]/div[1]/div', "Berhasil Menambahkan VIewers !")
    wait = WebDriverWait(browser, 30)
    # Optional: Wait for a few seconds before proceeding to the next iteration
    time.sleep(3)  # Adjust the sleep time as needed

# Close the browser when finished
browser.quit()
