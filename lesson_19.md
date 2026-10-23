1) Написать плейбук, который:
    - устанавливает пакеты `tree` и `jq`
    - создаёт директорию `/opt/app/config`.
    - копирует `files/app.conf` в `/opt/app/config/app.conf` (содержимое `app.conf` https://github.com/anestesia001/static-demo-app/blob/main/app.conf)
    - устанавливает права `0644`
2) Написать плейбук, который:
    - создаёт группу `devops`.
    - создаёт пользователя `ecom`: shell — `/bin/bash`; домашняя директория — `/home/ecom`; пользователь входит в группу `devops`.
    - cоздаёт директорию `/home/ecom/.ssh` с правами `0700`.
    - создаёт файл `/home/ecom/.ssh/authorized_keys`.
    - вставляет в `authorized_keys` публичный SSH-ключ, который лежит в файле `files/ecom_key.pub`.
    - устанавливает владельца `ecom` и права `0600` на `authorized_keys`.
3) Написать плейбук, который:
    - создаёт пользователя `demoapp` без возможности входа по паролю.
    - создаёт директорию `/opt/demo_app` с владельцем `demoapp`.
    - копирует `index.html` (https://github.com/anestesia001/static-demo-app/blob/main/index.html) в `/opt/demo_app/index.html`.
    - копирует unit-файл (https://github.com/anestesia001/static-demo-app/blob/main/demo-app.service) в `/etc/systemd/system/demo-app.service.`
    - выполняет `systemctl daemon-reload`.
    - включает и запускает сервис `demo-app`.
    - выполняет проверку через `curl`
