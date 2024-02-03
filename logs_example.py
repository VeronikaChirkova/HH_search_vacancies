import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    filename = "mylog.log")


def summary(x,y):
    result = x + y
    logging.debug(result)
    logging.info(result)
    logging.warning(result)
    logging.error(result)
    logging.critical(f"Vsyo propalo! -> {result}")


summary(1,2)