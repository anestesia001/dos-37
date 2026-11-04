1) В домашней директории создать директорию `docker_files`; в директории `docker_files` создать файл `index.php` с содержимым
```php
<?php
phpinfo();
?>
```
Запустить контейнер из image `php:8.2-apache` с
- именем `php-web-1`
- маппингом портов `8000:80`
- сопоставлением (bind mount) файла `index.php` на хосте с файлом `/var/www/index.php` в контейнере

Проверить, что контейнер запустился и проверить его работу с помощью
```
curl -I 127.0.0.1:8000
```
если ответ похож на такое, то все ок
```
HTTP/1.1 200 OK
Date: Thu, 10 Jul 2025 03:28:13 GMT
Server: Apache/2.4.62 (Debian)
X-Powered-By: PHP/8.2.29
Content-Type: text/html; charset=UTF-8
```

2) В директории `docker_files` создать файл `hello.py` с содержимым
```python
#!/usr/bin/python
import socket
import os
import pwd
user_name = pwd.getpwuid(os.getuid())[0]
host_name = socket.gethostname()
print(f"Hello, {user_name} you inside in {host_name}")
```
Запустить контейнер из image `python:3.11` с именем sayhello-1 и сопоставлением (bind mount) файла `hello.py` на хосте с файлом `/app/hello.py` в контейнере.\
Зайти в запущенный контейнер и выполнить в нем `python /app/hello.py` Если вывод похож на `Hello, root you inside in 1adc7f445dc9`, то все ок

3) В директории `docker_files` создать файл `info.php` с содержимым ```php
Версия ОС сервера: Linux 6b53817c4c3f 5.10.0-34-amd64 #1 SMP Debian 5.10.234-1 (2025-02-24) x86_64
Тип ОС сервера: Linux
IP-адрес сервера: 172.17.0.2
```
Запустить контейнер из image `php:latest` с именем phpinfo-1 и сопоставлением (bind mount) файла `info.php` на хосте с файлом `/app/info.php` в контейнере.\
Зайти в запущенный контейнер и выполнить в нем `php /app/info.php`. Вывод должен быть похож на
```
Версия ОС сервера: Linux 6b53817c4c3f 5.10.0-34-amd64 #1 SMP Debian 5.10.234-1 (2025-02-24) x86_64
Тип ОС сервера: Linux
IP-адрес сервера: 172.17.0.2
```
4) В директории `docker_files` создать директорию `flask-info`, в ней файл `app.py` с содержимым
```pytnon
from flask import Flask
import sys
import os

app = Flask(__name__)

@app.route('/')
def index():
    python_version = sys.version
    current_directory = os.getcwd()
    return f"Версия Python: {python_version}\nТекущая директория: {current_directory}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```
Собрать для `app.py` docker image; запустить из созданного image контейнер с именем `info-py-1` и маппингом портов `5000:5000`.\
Проверить работоспособность комнандой 
```bash
curl 127.0.0.1:5000
```
Все ок, если отдается что-то похожее на
```bash
Версия Python: 3.9.2 (default, Mar 20 2025, 02:07:39)
[GCC 10.2.1 20210110]
Текущая директория: /home/anestesia/python
```
5) В директории `docker_files` создать директорию `node-info`, в ней файл `server.js` с содержимым
```js
const http = require('http');
const os = require('os');
const childProcess = require('child_process');

const getNodeVersion = () => {
    return childProcess.execSync('node -v').toString().trim();
};

const getOSVersion = () => {
    return os.type() + ' ' + os.release();
};

const server = http.createServer((req, res) => {
    const nodeVersion = getNodeVersion();
    const osVersion = getOSVersion();

    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.end(`Версия Node.js: ${nodeVersion}\nВерсия ОС: ${osVersion}`);
});

server.listen(3000, () => {
    console.log('Сервер запущен на порту 3000');
});
```
и файл `package.json` с содержимым
```json
{
  "name": "node-info-app",
  "version": "1.0.0",
  "description": "",
  "main": "server.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "anestesia",
  "license": "ISC",
  "dependencies": {
    "express": "^4.21.1"
  },
  "scripts": {
	  "start": "node server.js"
  }
}
```
Собрать docker image для этого проекта; из собранного image запустить контейнер с именем `info-node-1` с маппингом портов `3000:3000`.\
Проверить работоспособность комнандой 
```bash
curl 127.0.0.1:3000
```
Все ок, сли отдается что-то похожее на
```
Версия Node.js: v23.11.0
Версия ОС: Linux 5.10.0-19-amd64
```
