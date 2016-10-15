import argparse
import os.path
import sys
import requests
import whois
from urllib.parse import urlparse
from datetime import date


MIN_EXPIRATION_DATE = 30


def create_parser():
    parser = argparse.ArgumentParser(description='Скрипт выполняет проверку \
                                     состояния сайтов.')
    parser.add_argument('-f', '--file', metavar='ФАЙЛ',
                        help='Имя файла с URL адресами для проверки.')
    return parser


def get_url_list(filepath):
    with open(filepath, 'r') as f:
        return f.read().splitlines()


def is_server_respond_with_200(url):
    try:
        return requests.get(url, timeout=(5, 5)).status_code == \
               requests.codes.ok
    except requests.exceptions.RequestException:
        return False


def get_domain_expiration_date(domain_name):
    expiration_date = whois.whois(domain_name).expiration_date
    return expiration_date[0].date() if expiration_date else None


def is_paid_domain_name(domain_name):
    expiration_date = get_domain_expiration_date(domain_name)
    return (expiration_date - date.today()).days > MIN_EXPIRATION_DATE \
        if expiration_date else False


def output_status_site(url):
    print('{} \n\tHTTP статус 200: {} '
          '\n\tДоменное имя оплачено на месяц вперед: {}\n'
          .format(url,
                  is_server_respond_with_200(url),
                  is_paid_domain_name(urlparse(url).netloc)))


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    if namespace.file:
        filepath = namespace.file
    else:
        filepath = input('Введите текстовый файл с URL адресами '
                         'для проверки:\n')
    if not os.path.exists(filepath):
        print('Файл не существует!')
        sys.exit(1)
    url_list = get_url_list(filepath)
    for url in url_list:
        output_status_site(url)
