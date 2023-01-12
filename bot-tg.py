import logging
import os

from dotenv import load_dotenv
from google.cloud import dialogflow
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

load_dotenv()
GOOGLE_PROJECT_ID = os.environ['GOOGLE_PROJECT_ID']
GOOGLE_SESSION_ID = os.environ['GOOGLE_SESSION_ID']
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']


class TelegramLogsHandler(logging.Handler):

    def __init__(self, chat_id, tg_bot):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def send_message(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    message = detect_intent_texts(update.message.text, "ru-ru")
    update.message.reply_text(message)


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
    return response.query_result.fulfillment_text


def err(update: object, context: CallbackContext):
    logger.warning(context.error)


def main() -> None:
    """Start the bot."""
    load_dotenv()
    chat_id = os.environ['TG_CHAT_ID']
    tg_api_token = os.environ['TG_API_TOKEN']
    logger.setLevel(logging.WARNING)
    updater = Updater(tg_api_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_message))
    dispatcher.add_error_handler(err, run_async=True)
    handler = TelegramLogsHandler(chat_id, updater.bot)
    logger.addHandler(handler)
    try:
        updater.start_polling()
    except:
        logger.exception('Бот упал с ошибкой:')
    updater.idle()


if __name__ == '__main__':
    main()
