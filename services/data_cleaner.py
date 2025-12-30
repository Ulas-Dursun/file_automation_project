"""Data cleaning service for CSV files."""

from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
from utils.logger import LoggerService


class DataCleaner:
    """
    Service for cleaning CSV data files.

    Handles missing values, duplicate rows, and data type inconsistencies.
    """

    def __init__(self, logger: LoggerService) -> None:
        """
        Initialize the data cleaner.

        Args:
            logger: Logger service instance
        """
        self._logger = logger

    def clean_csv(self, file_path: Path, output_path: Path) -> Dict[str, Any]:
        """
        Clean a CSV file and save the result.

        Args:
            file_path: Path to the input CSV file
            output_path: Path for the cleaned output CSV file

        Returns:
            Dictionary containing cleaning statistics
        """
        if not file_path.exists() or not file_path.is_file():
            self._logger.error(f"CSV file does not exist: {file_path}")
            return {}

        self._logger.info(f"Starting data cleaning: {file_path.name}")

        try:
            df = pd.read_csv(file_path)
            initial_rows = len(df)
            initial_cols = len(df.columns)

            stats: Dict[str, Any] = {
                'initial_rows': initial_rows,
                'initial_columns': initial_cols,
                'missing_values_found': int(df.isnull().sum().sum()),
                'duplicate_rows_found': int(df.duplicated().sum())
            }

            df_cleaned = self._remove_duplicates(df)
            df_cleaned = self._handle_missing_values(df_cleaned)
            df_cleaned = self._standardize_data_types(df_cleaned)

            stats['final_rows'] = len(df_cleaned)
            stats['final_columns'] = len(df_cleaned.columns)
            stats['rows_removed'] = initial_rows - len(df_cleaned)

            output_path.parent.mkdir(parents=True, exist_ok=True)
            df_cleaned.to_csv(output_path, index=False)

            self._log_cleaning_stats(stats, file_path.name)
            self._logger.info(f"Cleaned data saved to: {output_path}")

            return stats

        except Exception as e:
            self._logger.error(f"Error cleaning CSV {file_path.name}: {str(e)}")
            return {}

    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate rows from DataFrame.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with duplicates removed
        """
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            self._logger.info(f"Removing {duplicates} duplicate rows")
            return df.drop_duplicates().copy()
        return df.copy()

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in DataFrame.

        Strategy:
        - Numeric columns: fill with median
        - Categorical columns: fill with mode or 'Unknown'

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with missing values handled
        """
        missing_count = df.isnull().sum().sum()
        if missing_count == 0:
            return df

        self._logger.info(f"Handling {missing_count} missing values")

        df = df.copy()

        for column in df.columns:
            if df[column].isnull().any():
                if pd.api.types.is_numeric_dtype(df[column]):
                    median_value = df[column].median()
                    df[column] = df[column].fillna(median_value)
                    self._logger.debug(f"Filled numeric column '{column}' with median: {median_value}")
                else:
                    mode_values = df[column].mode()
                    fill_value = mode_values[0] if len(mode_values) > 0 else 'Unknown'
                    df[column] = df[column].fillna(fill_value)
                    self._logger.debug(f"Filled categorical column '{column}' with: {fill_value}")

        return df

    def _standardize_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize data types where possible.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with standardized types
        """
        df = df.copy()

        for column in df.columns:
            if df[column].dtype == 'object':
                df[column] = df[column].str.strip()

        return df

    def _log_cleaning_stats(self, stats: Dict[str, Any], filename: str) -> None:
        """
        Log cleaning statistics.

        Args:
            stats: Statistics dictionary
            filename: Name of the file being cleaned
        """
        self._logger.info(f"Cleaning statistics for {filename}:")
        self._logger.info(f"  Initial rows: {stats['initial_rows']}, Final rows: {stats['final_rows']}")
        self._logger.info(f"  Missing values handled: {stats['missing_values_found']}")
        self._logger.info(f"  Duplicate rows removed: {stats['duplicate_rows_found']}")