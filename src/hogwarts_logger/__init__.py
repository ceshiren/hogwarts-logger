from hogwarts_logger.core.logger import Logger

logger = Logger.get_instance()
log, debug, info, warn, error = logger.get_log_actions()[:5]
trace = log
