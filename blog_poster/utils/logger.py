import sys

from loguru import logger

# logger
logger.remove(0)
logger.add(sys.stdout, backtrace=True, diagnose=True)
