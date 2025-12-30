"""File organization service."""

from pathlib import Path
from typing import Dict, List, Set
from config.settings import AppConfig
from utils.logger import LoggerService
from utils.file_utils import FileOperations


class FileOrganizer:
    """
    Service for organizing files by type into categorized folders.

    Moves files into subdirectories based on their extensions and handles
    duplicate filenames automatically.
    """

    def __init__(self, config: AppConfig, logger: LoggerService) -> None:
        """
        Initialize the file organizer.

        Args:
            config: Application configuration
            logger: Logger service instance
        """
        self._config = config
        self._logger = logger
        self._extension_map = self._build_extension_map()

    def _build_extension_map(self) -> Dict[str, str]:
        """
        Build a reverse mapping from extension to category.

        Returns:
            Dictionary mapping extensions to category names
        """
        extension_map: Dict[str, str] = {}
        for category, extensions in self._config.file_extensions.items():
            for ext in extensions:
                extension_map[ext.lower()] = category
        return extension_map

    def organize_directory(self, directory: Path) -> Dict[str, int]:
        """
        Organize all files in a directory by their type.

        Args:
            directory: Directory to organize

        Returns:
            Dictionary with statistics: moved count per category
        """
        if not directory.exists() or not directory.is_dir():
            self._logger.error(f"Directory does not exist: {directory}")
            return {}

        self._logger.info(f"Starting file organization in: {directory}")

        files = FileOperations.get_files_in_directory(directory, recursive=False)
        stats: Dict[str, int] = {}
        processed_files: Set[Path] = set()

        for file_path in files:
            if file_path in processed_files:
                continue

            category = self._get_file_category(file_path)

            if category == 'other':
                self._logger.debug(f"Skipping uncategorized file: {file_path.name}")
                continue

            target_dir = directory / category
            FileOperations.ensure_directory(target_dir)

            target_path = FileOperations.get_unique_filename(
                target_dir,
                file_path.name,
                self._config.max_duplicate_suffix
            )

            if FileOperations.move_file(file_path, target_path):
                stats[category] = stats.get(category, 0) + 1
                processed_files.add(file_path)
                self._logger.info(f"Moved {file_path.name} -> {category}/{target_path.name}")
            else:
                self._logger.error(f"Failed to move {file_path.name}")

        self._log_statistics(stats)
        return stats

    def _get_file_category(self, file_path: Path) -> str:
        """
        Determine the category of a file based on its extension.

        Args:
            file_path: Path to the file

        Returns:
            Category name or 'other' if not recognized
        """
        extension = file_path.suffix.lower()
        return self._extension_map.get(extension, 'other')

    def _log_statistics(self, stats: Dict[str, int]) -> None:
        """
        Log organization statistics.

        Args:
            stats: Dictionary with moved file counts per category
        """
        total = sum(stats.values())
        self._logger.info(f"Organization complete. Total files moved: {total}")
        for category, count in sorted(stats.items()):
            self._logger.info(f"  {category}: {count} files")