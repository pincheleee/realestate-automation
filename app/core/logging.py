import structlog
from typing import Any, Dict
from app.core.config import get_settings

settings = get_settings()

def get_logger(name: str) -> structlog.BoundLogger:
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(settings.LOG_LEVEL),
        cache_logger_on_first_use=True,
    )
    return structlog.get_logger(name)

class LogContext:
    def __init__(self, logger: structlog.BoundLogger):
        self.logger = logger
        self.context: Dict[str, Any] = {}

    def bind(self, **kwargs: Any) -> "LogContext":
        self.context.update(kwargs)
        return self

    def unbind(self, *keys: str) -> "LogContext":
        for key in keys:
            self.context.pop(key, None)
        return self

    def __enter__(self) -> structlog.BoundLogger:
        return self.logger.bind(**self.context)

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.unbind(*self.context.keys()) 