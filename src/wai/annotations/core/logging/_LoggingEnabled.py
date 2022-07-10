import logging
import os
from typing import Optional

# numba drowns out the output in the console with its debug messages
# to alleviate this, its logging level gets set to WARNING by default
# can be changed via WAIANN_NUMBA_LOGLEVEL environment variable
try:
    logging.getLogger('numba').setLevel(level=os.getenv("WAIANN_NUMBA_LOGLEVEL", logging.WARNING))
except:
    logging.getLogger('numba').setLevel(level=logging.WARNING)


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
