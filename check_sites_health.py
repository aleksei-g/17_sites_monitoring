import argparse
import os.path
import sys
import requests
import whois
from urllib.parse import urlparse
from datetime import date, timedelta


MIN_EXPIRATION_DATE = 30


def create_parser():
    parser = argparse.ArgumentParser(description='Скрипт выполняет проверку \
                                     состояния сайтов.')
    parser.add_argument('-f', '--file', metavar='ФАЙЛ',
                        help='Имя файла с URL адресами для проверки.')
    return parser


def check_filepath(filepath):
    if not os.path.exists(filepath):
        print('Файл не существует!')
        return False
    return True


def get_url_list(filepath):
    with open(filepath, 'r') as f:
        return f.read().splitlines()


def get_domain_name_from_url(url):
    return urlparse(url).netloc


def is_server_respond_with_200(url):
    try:
        response = requests.get(url, timeout=(5, 5))
    except requests.exceptions.RequestException:
        return None
    return response.status_code


def get_domain_expiration_date(domain_name):
    expiration_date = whois.whois(domain_name).expiration_date
    return expiration_date[0].date() if expiration_date else None


def output_status_site(url):
    err = False
    status_code = is_server_respond_with_200(url)
    if status_code:
        tests_str = '\tСервер отвечает на запрос статусом %s\n' % status_code
        if status_code != requests.codes.ok:
            err = True
    else:
        tests_str = '\tСайт недоступен!\n'
        err = True
    expiration_date = get_domain_expiration_date(get_domain_name_from_url(url))
    if expiration_date:
        if (expiration_date - date.today()).days > MIN_EXPIRATION_DATE:
            tests_str += \
                '\tДоменное имя проплачено как минимум на 1 месяц вперед\n'
        else:
            tests_str += '\tИстекает срок действия проплаты доменного имени\n'
            err = True
    else:
        tests_str += '\tНе удалось получить expiration date.\n'
        err = True
    if not err:
        test_status = '\nТест: ОК\n'
    else:
        test_status = '\nТест: FAIL\n'
    output_status_str = '%s%s%s' % (url, test_status, tests_str)
    print(output_status_str)


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    if namespace.file:
        filepath = namespace.file
    else:
        filepath = input('Введите текстовый файл с URL адресами '
                         'для проверки:\n')
    if not check_filepath(filepath):
        sys.exit(1)
    url_list = get_url_list(filepath)
    for url in url_list:
        output_status_site(url)
