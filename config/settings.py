"""Application configuration settings."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass(frozen=True)
class AppConfig:
    """
    Application configuration container.

    Attributes:
        file_extensions: Mapping of file categories to their extensions
        log_file: Path to the log file
        max_duplicate_suffix: Maximum number for duplicate file renaming
    """

    file_extensions: Dict[str, List[str]]
    log_file: Path
    max_duplicate_suffix: int

    @staticmethod
    def get_default() -> 'AppConfig':
        """
        Get default application configuration.

        Returns:
            Default AppConfig instance
        """
        return AppConfig(
            file_extensions={
                'documents': ['.pdf', '.doc', '.docx', '.txt', '.odt'],
                'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
                'videos': ['.mp4', '.avi', '.mkv', '.mov', '.flv'],
                'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
                'archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
                'spreadsheets': ['.xls', '.xlsx', '.csv'],
                'code': ['.py', '.java', '.js', '.go', '.cpp', '.c', '.h'],
            },
            log_file=Path('automation.log'),
            max_duplicate_suffix=9999
        )