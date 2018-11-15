import logging
import os

currdir = os.path.split(os.path.abspath(__file__))[0]

# 通过下面的方式进行简单配置输出方式与日志级别
# logging.basicConfig(filename='%s/../logs/logger.log' % currdir, level=logging.INFO)


# create logger
logger_name = "logger"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.INFO)

# create file handler
log_path = '%s/../logs/logger.log' % currdir
fh = logging.FileHandler(log_path)
fh.setLevel(logging.INFO)

# create formatter
fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)

# add handler and formatter to logger
fh.setFormatter(formatter)
logger.addHandler(fh)

# print log info
# logger.debug('debug message')
# logger.info('info message')
# logger.error('error message')
