import os

# TOKEN = os.environ.get('TELEGRAM_TOKEN')
TOKEN = '6508681099:AAHOKB7JNIaAx68wFxRpbPbTLshYNYu37q0'
UPLOADS_FOLDER = 'C:/Users/Admin/PycharmProjects/TestTask_AyanTex/bot/uploads/'
IMAGE_PATH = 'C:/Users/Admin/PycharmProjects/TestTask_AyanTex/bot/uploads/uploaded_image.jpg'
TEMPLATE_PATH = 'C:/Users/Admin/PycharmProjects/TestTask_AyanTex/bot/uploads/template.jpg'
SERVER_URL = 'http://127.0.0.1:5000/upload_template'
MODEL_URL = 'https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2'
SELECT_ACTION, UPLOAD_TEMPLATE, UPLOAD_IMAGE = range(3)
LOG_FILE = 'bot.log'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
