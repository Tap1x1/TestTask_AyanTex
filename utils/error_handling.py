import logging


# Настройка логгера
def setup_logger(log_file):
    """Эта функция настраивает систему логирования, определяя формат и путь к файлу журнала, чтобы записывать информацию
     о событиях в приложении."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s]: %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


# Обработка ошибок и логирование
def error_handler(func):
    """Функция используется как декоратор для обработки ошибок в других функциях."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.message(f"Message in {func.__name__}: {str(e)}")
            raise

    return wrapper
