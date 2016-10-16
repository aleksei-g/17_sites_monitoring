# 17_sites_monitoring

# Мониторинг сайтов

Утилита для проверки состояния сайтов. На вход скрипт принимает файл с URL адресами для проверки (каждый URL с новой строки). На выходе - статус каждого сайта по результатам следующих проверок:
* сервер отвечает на запрос статусом HTTP 200;
* доменное имя сайта проплачено как минимум на 1 месяц вперед.

**Параметры скрипта:**
* **-f ФАЙЛ (--file ФАЙЛ):** необязательный параметр, путь до файла с URL адресами для проверки.

Так же есть возможность передать файл с URL адресами в **stdin** параметре.

**Пример использования:**
* Передача пути до файла в параметрах запуска скрипта:
```
python check_sites_health.py -f sites.txt
```

* Передача пути до файла в stdin, вывод stdout и stderr в соответсвующие файлы логов:
```
cat sites.txt | python check_sites_health.py 1>result.log 2>errors.log
```

* Если файл с URL адресами не был передан, скрипт после запуска будет ожидать ввода URL адресов от пользователя, для завершения ввода используется сочетание клавиш **"Ctrl+D"**.

**Установка дополнительных пакетов:**

Для корректоной работы скрипта необходимо установить следующие модули:
* **requests** - для работы с HTTP,
* **python-whois** - для получения данных о домене.

Пакеты устанавливаются по команде `pip install -r requirements.txt`.
