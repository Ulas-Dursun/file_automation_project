"""Logging service with singleton pattern."""

import logging
from pathlib import Path
from typing import Optional


class LoggerService:
    """
    Singleton logging service for application-wide logging.

    Ensures a single logger instance is used throughout the application.
    """

    _instance: Optional['LoggerService'] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls) -> 'LoggerService':
        """
        Create or return the singleton instance.

        Returns:
            The singleton LoggerService instance
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the logger if not already initialized."""
        if self._logger is None:
            self._setup_logger()

    def _setup_logger(self) -> None:
        """Configure the logger with file and console handlers."""
        self._logger = logging.getLogger('FileAutomation')
        self._logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler('automation.log', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        self._logger.addHandler(console_handler)
        self._logger.addHandler(file_handler)

    def info(self, message: str) -> None:
        """
        Log an info message.

        Args:
            message: The message to log
        """
        if self._logger:
            self._logger.info(message)

    def error(self, message: str) -> None:
        """
        Log an error message.

        Args:
            message: The error message to log
        """
        if self._logger:
            self._logger.error(message)

    def warning(self, message: str) -> None:
        """
        Log a warning message.

        Args:
            message: The warning message to log
        """
        if self._logger:
            self._logger.warning(message)

    def debug(self, message: str) -> None:
        """
        Log a debug message.

        Args:
            message: The debug message to log
        """
        if self._logger:
            self._logger.debug(message)