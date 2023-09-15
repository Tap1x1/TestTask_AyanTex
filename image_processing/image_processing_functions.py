import logging

from Levenshtein import distance


logger = logging.getLogger(__name__)


def compare_text_similarity(template_text, extracted_text, similarity_threshold):
    """Эта функция сравнивает сходство между двумя текстовыми строками,
    используя расстояние Левенштейна, которое измеряет количество операций (вставок, удалений, замен)
    для преобразования одной строки в другую. Если сходство текстов выше заданного порогового значения,
    функция возвращает True и коэффициент сходства. В противном случае, она возвращает False и коэффициент сходства."""
    try:
        # Вычислите расстояние Левенштейна между текстами
        levenshtein_distance = distance(template_text, extracted_text)

        # Вычислите сходство в пределах [0, 1], где 1 - это точное совпадение
        max_length = max(len(template_text), len(extracted_text))
        similarity = 1 - (levenshtein_distance / max_length)

        # Сравните сходство с пороговым значением
        if similarity >= similarity_threshold:
            return True, similarity
        else:
            return False, similarity
    except Exception as e:
        logger.error(f"Ошибка в compare_text_similarity: {str(e)}")
        return False, 0.0