import logging
import cv2
import tensorflow as tf
import pytesseract
from Levenshtein import distance

logger = logging.getLogger(__name__)


def preprocess_image(image_path, target_size=(600, 600)):
    """Эта функция предназначена для предварительной обработки изображения, которое загружается из указанного пути."""
    try:
        # Загрузите изображение и измените его размер
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return cv2.resize(image_rgb, target_size)
    except Exception as e:
        logger.error(f"Ошибка в preprocess_image: {str(e)}")
        return None


def similarity_score(text1, text2):
    """Эта функция вычисляет меру сходства между двумя текстовыми строками, используя коэффициент Жаккара.
    Если одна из строк пуста или происходит ошибка при вычислении, она вернет 0.0, иначе вернет числовое значение,
    отражающее степень схожести между текстами."""
    try:
        if len(text1) == 0 or len(text2) == 0:
            return 0.0  # Возвращаем 0 при нулевой длине текста
        else:
            return 1 - (distance(text1, text2) / max(len(text1), len(text2)))
    except Exception as e:
        logger.error(f"Ошибка в similarity_score: {str(e)}")
        return 0.0


def detect_objects_and_extract_text(image_path, detection_model):
    """Эта функция принимает путь к изображению и модель обнаружения объектов, а затем выполняет следующие шаги:
    сначала она использует модель обнаружения объектов для нахождения объектов на изображении, затем извлекает текст
    с областей, где объекты были найдены, и возвращает уникальные текстовые строки, избегая дублирования текста.
    Если происходит какая-либо ошибка, она регистрируется с помощью логгера"""
    try:
        image = preprocess_image(image_path)
        image_tensor = tf.convert_to_tensor(image[tf.newaxis, ...])
        detections = detection_model(image_tensor)
        boxes = detections['detection_boxes'][0].numpy()
        scores = detections['detection_scores'][0].numpy()
        threshold = 0.1
        selected_indices = tf.image.non_max_suppression(boxes, scores, max_output_size=boxes.shape[0], iou_threshold=threshold)
        selected_boxes = tf.gather(boxes, selected_indices)

        # Извлечение текста с областей, где обнаружены объекты
        extracted_texts = []
        for selected_box in selected_boxes:
            ymin, xmin, ymax, xmax = map(int, selected_box * [image.shape[0], image.shape[1], image.shape[0], image.shape[1]])
            cropped_image = image[ymin:ymax, xmin:xmax]
            extracted_text = pytesseract.image_to_string(cropped_image, lang='eng')
            extracted_texts.append(extracted_text.strip())

        # Удаление дублирующихся текстов
        unique_texts = []
        for text in extracted_texts:
            is_unique = True
            for unique_text in unique_texts:
                similarity = similarity_score(text, unique_text)
                if similarity > 0.1:  # Настройте порог сходства по вашему усмотрению
                    is_unique = False
                    break
            if is_unique:
                unique_texts.append(text)

        return unique_texts
    except Exception as e:
        logger.error(f"Ошибка в detect_objects_and_extract_text: {str(e)}")
