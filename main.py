from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import pyotp
import time

def wait_until_elem_id_appear(driver, id_name, timeout=10):
    print("Waiting for id={}".format(id_name))
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.presence_of_element_located((By.ID, id_name)))

def find_element_by_href_text(driver, href):
    return driver.find_element_by_xpath("//a[contains(@href, " + href + ")]")

if ("amazon_email" not in os.environ):
    exit("email not set")


if ("amazon_password" not in os.environ):
    exit("password not set")


if ("otp_key" not in os.environ):
    exit("otp not set")


# Set the Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("user-data-dir=/Users/wge/Library/Application Support/Google/Chrome/Default")


browser = webdriver.Chrome()
# browser.get('https://primenow.amazon.co.uk/home')
# postal_input = browser.find_element_by_id("lsPostalCode")
# postal_input.send_keys("SW7 5JN")
# postal_input.submit()
browser.get("https://primenow.amazon.co.uk/signin?returnUrl=https%3A%2F%2Fprimenow.amazon.co.uk%2Fhome")
email_input = browser.find_element_by_id("ap_email")
email_input.send_keys(os.environ["amazon_email"])
# Wait for some time so it loosk more like human
time.sleep(2)

password_input = browser.find_element_by_id("ap_password")
password_input.send_keys(os.environ["amazon_password"])
# Wait for some time so it loosk more like human
time.sleep(2)
password_input.submit()

totp = pyotp.TOTP(os.environ["otp_key"])
wait_until_elem_id_appear(browser, "auth-mfa-otpcode")
otp_input = browser.find_element_by_id("auth-mfa-otpcode")
otp_input.send_keys(totp.now())
otp_input.submit()

browser.get("https://primenow.amazon.co.uk/cart")
checkout_button = find_element_by_href_text(browser, "'/checkout/enter-checkout'")
checkout_button.click()

browser.minimize_window()

start_time = time.time()

while True:
    browser.refresh()
    try:
        no_slot_text = browser.find_elements_by_xpath("//span[contains(text(), 'No delivery windows for today or tomorrow')]")
    except:
        browser.maximize_window()
        place_order_in_earlest_slot(browser)
        break
    now = time.time()
    time.sleep(60)


print("This is the end of execution you should have a delivery slot.")

def place_order_in_earlest_slot(browser):
    time_slot = browser.find_element_by_xpath("//*[contains(text(), '00 PM']")
    time_slot.click()
    continue_button = browser.find_element_by_xpath("//*[contains(text(), 'Continue')]")
    continue_button.click()
    place_order_button = browser.find_element_by_xpath("//*[contains(text(), 'Place Your Order')]")
    place_order_button.click()