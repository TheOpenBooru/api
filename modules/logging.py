import logging

file_handler = logging.FileHandler('file.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s'))

logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler]
)
