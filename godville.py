import os
import random
from getpass import getpass
from sys import argv
from time import sleep
import logging

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert

from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
load_dotenv(dotenv_path=ROOT_DIR + '/.env')

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
logger = logging.getLogger(__name__)

RUNNING_AS_MAIN = False

def get_user_agent():
    r = requests.get(url="https://jnrbsn.github.io/user-agents/user-agents.json")
    r.close()
    if r.status_code == 200 and len(list(r.json())) > 0:
        agents = r.json()
        return list(agents).pop(random.randint(0, len(agents) - 1))
    else:
        return "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"


def get_credentials():
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    return username, password

def click_action_link(browser, text):
    try:
        clickable = browser.find_element(By.XPATH, f'//a[contains(text(), "{text}")]')
        if clickable is not None and clickable.is_displayed():
            browser.execute_script("window.confirm = function(){return true;}");
            clickable.click()

            print(f'"{text}" executed!')
            return True
    except NoSuchElementException:
        # print(text, 'not found')
        return False

    # print(text, 'may be invisible...')
    return False

def get_godpower():
    cookies = {}

    response = requests.post('https://godvillegame.com/login', data={
        'username': os.getenv('USERNAME'),
        'password': os.getenv('PASSWORD'),
        'save_login': 'true',
        'commit': 'Login'
    })
    for c in response.cookies:
        cookies[c.name] = c.value

    response = requests.post('https://godvillegame.com/login/login', data={
        'username': os.getenv('USERNAME'),
        'password': os.getenv('PASSWORD'),
        'save_login': 'true',
        'commit': 'Login'
    }, cookies=cookies)
    for c in response.cookies:
        cookies[c.name] = c.value

    cookies['gn'] = os.getenv('USERNAME')

    response = requests.post('https://godvillegame.com/fbh/feed?a=GjZLI9oQGPkBZMqMMMP3KYBRVcqmu&cnt=-1', cookies=cookies)

    json = response.json()

    return int(json['hero']['godpower'])



def do_bot_action():
    godpower = get_godpower()

    print('Godpower:', str(godpower) + '%')    
    if godpower < 50:
        print('Not enough godpower!')
        return

    # logger.info('Starting browser...')

    username, password = get_credentials()

    profile = FirefoxProfile()
    profile.set_preference("general.useragent.override", get_user_agent())
    browser_options = webdriver.FirefoxOptions()
    browser_options.add_argument("--headless")
    browser_options.profile = profile

    global RUNNING_AS_MAIN
    if RUNNING_AS_MAIN:
        import warnings
        warnings.filterwarnings("ignore", category=DeprecationWarning) 
        geckodriver_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'geckodriver')
        service = Service(executable_path=geckodriver_path, firefox_binary=FirefoxBinary('/Applications/Firefox.app/Contents/MacOS/firefox'), log_output="/dev/null")
    else:            
        service = Service(executable_path="/usr/local/bin/geckodriver", log_output="/dev/null")

    browser = webdriver.Firefox(options=browser_options, service=service)
    browser.set_window_size(1024, 768)

    try:
        browser.get('https://godvillegame.com')
        html = browser.page_source

        WebDriverWait(browser, 30).until(EC.text_to_be_present_in_element((By.NAME, 'username'), ''))
        mail_field = browser.find_element(By.NAME, 'username')
        mail_field.send_keys(username)

        WebDriverWait(browser, 30).until(EC.text_to_be_present_in_element((By.NAME, 'password'), ''))
        password_field = browser.find_element(By.NAME, 'password')
        password_field.send_keys(password)

        login_button = browser.find_element(By.NAME, 'commit')
        login_button.click()

        ## login done

        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'gp_val')))
        # godpower_element = browser.find_element(By.CLASS_NAME, 'gp_val')
        # godpower = int(''.join(filter(str.isdigit, godpower_element.text)))

        # print('Godpower:', str(godpower) + '%')
        sleep(2)
        # browser.implicitly_wait(5)

        # if godpower < 50:
        #     print('Not enough godpower!')
        #     return

        ## now we're talking...
        action_orders = [
            'Resurrect',
            'Explore Datamine',
            'Set Sail',
            'Drop to Dungeon',
            'Send to Arena',
        ]
        idle_orders = [
            'Punish',
            'Encourage',
            'Miracle',
        ]

        something_done = False
        for order in action_orders:
            if click_action_link(browser, order):
                something_done = True
                break

        if not something_done:
            order = idle_orders[random.randint(0, len(idle_orders) - 1)]
            if not click_action_link(browser, order):
                print('nothing found to do...')

        # browser.implicitly_wait(5)
        sleep(5)
    except Exception as e:
        raise e
    finally:
        browser.quit()


if __name__ == "__main__":
    RUNNING_AS_MAIN = True
    do_bot_action()

