import logging
from logging.handlers import SysLogHandler

def setup_papertrail_logging(logger_name='papertrail'):
    # Create a specific logger for Papertrail
    papertrail_logger = logging.getLogger(logger_name)

    if not papertrail_logger.handlers:

        papertrail_logger.setLevel(logging.DEBUG)  # Or any appropriate level
        papertrail_logger.propagate = False

        # Configure SysLogHandler for Papertrail
        syslog_handler = SysLogHandler(address=('logs3.papertrailapp.com', 23803))
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%b %d %H:%M:%S')
        syslog_handler.setFormatter(formatter)
        papertrail_logger.addHandler(syslog_handler)

    return papertrail_logger

def setup_local_logging():
    # Configure the root logger for local outputs
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Configure StreamHandler for console output
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%b %d %H:%M:%S')
    console.setFormatter(formatter)
    logger.addHandler(console)

def main():
    setup_local_logging()
    papertrail_logger = setup_papertrail_logging()
    papertrail_logger.info("Hello, World to Papertrail!")
    logging.info("Hello, World locally!")

if __name__ == '__main__':
    main()
