# logger_config.py
import logging

def setup_logger():
    # Настройка основного логгера для проекта
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("SigmaBot.log"),
            logging.StreamHandler()
        ]
    )

    # Получение логгера для проекта
    logger = logging.getLogger("SigmaBot")

    # Настройка логгера для httpx на уровень DEBUG
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.ERROR)

    return logger