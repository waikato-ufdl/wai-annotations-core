import logging
import os
from typing import Optional


def adjust_logging_level(logger_name, default_level, env_var):
    """
    Adjusts the logging level for the specified logger.

    :param logger_name: the name of the logger, eg 'numba'
    :type logger_name: str
    :param default_level: the default logging level to use, if env var not set or value from env var fails to parse
    :type default_level: int
    :param env_var: the name of the environment variable
    :type env_var: str
    """
    try:
        logging.getLogger(logger_name).setLevel(level=os.getenv(env_var, default_level))
    except:
        logging.getLogger(logger_name).setLevel(level=default_level)


# matplotlib outputs a lot of debugging info (fonts, etc)
# to alleviate this, its logging level gets set to WARNING by default
# can be changed via WAIANN_MATPLOTLIB_LOGLEVEL environment variable
adjust_logging_level("matplotlib", logging.WARNING, "WAIANN_MATPLOTLIB_LOGLEVEL")

# numba drowns out the output in the console with its debug messages
# to alleviate this, its logging level gets set to WARNING by default
# can be changed via WAIANN_NUMBA_LOGLEVEL environment variable
adjust_logging_level("numba", logging.WARNING, "WAIANN_NUMBA_LOGLEVEL")


class LoggingEnabled:
    """
    Mixin class which adds logging support to the inheriting class.
    """
    # The cached logger
    _logger: Optional[logging.Logger] = None

    @property
    def logger(self) -> logging.Logger:
        """
        Gets the logger for the class.

        :return:    The logger.
        """
        return self._logger

    @classmethod
    def get_class_logger(cls) -> logging.Logger:
        """
        Gets the logger for the class.

        :return:    The logger.
        """
        return cls._logger

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Cache the logger
        cls._logger = logging.getLogger(cls.__module__ + "." + cls.__name__)
