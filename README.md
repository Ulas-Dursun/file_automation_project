# File Automation System

A Python-based automation tool for organizing files and cleaning CSV data.

## Features

- **File Organization**: Automatically sorts files into categorized folders (documents, images, videos, etc.)
- **Data Cleaning**: Handles missing values, removes duplicates, and standardizes CSV data
- **Smart Duplicate Handling**: Renames duplicate files automatically
- **Detailed Logging**: Tracks all operations with timestamps

## Project Structure

```
file_automation_project/
├── config/
│   ├── __init__.py
│   └── settings.py          # Application configuration
├── services/
│   ├── __init__.py
│   ├── file_organizer.py    # File organization logic
│   └── data_cleaner.py      # CSV cleaning logic
├── utils/
│   ├── __init__.py
│   ├── logger.py            # Logging service
│   └── file_utils.py        # File operations
└── main.py                  # Entry point
```

## Requirements

- Python 3.10+
- pandas

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/file_automation_project.git
cd file_automation_project
```

2. Install dependencies:
```bash
pip install pandas
```

## Usage

Run the main script to see demonstrations:
```bash
python main.py
```

The script will:
1. Create sample files in `tests/sample_data/file_organization/`
2. Organize them into categorized folders
3. Create a dirty CSV with data quality issues
4. Clean the CSV and save the result

### Results

Check the following locations:
- Organized files: `tests/sample_data/file_organization/`
- Cleaned CSV: `tests/sample_data/cleaned_data.csv`
- Execution logs: `automation.log`

## Example Output

```
File Automation System Starting
============================================================
DEMONSTRATION: FILE ORGANIZATION
============================================================
Moved document1.pdf -> documents/document1.pdf
Moved image1.jpg -> images/image1.jpg
Organization complete. Total files moved: 10
  documents: 3 files
  images: 2 files
  videos: 1 files
  ...

============================================================
DEMONSTRATION: DATA CLEANING
============================================================
Original data: 30 rows, 7 columns
Missing values: 48
Duplicate rows: 5

BEFORE vs AFTER comparison:
  Rows: 30 -> 25 (removed 5)
  Missing values handled: 48
  Duplicates removed: 5
```

## Supported File Types

- **Documents**: PDF, DOC, DOCX, TXT, ODT
- **Images**: JPG, JPEG, PNG, GIF, BMP, SVG
- **Videos**: MP4, AVI, MKV, MOV, FLV
- **Audio**: MP3, WAV, FLAC, AAC, OGG
- **Archives**: ZIP, RAR, 7Z, TAR, GZ
- **Spreadsheets**: XLS, XLSX, CSV
- **Code**: PY, JAVA, JS, GO, CPP, C, H

**University Project** - January 2026
