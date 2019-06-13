import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('main')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = TimedRotatingFileHandler('../log/server_log', when='D', interval=1)
fh.suffix = '%Y%m%d'
# fh.namer = 'server-%Y%d%m.log'
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.setLevel(logging.DEBUG)
