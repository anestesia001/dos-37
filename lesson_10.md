1) В домашней директории создать `home_works` создать директорию `lesson_10`
2) В директории `lesson_10` создать директорию `available`, в ней файлы `app.conf, readme.md, app.log` с произвольным содержимым
3) В директории `lesson_10` создать директорию `enabled`, в ней создать symlink на `available/app.conf`
4) В директории `lesson_10` создать директории `logs` и `debug`; переместить файл `available/app.log` в директорию `logs`, а в `debug` сделать hardlink на `logs/app.log`
5) Добавить к вашей ВМ дополнительный диск.\
Для VirtualBox инструкция https://gist.github.com/AnastasiyaGapochkina01/a333559e4910bd85153714de4540ced8
6) Посмотреть список блочных устройств (`lsblk`) и список смонтированных ФС (`df -Th`)
7) Создать на новом диске ФС типа ext4
8) Создать директорию `/opt/application` и смонтировать в нее новый диск (монтирование должно быть постоянным, через `/etc/fstab`)
8) Скопировать `/opt/application` все **содержимое** `lesson_10`. Должно получиться примерно такое
```bash
/opt/application/
├── available
│   └── app.conf
├── debug
│   └── app.log
├── enabled
│   └── app.conf -> available/app.conf
└── logs
    └── app.log
```
9) Попробовать сделать hardlink на файл `$HOME/home_works/lesson_10/available/readme.md` в директории `/opt/application` (не получится); затем сделать symlink на этот же файл
