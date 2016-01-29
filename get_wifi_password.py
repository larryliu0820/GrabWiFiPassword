__author__ = 'mengwliu'
import urllib2
from BeautifulSoup import BeautifulSoup
import os
import stat
import zipfile
import re
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# This script is to automatically get WIFI password for clear-guest


def get_driver():
    download_url = "http://chromedriver.storage.googleapis.com/2.20/chromedriver_mac32.zip"
    directory = '/tmp/'
    filename = 'chromedriver_mac32.zip'
    if os.environ['PATH'].find('chromedriver') is -1 and not os.path.isfile(directory + 'chromedriver'):
        f = urllib2.urlopen(download_url)
        data = f.read()
        with open(directory + filename, "wb") as code:
            code.write(data)
        z = zipfile.ZipFile(directory + filename)
        z.extractall(directory)
        st = os.stat(directory + 'chromedriver')
        os.chmod(directory + 'chromedriver', st.st_mode | stat.S_IEXEC)

    chrome_driver = directory + 'chromedriver'

    chromeOptions = selenium.webdriver.ChromeOptions()
    prefs = {"download.default_directory": "/tmp/"}
    chromeOptions.add_experimental_option("prefs",prefs)

    driver = selenium.webdriver.Chrome(executable_path=chrome_driver, chrome_options=chromeOptions)
    return driver


def sign_in(driver):

    username_input = driver.find_element_by_id("sso_username")
    password_input = driver.find_element_by_id("ssopassword")

    username_input.send_keys("mengwei.liu@oracle.com")
    password_input.send_keys("APB89fUG")

    print ("Sign in with username and password.")
    elem = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "submit_btn"))
    )
    elem.click()


def main():
    driver = get_driver()
    url = "https://gmp.oracle.com/captcha/"
    driver.get(url)
    sign_in(driver)

    america_btn = driver.find_element_by_id("ext-gen18")
    america_btn.click()

    password_text = driver.find_element_by_id("ext-gen38")
    print password_text.text