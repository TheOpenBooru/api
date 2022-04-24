import logging


logging.basicConfig(
    filename='./data/log.txt',
    filemode='a',
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s - %(message)s',
)
