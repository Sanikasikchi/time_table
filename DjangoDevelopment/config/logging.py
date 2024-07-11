LOGGING = {
    'version': 1,                       # the dictConfig format version
    'disable_existing_loggers': False,  # retain the default loggers
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'verbose2',
            'level': 'ERROR',
        },
    },
    'loggers': {
        '': {
            'level': 'ERROR',
            # 'level': 'DEBUG',
            'handlers': ['file'],
        },
    },
    'formatters': {
        'verbose2': {
            'format': '[{asctime}] [{levelname}] {name}:{lineno} - {funcName}() >> {message}',
            'style': '{',
        },
    },

}