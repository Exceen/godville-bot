import requests
import json
import base64
import random
from time import sleep
from dotenv import load_dotenv
import os

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
load_dotenv(dotenv_path=ROOT_DIR + '/.env')


ACTION_PRIORITY = [
    {'action': 'punish', 'threshold': 75},
    # {'action': 'encourage', 'threshold': 75},
    # {'action': 'third_action', 'threshold': 75},
    {'action': 'to_dungeon', 'threshold': 50},
    {'action': 'to_sail', 'threshold': 50},
    {'action': 'to_royale', 'threshold': 50},
    # {'action': 'to_arena', 'threshold': 50},
]


def random_char():
    e = random.randint(0, 61)
    if e < 10:
        return str(e)
    elif e < 36:
        return chr(e + 55)  # A-Z
    else:
        return chr(e + 61)  # a-z


def random_string(length):
    return ''.join(random_char() for _ in range(length))


def encode_base64(s):
    text_bytes = s.encode('utf-8')
    base64_bytes = base64.b64encode(text_bytes)
    base64_string = base64_bytes.decode('utf-8')
    base64_string = base64_string.replace('=', '')
    return base64_string


def get_login_cookies():
    cookies = {}

    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    response = requests.post('https://godvillegame.com/login', data={
        'username': username,
        'password': password,
        'save_login': 'true',
        'commit': 'Login'
    })
    for c in response.cookies:
        cookies[c.name] = c.value

    response = requests.post('https://godvillegame.com/login/login', data={
        'username': username,
        'password': password,
        'save_login': 'true',
        'commit': 'Login'
    }, cookies=cookies)
    for c in response.cookies:
        cookies[c.name] = c.value

    cookies['gn'] = username

    return cookies


def get_all_info(cookies):
    response = requests.post('https://godvillegame.com/fbh/feed?a=GjZLI9oQGPkBZMqMMMP3KYBRVcqmu&cnt=-1', cookies=cookies)
    return response.json()


def do_action(cookies, action):
    action_dict = {'action': action}

    magic_values = {
        'action': 'YFQT8EtYAQwiIgmiUA2V',
        # 'type': 'N21ig4U1AbvfogpUb4AP', # 1
        # 'type': 'BhyjK8yaDXc6mKTI6do7', # 2
        # 'type': '3JaEcn7VbOq7sIs8koKn', # 3
    }

    k = list(action_dict.keys())[0]
    a = random_string(4) + magic_values[k] + random_string(5)
    b = random_string(5) + encode_base64(json.dumps(action_dict, separators=(',', ':'))) + random_string(3)

    body = {
        'a': a,
        'b': b,
    }

    print(action_dict, '->', body)

    response = requests.post('https://godvillegame.com/fbh/feed', cookies=cookies, data=body)
    try:
        return response.json()
    except Exception as e:
        raise e


def get_godpower(cookies):
    return int(get_all_info(cookies)['hero']['godpower'])


def get_action_availability(hero_info):
    action_availability = {}
    action_availability['punish'] = True
    action_availability['encourage'] = True
    action_availability['third_action'] = True

    action_availability['to_arena'] = hero_info['is_arena_available'] and not hero_info['is_arena_disabled']
    action_availability['to_dungeon'] = hero_info['d_a']
    action_availability['to_sail'] = hero_info['s_a']
    action_availability['to_royale'] = hero_info['r_a']

    return action_availability


def do_bot_action():
    cookies = get_login_cookies()
    all_info = get_all_info(cookies)
    action_availability = get_action_availability(all_info['hero'])

    if all_info['hero']['health'] == 0:
        do_action(cookies, 'resurrect')

    godpower = get_godpower(cookies)
    print('godpower:', str(godpower) + '%')

    if godpower < min([action['threshold'] for action in ACTION_PRIORITY]):
        print('Not enough godpower to do anything!')
        return

    for action in ACTION_PRIORITY:
        print('checking', action)
        if action_availability[action['action']]:
            while godpower >= action['threshold']:
                do_action(cookies, action['action'])
                print('executed', action['action'])
                godpower = get_godpower(cookies)



if __name__ == '__main__':
    do_bot_action()

