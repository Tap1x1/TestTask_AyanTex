import logging
import os
import requests
import tensorflow_hub as hub
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from config import TOKEN, SERVER_URL, UPLOADS_FOLDER, MODEL_URL, SELECT_ACTION, UPLOAD_TEMPLATE, UPLOAD_IMAGE, \
    LOG_FILE, IMAGE_PATH, TEMPLATE_PATH
from image_processing.image_processing_functions import compare_text_similarity
from image_processing.template_matching import detect_objects_and_extract_text
from utils.error_handling import error_handler, setup_logger

setup_logger(LOG_FILE)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(
        f"Привет, {user.first_name}! Я бот для обработки фотографий стеллажей с товарами. "
        "Чтобы начать, отправьте мне шаблон стеллажа командой /template."
    )
    return SELECT_ACTION


def upload_template(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Отправьте мне фотографию шаблона стеллажа. "
        "Этот шаблон будет использоваться для сравнения с другими стеллажами."
    )
    return UPLOAD_TEMPLATE


@error_handler
def template_handling(update: Update, context: CallbackContext) -> None:
    """Функция обрабатывает, скачивает и загружает на сервер шаблон, отправленный пользователем через Telegram бота."""
    try:
        template_file = update.message.photo[-1].get_file()
        template_file.download(TEMPLATE_PATH)
        with open(TEMPLATE_PATH, 'rb') as template_file:
            response = requests.post(SERVER_URL, files={'file': template_file})
            if response.status_code == 200:
                update.message.reply_text("Шаблон стеллажа успешно отправлен на сервер.")
            else:
                update.message.reply_text("Не удалось отправить шаблон стеллажа на сервер.")
    except Exception as e:
        logger.error(f"Произошла ошибка шаблона: {str(e)}")
    return SELECT_ACTION


def upload_image(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Отправьте мне фотографию стеллажа для сравнения с шаблоном.")
    return UPLOAD_IMAGE


@error_handler
def image_handling(update: Update, context: CallbackContext) -> None:
    """Функция скачивает отправленное пользователем изображение через Telegram бота. Вызевает функцию каторая извлекает
    текст из изображения и шаблона. После вызывается функция для сравнения извлеченных данных. И отправляет пользователю
    результат с оценкой сходства изображений"""
    try:
        image_file = update.message.photo[-1].get_file()
        image_file.download(IMAGE_PATH)
        detection_model = hub.load(MODEL_URL)
        update.message.reply_text('Процесс сравнения...')
        extracted_image_text = detect_objects_and_extract_text(IMAGE_PATH, detection_model)
        extracted_template_text = detect_objects_and_extract_text(TEMPLATE_PATH, detection_model)
        similarity_threshold = 0.5  # Порог сходства

        # Вызываем функцию сравнения текста
        is_similar, similarity_score = compare_text_similarity(extracted_template_text, extracted_image_text,
                                                               similarity_threshold)

        if is_similar:
            response_text = f"Стеллажи совпадают (Сходство: {similarity_score}, где 1 это 100% сходство)"
        else:
            response_text = f"Стеллажи не совпадают (Сходство: {similarity_score}, где 1 это 100% сходство)"
        update.message.reply_text(response_text)
    except Exception as e:
        logger.error(f"Произошла ошибка изображения: {str(e)}")
    return SELECT_ACTION


def main():
    """Функция создает и настраивает основные компоненты для работы Telegram бота. Эта функция настраивает обработку
     команд и состояний бота, а также запускает бота в режиме опроса для взаимодействия с пользователями через Telegram."""
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECT_ACTION: [
                CommandHandler('template', upload_template),
                CommandHandler('image', upload_image),
                CommandHandler('start', start),
            ],
            UPLOAD_TEMPLATE: [
                MessageHandler(Filters.photo, template_handling),
            ],
            UPLOAD_IMAGE: [
                MessageHandler(Filters.photo, image_handling),
            ],
        },
        fallbacks=[],
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    if not os.path.exists(UPLOADS_FOLDER):
        os.makedirs(UPLOADS_FOLDER)
    main()