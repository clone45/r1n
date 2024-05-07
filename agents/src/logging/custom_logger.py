import logging

class CustomLogger(logging.Logger):
    def _log(self, level, msg, args, **kwargs):
        if level >= self.level:
            msg = f"__{msg}"  # Automatically prepend '__' to all messages
        super()._log(level, msg, args, **kwargs)

class CustomAppFilter(logging.Filter):
    def filter(self, record):
        if record.msg.startswith('__'):
            record.msg = record.msg[2:]  # Strip the '__' prefix before logging
            return True
        return False  # Discard messages not starting with '__'
