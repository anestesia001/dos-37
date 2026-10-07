1) Запустить на ВМ как systemd сервис приложение на python
```python
from flask import Flask, jsonify
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Nginx Test App</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Welcome to the test app!</h1>
        <p>This is the main page served by Flask via Nginx</p>
        <img src="/static/nginx-logo.png" alt="Nginx Logo" width="200">
        <p>Examples of endpoints:</p>
        <ul>
            <li><a href="/api/data">/api/data</a> - JSON API</li>
            <li><a href="/slow">/slow</a> - Slow request (3s) </li>
            <li><a href="/static/index.html">/static/index.html</a> - Static file </li>
        </ul>
    </body>
    </html>
    """

@app.route('/api/data')
def api_data():
    return jsonify({
        "status": "success",
        "message": "Data from the Flask application",
        "timestamp": time.time(),
        "items": [1, 2, 3, 4, 5]
    })

@app.route('/slow')
def slow_response():
    time.sleep(3) 
    return "This response took 3 seconds!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
```
2) Создать директорию `/var/www/static`, в ней создать файлы
- index.html
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Динамические стили из JavaScript</title>
    <script src="/static/style.js" defer></script>
</head>
<body>
    <header id="main-header">
        <h1>Добро пожаловать!</h1>
    </header>

    <section class="content">
        <div class="card">
            <h2>Карточка 1</h2>
            <p>Это пример карточки с динамическими стилями</p>
            <button class="btn">Нажми меня</button>
        </div>

        <div class="card">
            <h2>Карточка 2</h2>
            <p>Еще один контейнер со стилями из JS</p>
            <button class="btn">Кнопка</button>
        </div>
    </section>

    <button onclick="toggleDarkMode()">Переключить тему</button>

    <footer id="main-footer">
        <p>Динамические стили из JavaScript &copy; 2023</p>
    </footer>
</body>
</html>
```
- style.js
```js
function applyStyles() {
    const css = `
        /* Основные стили */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f2f5;
            color: #333;
            line-height: 1.6;
        }

        #main-header {
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .content {
            display: flex;
            justify-content: center;
            gap: 2rem;
            padding: 2rem;
            flex-wrap: wrap;
        }

        .card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.08);
            padding: 1.5rem;
            width: 300px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 20px rgba(0,0,0,0.12);
        }

        .btn {
            background-color: #4a6ee0;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 50px;
            cursor: pointer;
            font-weight: 600;
            transition: background-color 0.3s;
            margin-top: 1rem;
        }

        .btn:hover {
            background-color: #2e56d0;
        }

        #main-footer {
            text-align: center;
            padding: 1.5rem;
            background-color: #2c3e50;
            color: #ecf0f1;
            margin-top: 2rem;
        }

        /* Адаптивность */
        @media (max-width: 768px) {
            .content {
                flex-direction: column;
                align-items: center;
            }

            .card {
                width: 85%;
            }
        }
    `;


    const styleElement = document.createElement('style');
    styleElement.id = 'dynamic-styles';
    styleElement.textContent = css;


    document.head.appendChild(styleElement);
}


document.addEventListener('DOMContentLoaded', applyStyles);


function toggleDarkMode() {
    const dynamicStyles = document.getElementById('dynamic-styles');
    const isDark = dynamicStyles.textContent.includes('dark-mode');

    if (isDark) {
        dynamicStyles.textContent = dynamicStyles.textContent.replace(
            /\/\* DARK MODE START \*\/[\s\S]*?\/\* DARK MODE END \*\//g,
            ''
        );
    } else {
        dynamicStyles.textContent += `
            /* DARK MODE START */
            body {
                background-color: #121212;
                color: #e0e0e0;
            }

            .card {
                background-color: #1e1e1e;
                box-shadow: 0 6px 15px rgba(0,0,0,0.3);
            }

            #main-footer {
                background-color: #0d0d0d;
            }
            /* DARK MODE END */
        `;
    }
}
```
Скачать лого nginx:
```bash
wget -O /var/www/static/nginx-logo.png https://nginx.org/nginx.png
```
3) Настроить Nginx в качестве прокси для созданного в пп1,2 приложения
- nginx проксирует запросы на flask-бэкенд
- nginx раздает статические файлы из директории `/var/www/static`

Итог работы выглядит так: [видео](https://youtu.be/AHcrRwR9O6o)
