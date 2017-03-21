#!/usr/bin/env python
__author__ = 'mengwliu'

<<<<<<< HEAD
import os
=======
>>>>>>> 11d139878777230fd9fa88b29ed22ae181e972a4
import sys
import getopt
from smtplib import SMTP_SSL as smtp
from smtplib import SMTPException
from email.mime.text import MIMEText
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# This script is to automatically get WIFI password for clear-guest


def get_driver():
<<<<<<< HEAD
=======
    service_args = [
        '--proxy=www-proxy.us.oracle.com:80',
        '--proxy-type=html',
    ]
>>>>>>> 11d139878777230fd9fa88b29ed22ae181e972a4
    desired_capabilities = dict(selenium.webdriver.DesiredCapabilities.PHANTOMJS)
    desired_capabilities["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36")
    desired_capabilities["phantomjs.page.settings.Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"

<<<<<<< HEAD
    driver = selenium.webdriver.PhantomJS(desired_capabilities=desired_capabilities)
=======
    driver = selenium.webdriver.PhantomJS(service_args=service_args, desired_capabilities=desired_capabilities)
>>>>>>> 11d139878777230fd9fa88b29ed22ae181e972a4

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
    https_proxy = os.environ['https_proxy']
    http_proxy = os.environ['http_proxy']
    
    del os.environ['https_proxy']
    del os.environ['http_proxy']

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

    receivers = ["Sha Bi No.1 <yi.t.tian@oracle.com>", "Chao Shuai <mengwei.liu@oracle.com>"]
    #receivers = ["Mengwei Liu <mengwei.liu@oracle.com>"]
    sender = 'Larry Liu <mengwei.liu@oracle.com>'
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

    os.environ['https_proxy'] = https_proxy
    os.environ['http_proxy'] = http_proxy

if __name__ == "__main__":
   main(sys.argv[1:])


