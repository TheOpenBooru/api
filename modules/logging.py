import logging
import datetime
import coloredlogs


CUR_TIME = datetime.datetime.now().strftime("%m %d %Y-%H:%M:%S")
logger = logging.getLogger()

stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(f"./data/logs/{CUR_TIME}.log")
stream_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s] %(levelname)s (%(name)s): %(message)s")
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
coloredlogs.install(level=logging.INFO,logger=logger)
