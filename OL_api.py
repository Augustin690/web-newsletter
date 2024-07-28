#!/usr/bin/env python3
from __future__ import print_function

import requests
import os
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URL_TO_MONITOR = "https://www.ol.fr/fr/fans/actualites"

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.message import EmailMessage


def gmail_send_message(content):
    SCOPES = ['https://mail.google.com/']

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content(content)

        message['To'] = 'augustin.curinier@gmail.com'
        message['From'] = 'augustin.curinier@gmail.com'
        message['Subject'] = 'NEWS OL'

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message


# configure webdriver
options = Options()
options.headless = True  # hide GUI
options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
options.add_argument("start-maximized")  # ensure window is full-screen

#

# configure chrome browser to not load images and javascript
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(
    # this will disable image loading
    "prefs", {"profile.managed_default_content_settings.images": 2}
)

# wait for page to load
gmail_send_message('coucouuuuu')
listt = []


def webpage_was_changed_2():
    driver = webdriver.Chrome(options=options)
    driver.get(URL_TO_MONITOR)

    # create the previous_content.txt if it doesn't exist
    if not os.path.exists("previous_content.txt"):
        open("previous_content.txt", 'w+', encoding="utf-8").close()

    filehandle = open("previous_content.txt", 'r', encoding="utf-8")
    previous_response_text = filehandle.read()
    filehandle.close()

    element = WebDriverWait(driver=driver, timeout=40).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          'body > app-root > main > app-article-list > div > div:nth-child(2) > app-news-highlighted-news > div > div.col-lg-8.col-md-12.col-sm-12.col-xs-12.dimStyle-left > app-news > div > a')))

    OL = driver.find_element(By.CSS_SELECTOR,
                             'body > app-root > main > app-article-list > div > div:nth-child(2) > app-news-highlighted-news > div > div.col-lg-8.col-md-12.col-sm-12.col-xs-12.dimStyle-left > app-news > div > a')

    print(OL.text)
    print(OL.get_attribute('href'))
    listt.append(OL.text + ' \n ' + OL.get_attribute('href'))

    if previous_response_text == OL.text:
        driver.quit()
        return False
    else:

        filehandle = open("previous_content.txt", 'w', encoding="utf-8")
        filehandle.write(OL.text)
        filehandle.close()
        driver.quit()
        return True


webpage_was_changed_2()
gmail_send_message(listt[0])