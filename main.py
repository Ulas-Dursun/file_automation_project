"""
Main entry point for the File Automation Project.

Demonstrates file organization and data cleaning capabilities.
"""

from pathlib import Path
from config.settings import AppConfig
from utils.logger import LoggerService
from utils.file_utils import FileOperations
from services.file_organizer import FileOrganizer
from services.data_cleaner import DataCleaner
import pandas as pd
import random


def create_sample_files(test_dir: Path) -> None:
    """
    Create sample files for demonstration.

    Args:
        test_dir: Directory to create sample files in
    """
    FileOperations.ensure_directory(test_dir)

    sample_files = [
        'document1.pdf',
        'document2.txt',
        'image1.jpg',
        'image2.png',
        'video1.mp4',
        'code1.py',
        'code2.java',
        'archive1.zip',
        'spreadsheet1.xlsx',
        'duplicate.txt',
        'duplicate.txt',
    ]

    for filename in sample_files:
        file_path = test_dir / filename
        if not file_path.exists():
            file_path.write_text(f"Sample content for {filename}")


def create_sample_csv(csv_path: Path) -> None:
    """
    Create a realistic sample CSV file with significant data quality issues.

    Creates a dataset with:
    - 25 rows of employee data
    - ~30% missing values across different columns
    - 5 duplicate rows
    - Whitespace issues (leading/trailing spaces)
    - Mixed case inconsistencies

    Args:
        csv_path: Path where CSV should be created
    """
    random.seed(42)

    departments = ['HR', 'IT', 'Sales', 'Marketing', 'Finance']
    cities = ['Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya']
    names = [
        'Ahmet Yilmaz', 'Mehmet Kaya', 'Ayse Demir', 'Fatma Celik', 'Ali Sahin',
        'Zeynep Ozturk', 'Mustafa Arslan', 'Elif Kilic', 'Hasan Aslan', 'Hulya Polat',
        'Ibrahim Erdogan', 'Selin Kurt', 'Burak Ozkan', 'Deniz Acar', 'Emre Yildiz'
    ]

    data_rows = []

    for i in range(1, 26):
        name = random.choice(names)
        age = random.randint(23, 60) if random.random() > 0.25 else None
        salary = random.randint(40000, 120000) if random.random() > 0.30 else None
        department = random.choice(departments) if random.random() > 0.20 else None
        city = random.choice(cities) if random.random() > 0.25 else None

        if name and random.random() > 0.30:
            if random.random() > 0.5:
                name = f"  {name}  "
            else:
                name = f"{name} "

        if department and random.random() > 0.40:
            department = department.upper() if random.random() > 0.5 else department.lower()

        if city and random.random() > 0.50:
            city = f" {city} " if random.random() > 0.5 else city

        data_rows.append({
            'employee_id': i,
            'name': name,
            'age': age,
            'salary': salary,
            'department': department,
            'city': city,
            'years_experience': random.randint(0, 25) if random.random() > 0.35 else None
        })

    duplicate_rows = [data_rows[5].copy(), data_rows[10].copy(), data_rows[15].copy(),
                      data_rows[18].copy(), data_rows[22].copy()]
    data_rows.extend(duplicate_rows)

    random.shuffle(data_rows)

    df = pd.DataFrame(data_rows)

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)


def demonstrate_file_organization(config: AppConfig, logger: LoggerService) -> None:
    """
    Demonstrate file organization functionality.

    Args:
        config: Application configuration
        logger: Logger service instance
    """
    logger.info("=" * 60)
    logger.info("DEMONSTRATION: FILE ORGANIZATION")
    logger.info("=" * 60)

    test_dir = Path('tests/sample_data/file_organization')

    create_sample_files(test_dir)
    logger.info(f"Created sample files in: {test_dir}")

    organizer = FileOrganizer(config, logger)
    stats = organizer.organize_directory(test_dir)

    if stats:
        logger.info("File organization completed successfully")
    else:
        logger.error("File organization encountered errors")


def demonstrate_data_cleaning(logger: LoggerService) -> None:
    """
    Demonstrate data cleaning functionality.

    Args:
        logger: Logger service instance
    """
    logger.info("")
    logger.info("=" * 60)
    logger.info("DEMONSTRATION: DATA CLEANING")
    logger.info("=" * 60)

    input_csv = Path('tests/sample_data/dirty_data.csv')
    output_csv = Path('tests/sample_data/cleaned_data.csv')

    create_sample_csv(input_csv)
    logger.info(f"Created sample CSV with data quality issues: {input_csv}")

    try:
        df_dirty = pd.read_csv(input_csv)
        logger.info(f"Original data: {len(df_dirty)} rows, {len(df_dirty.columns)} columns")
        logger.info(f"Missing values: {df_dirty.isnull().sum().sum()}")
        logger.info(f"Duplicate rows: {df_dirty.duplicated().sum()}")
    except Exception:
        pass

    cleaner = DataCleaner(logger)
    stats = cleaner.clean_csv(input_csv, output_csv)

    if stats:
        logger.info("Data cleaning completed successfully")
        logger.info("")
        logger.info("BEFORE vs AFTER comparison:")
        logger.info(f"  Rows: {stats['initial_rows']} -> {stats['final_rows']} (removed {stats['rows_removed']})")
        logger.info(f"  Missing values handled: {stats['missing_values_found']}")
        logger.info(f"  Duplicates removed: {stats['duplicate_rows_found']}")
    else:
        logger.error("Data cleaning encountered errors")


def main() -> None:
    """Main execution function."""
    config = AppConfig.get_default()
    logger = LoggerService()

    logger.info("File Automation System Starting")
    logger.info(f"Python Project: SEN4015 - Advanced Programming with Python")
    logger.info("")

    demonstrate_file_organization(config, logger)
    demonstrate_data_cleaning(logger)

    logger.info("")
    logger.info("=" * 60)
    logger.info("ALL DEMONSTRATIONS COMPLETED")
    logger.info("=" * 60)
    logger.info("Check 'tests/sample_data/' directory for organized files")
    logger.info("Check 'automation.log' for detailed execution logs")
    logger.info("")
    logger.info("TO COMPARE DATA QUALITY:")
    logger.info("  - Open: tests/sample_data/dirty_data.csv (BEFORE)")
    logger.info("  - Open: tests/sample_data/cleaned_data.csv (AFTER)")


if __name__ == '__main__':
    main()