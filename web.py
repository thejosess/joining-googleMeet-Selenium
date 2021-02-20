import selenium
import os
import time
import datetime
import random
import warnings
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

warnings.filterwarnings("ignore", category=DeprecationWarning)
print("Timestamp: " + datetime.datetime.now().strftime("%D  %H:%M:%S"))

AUTOMATION_FAILED = False
USE_FAILSAFE_PERCAUTIONS = True
CLASS_CODE = ""
EMAIL_ADDRESS = ""
AD_USERNAME = ""
AD_PASSWORD = ""
AUTH_TIMES = 2
URL_GOOGLE = "https://accounts.google.com/ServiceLogin?service=mail&passive=true&rm=false&continue=https://mail.google.com/mail/&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1#identifier"

options = Options()
options.headless = False
options.set_preference("permissions.default.microphone", 1)
options.set_preference("permissions.default.camera", 1)

profile = webdriver.FirefoxProfile()
# Absolute path to Firefox executable
binary = FirefoxBinary('/usr/lib/firefox/firefox-bin')
driver = webdriver.Firefox(profile, options=options, firefox_binary=binary)
driver.maximize_window()
driver.get(URL_GOOGLE)
print("Successfully loaded Google Authetication point! [Gmail]")

ptions = Options()
options.headless = False

if AUTOMATION_FAILED == False:
    for i in range(6):
        try:
            driver.find_element_by_id("identifierId").send_keys(EMAIL_ADDRESS)
            driver.find_element_by_id("identifierNext").click()
            print("Sucessfully uploaded email...")
            break
        except selenium.common.exceptions.NoSuchElementException:
            print("[ERROR]: Attempting to resend email address.")
            if USE_FAILSAFE_PERCAUTIONS:
                time.sleep(6)
            else:
                driver.implicitly_wait(6)
        except selenium.common.exceptions.WebDriverException as e:
            print("[ERROR]: Web driver error.\n[ERROR DETAILS]:", e)
            AUTOMATION_FAILED = True
            break

if AUTOMATION_FAILED == False:
    if AD_USERNAME == "" or AD_USERNAME == None:
        for i in range(6):
            try:
                driver.find_element_by_name("password").send_keys(AD_PASSWORD)
                driver.find_element_by_id("passwordNext").click()
                print("Sucessfully sent credentials...")
                break
            except selenium.common.exceptions.NoSuchElementException:
                print("[ERROR]: Attempting to find password input.")
                if USE_FAILSAFE_PERCAUTIONS:
                    time.sleep(6)
                else:
                    driver.implicitly_wait(6)
    else:
        for i in range(6) :
            try:
                inputElement = driver.find_element_by_id("username")
                inputElement.send_keys(EMAIL_ADDRESS)
                inputElement = driver.find_element_by_id("password")
                inputElement.send_keys(AD_PASSWORD)
                inputElement = driver.find_element_by_xpath("//input[@type='submit' and @value='Login']")
                inputElement.click()
                print("Sucessfully sent Active Directory credentials...")
                break
            except selenium.common.exceptions.NoSuchElementException:
                print("[ERROR]: Attempting to find active directory login elements.")
                if USE_FAILSAFE_PERCAUTIONS:
                    time.sleep(6)
                else:
                    driver.implicitly_wait(6)
            except selenium.common.exceptions.WebDriverException as e:
                print("[ERROR]: Web driver error.\n[ERROR DETAILS]:", e)
                AUTOMATION_FAILED = True
                break
time.sleep(3)
driver.refresh()
print("Loading Google Meets...")
driver.get("https://meet.google.com"+"/"+CLASS_CODE)

time.sleep(7)  # Ensure that the browser fully loads the next part.

for i in range(6):
    try:
        WebDriverWait(driver, 6).until(EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(),'Unirse ahora')]")))
        time.sleep(2)
        turn_off_mic_action = ActionChains(driver)
        turn_off_mic_action.key_down(Keys.CONTROL).send_keys(
            "d").key_up(Keys.CONTROL).perform()
        turn_off_camera_action = ActionChains(driver)
        turn_off_camera_action.key_down(Keys.CONTROL).send_keys(
            "e").key_up(Keys.CONTROL).perform()
        print("Sucessfully found landmark...turned off camera and microphone.")
        break
    except selenium.common.exceptions.TimeoutException:
        try:
            WebDriverWait(driver, 6).until(EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(),'Ask to join')]")))

            time.sleep(2)
            turn_off_mic_action = ActionChains(driver)
            turn_off_mic_action.key_down(Keys.CONTROL).send_keys(
                "d").key_up(Keys.CONTROL).perform()
            turn_off_camera_action = ActionChains(driver)
            turn_off_camera_action.key_down(Keys.CONTROL).send_keys(
                "e").key_up(Keys.CONTROL).perform()
            print("Sucessfully found landmark...turned off camera and microphone.")
            break
        except selenium.common.exceptions.TimeoutException:
            print("[ERROR]: Attempting to find landmark...")
            if USE_FAILSAFE_PERCAUTIONS:
                time.sleep(6)
            else:
                driver.implicitly_wait(6)

try:
    join_button = WebDriverWait(driver, 36).until(EC.presence_of_element_located(
        (By.XPATH, "//span[contains(text(),'Unirse ahora')]")))
    driver.execute_script("arguments[0].click();", join_button)
except selenium.common.exceptions.TimeoutException:
    try:
        join_button = WebDriverWait(driver, 36).until(EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(),'Solicitar unirse')]")))
        driver.execute_script("arguments[0].click();", join_button)
    except selenium.common.exceptions.TimeoutException:
        print("No se puede unir a Google Meet. Estas seguro de que el codigo es correcto?")
