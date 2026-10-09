1) Запустить приложение https://github.com/anestesia001/dos-36-js как systemd-демон
2) Настроить nginx в роли reverse proxy с TLS для этого приложения
3) Поднять второй экземпляр приложения из п1 на другом порту
4) Настроить на nginx балансировку запросов (round robin)
5) Провести нагрузочное тестирование приложения с помощью locust (скрипт с тестами есть в репозитории https://github.com/anestesia001/dos-36-js/blob/main/locustfile.py ; запуск `locust -f locustfile.py`)
