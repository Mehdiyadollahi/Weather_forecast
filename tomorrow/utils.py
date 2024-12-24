import hashlib
from datetime import datetime

def calculate_md5(text):
    """Calculates the MD5 hash of a given text string.

    Args:
        text: The input text string.

    Returns:
        The MD5 hash as a hexadecimal string.
    """

    md5_hash = hashlib.md5()
    md5_hash.update(text.encode())
    return md5_hash.hexdigest()

def format_datetime(timestamp_str):
    """Formats a timestamp string to a datetime object.

    Args:
        timestamp_str: The timestamp string in ISO 8601 format.

    Returns:
        A datetime object.
    """

    return datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))