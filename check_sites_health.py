import argparse
import sys
import requests
import whois
from urllib.parse import urlparse
from datetime import date, datetime


MIN_EXPIRATION_DATE = 30


def create_parser():
    parser = argparse.ArgumentParser(description='Скрипт выполняет проверку \
                                     состояния сайтов.')
    parser.add_argument('-f', '--file', metavar='ФАЙЛ',
                        type=argparse.FileType('r'),
                        default='-',
                        help='Имя файла с URL адресами для проверки.')
    return parser


def is_server_respond_with_200(url):
    try:
        return requests.get(url, timeout=(5, 5)).status_code == \
               requests.codes.ok
    except requests.exceptions.RequestException:
        return False


def get_domain_expiration_date(domain_name):
    expiration_date = whois.whois(domain_name).expiration_date
    if expiration_date:
        if type(expiration_date) == datetime:
            return expiration_date.date()
        elif type(expiration_date) == list:
            return expiration_date[0].date()
    else:
        return None


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
    filepath = namespace.file
    url_list = filepath.read().splitlines()
    if not url_list:
        print('Скрипт не получил данных для обработки!',
              file=sys.stderr)
    for url in url_list:
        output_status_site(url)
