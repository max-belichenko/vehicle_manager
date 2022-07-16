import logging.config

from settings.base import settings


if settings.debug:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO


LOGGER_CONFIGUARTION = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'consoleformat': {
            'class': 'logging.Formatter',
            'style': '{',
            'format': '{asctime} {name} {levelname} {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'consoleformat'
        },
    },
    'root': {
        'level': LOG_LEVEL,
        'handlers': ['console', ]
    },
}
