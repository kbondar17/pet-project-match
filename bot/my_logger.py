import logging

def get_logger(name):
    logger = logging.getLogger(name)
    format = '%(filename)+13s %(name)s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(format))
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    return logger
    # logger.debug(f'logger {name} initialized!')


# get_logger('bot_log')
# logger = logging.getLogger('bot_log.main')
# logger.debug('logger works!')
logger = get_logger('ТЕЛЕГРАМ ЛОГЕР:')
# dp.middleware.setup(LoggingMiddleware(logger))
print(logger.level)
print(logger.debug('сделали логер'))


# вот так инициализировать в других файлах

#logger = get_logger(f'my_log-{__name__}')
