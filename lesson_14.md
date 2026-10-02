1) Написать скрипт для поиска свободного порта из диапазона M-N, где M и N - передаются скрипту как аргументы
2) Написать скрипт, для деплоя лендинга https://gitlab.com/dos-26/cmdb/frontend и скрипт для его проверки
3) Развернуть Python-веб-сервер как systemd демон

Код сервера
```python
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

os.chdir("/srv/webapp/content")
server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
```

#### Требования
1) Сервер запущен как systemd демон с правами пользователя `webadmin`
2) Пользователь `webadmin` не имеет shell-доступпа и является членом группы `webgroup`
3) Код сервера расположен в директории `/opt/srv/webapp`; в той же диреткории лежит `content/index.html` с содержимым
```html
<!DOCTYPE html>
<html>
<head>
    <title>Приветствие</title>
    <style>
        .greeting {
            border: 5px solid orange; 
            padding: 20px; 
            font-size: 48px;
            text-align: center; 
            margin: 50px auto; 
            width: fit-content;
            border-radius: 15px;
            background-color: #fff8f0; 
            font-family: Arial, sans-serif;
            box-shadow: 0 0 15px rgba(255, 165, 0, 0.3); 
        }
    </style>
</head>
<body>
    <div class="greeting">Hello, DOS-29-ONL! You are amazing!</div>
</body>
</html>
```
