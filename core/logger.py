import logging

from core.config import Config


class Logger:
    """
    Central application logger.

    LOG_MODE from Config controls the output:

        "print"   -> ordinary print()
        "logging" -> Python logging to file
        "stop"    -> no output
    """

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

    def __init__(self, name: str = "SA_03"):
        self.name = name

        self._logger = logging.getLogger(name)

        # Prevent propagation to the root logger.
        self._logger.propagate = False

        # Configure logging only once.
        if not self._logger.handlers:
            self._configure()

    # --------------------------------------------------
    # Configuration
    # --------------------------------------------------

    def _configure(self):
        """
        Configure Python logging output.

        The log directory is created automatically.
        """

        log_file = Config.LOG_FILE

        log_file.parent.mkdir(parents=True, exist_ok=True)

        handler = logging.FileHandler(
            log_file,
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        handler.setFormatter(formatter)

        self._logger.addHandler(handler)

        # We want all four levels to reach the logger.
        self._logger.setLevel(logging.DEBUG)


    # --------------------------------------------------
    # Internal output
    # --------------------------------------------------

    def _write(self, level: str, *args):
        """
        Write a message according to Config.LOG_MODE.
        """

        message = " ".join(str(arg) for arg in args)

        mode = Config.LOG_MODE

        # ----------------------------------------------
        # STOP
        # ----------------------------------------------

        if mode == "stop":
            return

        # ----------------------------------------------
        # PRINT
        # ----------------------------------------------

        if mode == "print":
            print(*args)
            return

        # ----------------------------------------------
        # LOGGING
        # ----------------------------------------------

        if mode == "logging":

            if level == self.DEBUG:
                self._logger.debug(message)

            elif level == self.INFO:
                self._logger.info(message)

            elif level == self.WARNING:
                self._logger.warning(message)

            elif level == self.ERROR:
                self._logger.error(message)

            return

        # ----------------------------------------------
        # Unknown mode
        # ----------------------------------------------

        print(f"[Logger] Unknown LOG_MODE: {mode!r}")

    # --------------------------------------------------
    # Public interface
    # --------------------------------------------------

    def debug(self, *args):
        self._write(self.DEBUG, *args)

    def info(self, *args):
        self._write(self.INFO, *args)

    def warning(self, *args):
        self._write(self.WARNING, *args)

    def error(self, *args):
        self._write(self.ERROR, *args)



    # --------------------------------------------------
    # Public interface
    # --------------------------------------------------

    def debug(self, *args):
        self._write(self.DEBUG, *args)

    def info(self, *args):
        self._write(self.INFO, *args)

    def warning(self, *args):
        self._write(self.WARNING, *args)

    def error(self, *args):
        self._write(self.ERROR, *args)


# ------------------------------------------------------
# Global application logger
# ------------------------------------------------------

logger = Logger()

