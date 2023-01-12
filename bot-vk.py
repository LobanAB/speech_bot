import logging
import os
import random

from dotenv import load_dotenv
from google.cloud import dialogflow
import telegram
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

load_dotenv()
GOOGLE_PROJECT_ID = os.environ['GOOGLE_PROJECT_ID']
GOOGLE_SESSION_ID = os.environ['GOOGLE_SESSION_ID']
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']


class TelegramLogsHandler(logging.Handler):

    def __init__(self, chat_id, tg_api_token):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = telegram.Bot(token=tg_api_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def send_message(event, google_answer, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=google_answer,
        random_id=random.randint(1, 1000)
    )


def detect_intent_texts(text, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(GOOGLE_PROJECT_ID, GOOGLE_SESSION_ID)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text


def main():
    load_dotenv()
    vk_api_key = os.environ['VK_API_KEY']
    chat_id = os.environ['TG_CHAT_ID']
    tg_api_token = os.environ['TG_API_TOKEN']
    logger.setLevel(logging.WARNING)
    handler = TelegramLogsHandler(chat_id, tg_api_token)
    logger.addHandler(handler)
    bat = handler.tg_bot
    vk_session = vk.VkApi(token=vk_api_key)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    google_answer = detect_intent_texts(event.text, "ru-ru")
                    if google_answer:
                        send_message(event, google_answer, vk_api)
        except:
            logger.exception('Бот упал с ошибкой:')


if __name__ == '__main__':
    main()
