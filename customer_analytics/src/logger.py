import logging
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """Кастомний форматувач для виведення логів у форматі JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        # Якщо при виклику логера передано словник extra={"extra_info": {...}},
        # ми розпакуємо його прямо в JSON
        if hasattr(record, "extra_info"):
            log_record.update(record.extra_info)

        return json.dumps(log_record, ensure_ascii=False)


def setup_logger() -> logging.Logger:
    """Ініціалізація логера для сервісу."""
    logger = logging.getLogger("ml_service")
    logger.setLevel(logging.INFO)

    # Щоб логи не дублювалися під час перезапусків
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)

    return logger