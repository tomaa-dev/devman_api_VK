import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
import argparse


def get_shorten_link(short_link_params):
    short_link_url = 'https://api.vk.ru/method/utils.getShortLink'
    response = requests.get(short_link_url, params=short_link_params)
    response.raise_for_status()
    return response.json()["response"]["short_url"]


def get_cliсk_count(link_stats_params):
    link_stats_url = 'https://api.vk.ru/method/utils.getLinkStats'
    response = requests.get(link_stats_url, params=link_stats_params)
    response.raise_for_status()
    return response.json()["response"]["stats"][0]["views"]


def is_shorten_link(link_stats_params):
    response = requests.get('https://api.vk.ru/method/utils.getLinkStats', params=link_stats_params)
    response.raise_for_status()
    return 'response' in response.json() and 'stats' in response.json()['response']


def main():
    load_dotenv()
    vk_token = os.environ["VK_IMPLICIT_FLOW_TOKEN"]

    parser = argparse.ArgumentParser(description="Программа укорачивает ссылки")
    parser.add_argument('url', help='ссылка')
    args = parser.parse_args()

    user_url = args.url
    parsed_url = urlparse(user_url)

    short_link_params = {
        "access_token": vk_token,
        "url": user_url,
        "v": "5.199"
    }

    link_stats_params = {
        "access_token": vk_token,
        "key": parsed_url.path[1:],
        "interval": "forever",
        "interval_count": 1,
        "v": "5.199"
    }

    if is_shorten_link(link_stats_params):
        views_count = get_cliсk_count(link_stats_params)
        print("Количество кликов по ссылке:", views_count)
    else:
        shortened_url = get_shorten_link(short_link_params)
        print("Сокращенная ссылка:", shortened_url)


if __name__ == '__main__':
    main()