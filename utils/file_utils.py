"""File operation utilities."""

from pathlib import Path
from typing import List
import shutil


class FileOperations:
    """
    Utility class for common file operations.

    Provides static methods for file system operations used across services.
    """

    @staticmethod
    def ensure_directory(path: Path) -> None:
        """
        Ensure a directory exists, create if it doesn't.

        Args:
            path: Directory path to ensure
        """
        path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_files_in_directory(directory: Path, recursive: bool = False) -> List[Path]:
        """
        Get all files in a directory.

        Args:
            directory: Directory to search
            recursive: Whether to search recursively

        Returns:
            List of file paths
        """
        if not directory.exists() or not directory.is_dir():
            return []

        if recursive:
            return [f for f in directory.rglob('*') if f.is_file()]
        else:
            return [f for f in directory.iterdir() if f.is_file()]

    @staticmethod
    def move_file(source: Path, destination: Path) -> bool:
        """
        Move a file from source to destination.

        Args:
            source: Source file path
            destination: Destination file path

        Returns:
            True if successful, False otherwise
        """
        try:
            shutil.move(str(source), str(destination))
            return True
        except Exception:
            return False

    @staticmethod
    def get_unique_filename(directory: Path, filename: str, max_suffix: int = 9999) -> Path:
        """
        Generate a unique filename by appending a numeric suffix if needed.

        Args:
            directory: Target directory
            filename: Original filename
            max_suffix: Maximum suffix number to try

        Returns:
            Unique file path
        """
        base_path = directory / filename

        if not base_path.exists():
            return base_path

        stem = base_path.stem
        suffix = base_path.suffix

        for i in range(1, max_suffix + 1):
            new_path = directory / f"{stem}_{i}{suffix}"
            if not new_path.exists():
                return new_path

        return directory / f"{stem}_final{suffix}"