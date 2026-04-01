import subprocess
import os
import shutil
import pytest

MISSING_FIELDS_CSV_DIR = 'missing_fields_test_data/'
ALL_FIELDS_CSV_DIR = 'csv/examples/all-fields/'
CURRENT_SCRIPT = 'cohorts_csv.py'
BUGFIX_SCRIPT = 'cohorts_csv_fix.py'

@pytest.fixture
def test_output_dir():
    """
    Creates a temporary output dir before a test
    and cleans it up after the test runs.
    """
    TEST_OUTPUT_DIR = 'test_output/'
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    
    yield TEST_OUTPUT_DIR 
    
    print(f"\nCleaning up {TEST_OUTPUT_DIR}...")
    shutil.rmtree(TEST_OUTPUT_DIR)

def test_data_load_passes_with_all_data(test_output_dir):
    print("\nTesting for expected success with good data...")

    result = subprocess.run(
        [
            'python',
            CURRENT_SCRIPT,
            '-i', ALL_FIELDS_CSV_DIR,
            '-o', test_output_dir,
            '-d', 'test_dataset'
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed unexpectedly! Stderr: {result.stderr}"

def test_data_load_fails_with_missing_fields(test_output_dir):
    print("\nTesting for unexpected failure with missing, but valid, data...")
    
    result = subprocess.run(
        [
            'python', 
            CURRENT_SCRIPT,
            '-i', MISSING_FIELDS_CSV_DIR,
            '-o', test_output_dir,
            '-d', 'test_dataset'
        ],
        capture_output=True,
        text=True
    )
    
    assert result.returncode != 0, f"Script should not have completed successfully!"
    assert "Field required" in result.stderr
    assert "diseaseCode" in result.stderr

def test_bugfix_data_load_passes_with_missing_fields(test_output_dir):
    print("\nTesting for expected success with missing data and bugfix...")

    result = subprocess.run(
        [
            'python',
            BUGFIX_SCRIPT,
            '-i', MISSING_FIELDS_CSV_DIR,
            '-o', test_output_dir,
            '-d', 'test_dataset'
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed unexpectedly! Stderr: {result.stderr}"

def test_bugfix_data_load_passes_with_all_data(test_output_dir):
    print("\nTesting bugfix works with non-missing data...")

    result = subprocess.run(
        [
            'python',
            BUGFIX_SCRIPT,
            '-i', ALL_FIELDS_CSV_DIR,
            '-o', test_output_dir,
            '-d', 'test_dataset'
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed unexpectedly! Stderr: {result.stderr}"
