# Телеграм Бот для Обработки Изображений Стеллажей

Этот проект представляет собой Telegram бота, который позволяет пользователям отправлять фотографии стеллажей с товарами и загружать шаблон стеллажа для сравнения.

## Установка и Запуск

1. Клонируйте репозиторий на ваш компьютер:

   ```bash
   git clone https://github.com/Tap1x1/TestTask_AyanTex
    ```
2. Перейдите в каталог проекта:
    ```bash
    cd your-project
    ```
3. Установите зависимости, используя `pip`:
    ```bash
    pip install -r requirements.txt
    ```
4. Создайте и настройте файл `config.py` для конфигурации бота и сервера.
5. Запустите `main.py` для запуска бота и сервера:
    ```bash
    python main.py
    ```
## Как использовать

1. Начните чат с вашим Telegram ботом.

2. Отправьте фотографию стеллажа с товарами для обработки.

3. Отправьте шаблон стеллажа для сравнения.

4. Бот обработает фотографии и выдаст результат.

## Настройка
Вы можете настроить проект, изменив параметры в файле `config.py`. Этот файл содержит настройки для Telegram бота и сервера.
Скачайте и установите Tesseract OCR. После установки добавьте путь к исполняемому файлу Tesseract в переменную среды PATH.

## Зависимости
+ [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
+ [Flask](https://flask.palletsprojects.com/en/2.3.x/)
+ [opencv-python](https://pypi.org/project/opencv-python/)
+ [numpy](https://numpy.org/)
+ [tensorflow](https://www.tensorflow.org/?hl=ru)
+ [Keras](https://keras.io/)
+ [pytesseract](https://pypi.org/project/pytesseract/)
+ [requests](https://pypi.org/project/requests/)
+ [werkzeug](https://pypi.org/project/Werkzeug/)
+ [Levenshtein](https://pypi.org/project/Levenshtein/)
## Авторы
Уланов Александр

## Вопросы и Обратная Связь
Если у вас есть вопросы, предложения или проблемы, пожалуйста, создайте Issue в этом репозитории или свяжитесь с нами:

[Gmail](a.ulanov2000@gmail.com)

[Issue](https://github.com/Tap1x1/TestTask_AyanTex/issues)


## Лицензия
Этот проект распространяется под лицензией MIT. Подробности смотрите в файле LICENSE.
