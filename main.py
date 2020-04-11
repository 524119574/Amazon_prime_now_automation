import os
import pyotp
import time
import random
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger()


def wait_until_elem_id_appear(driver, id_name, timeout=10):
    print("Waiting for id={}".format(id_name))
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.presence_of_element_located((By.ID, id_name)))


def find_element_by_href_text(driver, href):
    return driver.find_element_by_xpath("//a[contains(@href, " + href + ")]")


def place_order_in_earliest_slot(browser):
    logging.info('Attempting to get a delivery slot')

    found_slot = False
    try:
        time_slot = browser.find_element_by_xpath("//*[contains(text(), '00 AM']")
        time_slot.click()
        found_slot = True
    except NoSuchElementException:
        pass

    if not found_slot:
        try:
            time_slot = browser.find_element_by_xpath("//*[contains(text(), '00 PM']")
            time_slot.click()
        except NoSuchElementException:
            log.error('No slots found.')
            return

    try:
        continue_button = browser.find_element_by_xpath("//*[contains(text(), 'Continue')]")
        continue_button.click()
    except NoSuchElementException:
        log.error("Could not find the 'Continue' button.")

    try:
        place_order_button = browser.find_element_by_xpath("//*[contains(text(), 'Place Your Order')]")
        place_order_button.click()
    except NoSuchElementException:
        log.error("Could not find the 'Place Your Order' button.")



def random_sleep_time(time):
    return time + random.randint(-time * 5, time * 5) / 10


if __name__ == "__main__":
    if ("amazon_email" not in os.environ):
        exit("email not set")


    if ("amazon_password" not in os.environ):
        exit("password not set")


    if ("otp_key" not in os.environ):
        exit("otp not set")

    # Set the Chrome options
    chrome_options = Options()
    chrome_options.headless=True

    browser = webdriver.Chrome(options=chrome_options)
    browser.get("https://primenow.amazon.co.uk/signin?returnUrl=https%3A%2F%2Fprimenow.amazon.co.uk%2Fhome")
    email_input = browser.find_element_by_id("ap_email")
    email_input.send_keys(os.environ["amazon_email"])
    # Wait for some time so it loosk more like human
    random_sleep_time(2)

    print("email entered")
    password_input = browser.find_element_by_id("ap_password")
    password_input.send_keys(os.environ["amazon_password"])
    # Wait for some time so it loosk more like human
    random_sleep_time(2)
    password_input.submit()
    print("password entered")

    totp = pyotp.TOTP(os.environ["otp_key"])
    wait_until_elem_id_appear(browser, "auth-mfa-otpcode")
    otp_input = browser.find_element_by_id("auth-mfa-otpcode")
    otp_input.send_keys(totp.now())
    otp_input.submit()
    print("otp entered")


    browser.get("https://primenow.amazon.co.uk/cart")
    checkout_button = find_element_by_href_text(browser, "'/checkout/enter-checkout'")
    checkout_button.click()

    # browser.minimize_window()

    while True:
        browser.refresh()
        try:
            no_slot_text = browser.find_elements_by_xpath("//span[contains(text(), 'No delivery windows for today or tomorrow')]")
        except:
            # browser.maximize_window()
            place_order_in_earliest_slot(browser)
            break
        now = time.time()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        random_sleep_time(60)

    print("This is the end of execution you should have a delivery slot.")