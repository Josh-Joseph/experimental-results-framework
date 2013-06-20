"""
This modelule is a replacement for logging that includes two additional logging levels: TIMING and PROGRESS

TIMING is set to a logging level of INFO
PROGRESS is set to a logging level of INFO

It is meant to be used in the same way as the standard logging module.
"""

from logging import root
from logging import *


##### add a timing call to logging ####
# set the level of logging.timing
TIMING = INFO
addLevelName(TIMING, 'TIMING')

# define the timing function to be used in the Logger class
def _logger_timing(self, message, *args, **kws):
    self.log(TIMING, message, *args, **kws)

# add it to the Logger class
Logger.timing = _logger_timing

# define a timing function be used easily with basicConfig()
def timing(msg, *args, **kwargs):
    """
    Log a message with severity 'TIMING' on the root logger.
    """
    if len(root.handlers) == 0:
        basicConfig()
    root.timing(msg, *args, **kwargs)


##### add a progress call to logging ####
# set the level of logging.progress
PROGRESS = INFO
addLevelName(PROGRESS, 'PROGRESS')

# define the progress function to be used in the Logger class
def _logger_progress(self, message, *args, **kws):
    self.log(PROGRESS, message, *args, **kws)

# add it to the Logger class
Logger.progress = _logger_progress

# define a progress function be used easily with basicConfig()
def progress(msg, *args, **kwargs):
    """
    Log a message with severity 'PROGRESS' on the root logger.
    """
    if len(root.handlers) == 0:
        basicConfig()
    root.progress(msg, *args, **kwargs)
















if 0:

    ##### add a progress call to logging ####
    # set the level of logging.progress
    PROGRESS = logging.CRITICAL
    logging.addLevelName(PROGRESS, 'PROGRESS')

    # define the progress function
    def progress(self, message, *args, **kws):
        self.log(PROGRESS, message, *args, **kws)
    logging.Logger.progress = progress

    logging.basicConfig()
    l = logging.getLogger()
    l.setLevel(TIMING)
    l.timing('test1')
    l.progress('test2')