import requests
import json
import logging
import base64
import random
from time import sleep
from dotenv import load_dotenv
import os

from godville import get_login_cookies, get_all_info
from debug import get_location

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
logger = logging.getLogger(__name__)


def watch_diffs():
    cookies = get_login_cookies()

    EXCLUDED_KEYS = [
        'turn_progress',
        's_send_after',
        'diary_last',
        'health',
        'diary',
        'hero',
        'ctime',
        'news_from_field',
        'smap',
        'dmap',
        'r_map',
        'bs', # royale
        'imp_e', # somethign with royale?
        'inventory',

    ]

    all_info = get_all_info(cookies)
    location = get_location(all_info)

    logger.info('started in ' + location)

    prev_all_info = None
    prev_hero_info = None
    while True:
        all_info = get_all_info(cookies)
        hero_info = all_info['hero']

        location = get_location(all_info)
        hero_info['location'] = location

        if prev_all_info:
            for key in all_info:
                if key in EXCLUDED_KEYS:
                    continue

                if key in prev_all_info:
                    if key in all_info:
                        if all_info[key] != prev_all_info[key]:
                            logger.info(f"[A] DIFF {key}: {prev_all_info[key]} -> {all_info[key]}")
                    else:
                        logger.info(f"[A] REM  {key}: {prev_all_info[key]}")
                else:
                    logger.info(f"[A] NEW  {key}: {all_info[key]}")

        if prev_hero_info:
            for key in hero_info:
                if key in EXCLUDED_KEYS:
                    continue

                if key in prev_hero_info:
                    if key in hero_info:
                        if hero_info[key] != prev_hero_info[key]:
                            logger.info(f"[H] DIFF {key}: {prev_hero_info[key]} -> {hero_info[key]}")
                    else:
                        logger.info(f"[H] REM  {key}: {prev_hero_info[key]}")
                else:
                    logger.info(f"[H] NEW  {key}: {hero_info[key]}")



        prev_all_info = all_info
        sleep(5)
    

if __name__ == '__main__':
    watch_diffs()

