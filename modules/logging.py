import logging
import datetime
import coloredlogs


CUR_TIME = datetime.datetime.now().strftime("%m %d %Y-%H:%M:%S")
logger = logging.getLogger()

formatter = logging.Formatter("[%(asctime)s] %(levelname)s (%(name)s): %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

file_handler = logging.FileHandler(f"./data/logs/{CUR_TIME}.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

coloredlogs.install(level=logging.INFO,logger=logger)
