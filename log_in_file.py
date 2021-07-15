import os
import datetime


def log_in_file(text):
    """
    :param text: text to write
    :return: -
    """
    if not os.path.exists('log.txt'):
        with open('log.txt', 'w') as logger:
            logger.write('Create log file' + '\n')
    with open('log.txt', 'a') as logger:
        logger.write(str(datetime.datetime.now()) + ' ' + str(text) + '\n')
    return True
