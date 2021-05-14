import logging
import sys
try:
    from logformat import LogFormat
except ImportError:
    from .logformat import LogFormat



class RootLogger:
    def __init__(self, logger=None, separator=":"):
        self.logger = logger or logging.getLogger()
        self.format = LogFormat(formatstring=self._get_fmt(), separator=separator)

    def _get_fmt(self):
        return self.logger.handlers[0].formatter._fmt

    def _set_fmt(self, _fmt):
        self.logger.handlers[0].setFormatter(logging.Formatter(_fmt))

    def setwidth(self, specifier, width):
        self.format.setwidth(specifier, width)
        self._set_fmt(str(self.format))

    def __getattr__(self, item):
        return getattr(self.logger, item)

    def __setattr__(self, key, value):
        # print(f"setattr {key=}, {value=}")
        super().__setattr__(key, value)
        if key in ['format']:
            self._set_fmt(str(value))


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET)
    logger = logging.getLogger()
    logger.info("root: switching to RootLogger")

    logger = RootLogger()
    logger.info("test Rootlogger")
    logger.error("test Rootlogger")
    logger.error(type(logger))
    logger.debug(logger.level)
    logger.critical(str(logger))

    logger.info(logger.format)
    logger.info(logger._get_fmt())

    logger.setwidth('message', 50)
    print("check!")
    logger.info(logger.format)
    logger.info(logger._get_fmt())

