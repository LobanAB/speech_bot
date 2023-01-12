# Распознование речи

Программа бот распознает реч и отвечает на заранее определенные вопросы.

## Как установить

- Скачайте код.
```
git clone https://github.com/LobanAB/speech_bot.git
```
- Для работы скачайте Python - https://www.python.org/.
- Установите зависимости 
```
pip install -r requirements.txt
```
- Создайте файл .env со следующим содержимым.

Для работы нужен ключ api Вконтакте .
```
TG_API_TOKEN={API токен вашего Телеграм бота. Бота создает [Отец Ботов](https://telegram.me/BotFather)}
TG_CHAT_ID={Чтобы получить свой chat_id, напишите в Telegram специальному боту: @userinfobot}
GOOGLE_PROJECT_ID={id, который вы получили, когда создавали проект}
GOOGLE_SESSION_ID={это строка, уникальная для каждого пользователя бота, чтобы он мог отличать одного пользователя от другого. Подойдёт id пользователя из Telegram.}
GOOGLE_APPLICATION_CREDENTIALS={***.json ключ доступа}
VK_API_KEY={API ключ Вконтакте} 
```
-[Как создать проект в DialogFlow](https://cloud.google.com/dialogflow/es/docs/quick/setup  "google.com")

-[Как получить json ключ доступа](https://cloud.google.com/docs/authentication/client-libraries  "google.com")

-[Как получить API ключ Вконтакте](https://vk.com/dev/first_guide  "vk.com")


## Как запустить программу

Для бота в Telegram
```
python bot-tg.py
```
Для бота в VK
```
python bot-vk.py
```

Бот запуститься и будет отвечать на вопросы пользователя.

## Как добавить фразы

- Подготовьте файл `questions.json`.

Со следующим содержимым:
```
{
    "{Название группы вопросов}": {
        "questions": [
            "{вопрос 1}",
            "{вопрос 2}",
            "{вопрос 3}",
            "{вопрос 4}",
            "{вопрос 5}",
            "{вопрос 6}",
            "{вопрос 7}"
        ],
        "answer": "{ответ 1}"
    },
        "{Название еще одной группы вопросов}": {
        "questions": [
            "{вопрос 8}",
            "{вопрос 9}",
            "{вопрос 10}",
            "{вопрос 11}",
            "{вопрос 12}",
            "{вопрос 13}",
            "{вопрос 14}"
        ],
        "answer": "{ответ 2}"
    }
}
```
- Запустите программу:
```
python intent.py
```

## Пример работы

![Бот Telegram](/img/bot-tg.jpg)
![Бот VK](/img/bot-vk.jpg)

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).