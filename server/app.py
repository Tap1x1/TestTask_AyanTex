import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS, UPLOADS_FOLDER

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER


def allowed_file(filename):
    """Эта функция проверяет, является ли расширение имени файла допустимым,
     сравнивая его с набором разрешенных расширений ALLOWED_EXTENSIONS."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_template', methods=['POST'])
def upload_template():
    """А функция upload_template() обрабатывает POST-запрос для загрузки файла (шаблона стеллажа) на сервер.
    Она проверяет, что файл был отправлен с запросом, имеет допустимое расширение, сохраняет его на сервере с
    безопасным именем и возвращает соответствующий HTTP-статус и сообщение в зависимости от результата операции."""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'template.jpg'))
            return jsonify({"message": "Template successfully uploaded"}), 200
        else:
            return jsonify({"error": "Invalid file format"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
