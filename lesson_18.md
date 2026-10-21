1) Запустить master-slave кластер postgresql (вручную или через repmgr)
2) Запустить приложение https://github.com/anestesia001/notes_api_db_replicated/tree/main

> [!WARNING]  
> приложение создает заметки через primary и читает заметки через replica и не использует общую точку входа (haproxy/etc)

3) Настроить nginx в качестве reverse proxy для приложения
4) Написать скрипт для проверки состояния primary, replica
