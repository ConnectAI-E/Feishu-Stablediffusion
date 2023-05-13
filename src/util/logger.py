import logging
import os

# create logs folder if not exist
if not os.path.exists("logs"):
    os.makedirs("logs")

CONSOLE_LOGGING_FORMAT = '%(asctime)s %(levelname)s %(message)s'
FILE_LOGGING_FORMAT = '%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(message)s'


def get_logger(name):
    logger = logging.getLogger(name)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(CONSOLE_LOGGING_FORMAT))
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(f'logs/{name}.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(FILE_LOGGING_FORMAT))
    logger.addHandler(file_handler)

    logger.setLevel(logging.DEBUG)
    return logger


feishu_logger = get_logger("feishu")
sd_logger = get_logger("sd")
app_logger = get_logger("app")

if __name__ == "__main__":
    feishu_logger.info("test")
    sd_logger.info("test")
    app_logger.debug("ddd")