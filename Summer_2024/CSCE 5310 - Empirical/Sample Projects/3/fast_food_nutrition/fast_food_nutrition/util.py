import os


TEST_DIR = os.path.join(os.path.dirname(__file__), "../tests/data")


def get_full_qualified_file_name(file_name: str) -> str:
    return os.path.join(TEST_DIR, file_name)
