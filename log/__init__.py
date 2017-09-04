import logging.handlers  # logger 인스턴스를 생성 및 로그 레벨 설정

logger = logging.getLogger("crumbs")
logger.setLevel(logging.DEBUG)

#  formmater 생성
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

# fileHandler와 StreamHandler를 생성
fileHandler = logging.FileHandler('./log/my.log')
streamHandler = logging.StreamHandler()

#  handler에 fommater 세팅
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

#  Handler를 logging에 추가
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)


def write(msg, type=None):
	if type == logging.INFO:
		logger.info(msg)
	elif type == logging.DEBUG:
		logger.debug(msg)
	elif type == logging.ERROR:
		logger.error(msg)
	elif type == logging.CRITICAL:
		logger.critical(msg)
	else:
		logger.info(msg)