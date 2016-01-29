__author__ = 'mengwliu'
import os
import sys
import stat
import getopt
import zipfile
import urllib2
from smtplib import SMTP_SSL as smtp
from smtplib import SMTPException
from email.mime.text import MIMEText
import selenium
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


def sign_in(driver, username, password):

    username_input = driver.find_element_by_id("sso_username")
    password_input = driver.find_element_by_id("ssopassword")

    username_input.send_keys(username)
    password_input.send_keys(password)

    print ("Sign in with username and password.")
    elem = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "submit_btn"))
    )
    elem.click()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hu:p:",["user=","pass="])
    except getopt.GetoptError:
        print 'get_wifi_password.py -u <username> -p <password>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'get_wifi_password.py -u <username> -p <password>'
            sys.exit()
        elif opt in ("-u", "--user"):
            username = arg
        elif opt in ("-p", "--pass"):
            password = arg

    driver = get_driver()
    url = "https://gmp.oracle.com/captcha/"
    driver.get(url)

    sign_in(driver, username, password)

    america_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ext-gen18"))
    )
    america_btn.click()

    password_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ext-gen38"))
    )

    text = password_text.text
    driver.quit()

    for line in text.split("\n"):
        if "Password" in line:
            mima = line.split(" ")[1]

    print mima

    # receivers = ["yi.t.tian@oracle.com", "shang.dang@oracle.com", "mengwei.liu@oracle.com"]
    receivers = ["Mengwei Liu <mengwei.liu@oracle.com>"]
    sender = 'Mengwei Liu <mengwei.liu@oracle.com>'
    try:
        conn = smtp('stbeehive.oracle.com')
        conn.login(username, password)
        msg = MIMEText(mima)
        msg['Subject'] = "clear-guest mima"
        msg['From'] = sender
        msg['To'] = ",".join(receivers)
        conn.sendmail(sender, receivers, msg.as_string())
        print "Successfully sent email"
    except SMTPException as e:
        print e.message
        print "Error: unable to send email"
    finally:
        conn.close()


