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


# def exit_with_error(message):
#     logger.info(str(message))
#     browser.quit()
#     exit(1)


def get_credentials():
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    return username, password


def main():
    logger.info('Starting browser...')

    username, password = get_credentials()

    profile = FirefoxProfile()
    profile.set_preference("general.useragent.override", get_user_agent())
    browser_options = webdriver.FirefoxOptions()
    # browser_options.add_argument("--headless")
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




        # main_text = 'Verfügbarkeit von Gemeinschaftsstrom'

        # WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.XPATH, f'//h4[contains(text(), "{main_text}")]')))
        # browser.implicitly_wait(2)
        # sleep(2)
        # WebDriverWait(browser, 120).until(EC.presence_of_element_located((By.XPATH, f'//h4[contains(text(), "{main_text}")]')))
        # main_div = browser.find_element(By.XPATH, f'//h4[contains(text(), "{main_text}")]')

        # parent_el = main_div.find_element(By.XPATH, '..')
        # while parent_el != None:
        #     if 'grid-column' in parent_el.get_attribute('style'):
        #         break
        #     parent_el = parent_el.find_element(By.XPATH, '..')

        # subelements = parent_el.find_elements(By.XPATH, './/h4')
        # subelements = [x for x in subelements if main_text not in str(x.text)]

        # if len(subelements) != 1:
        #     logger.warning('Unexpected number of subelements:', len(subelements))

        # availability_status = subelements[0].text


    except Exception as e:
        raise e
    finally:
        browser.quit()


if __name__ == "__main__":
    RUNNING_AS_MAIN = True
    main()

