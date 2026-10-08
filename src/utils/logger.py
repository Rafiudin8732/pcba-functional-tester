import logging
import os
from datetime import datetime


def setup_logger(name: str = "pcba_tester", log_dir: str = "logs") -> logging.Logger:
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        file_handler = logging.FileHandler(os.path.join(log_dir, f"pcba_tester_{timestamp}.log"), encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
