"""
Lumen Nation central configuration.

No secrets belong in source control.
Environment variables may override safe defaults.
"""

from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = Path(
    os.environ.get(
        "LUMEN_DATABASE",
        str(DATABASE_DIR / "lumen.db")
    )
)

APP_NAME = "Lumen Nation"
APP_VERSION = "0.5.0"

HOST = os.environ.get("LUMEN_HOST", "127.0.0.1")

try:
    PORT = int(os.environ.get("LUMEN_PORT", "8000"))
except ValueError:
    PORT = 8000

DEBUG = os.environ.get("LUMEN_DEBUG", "0") == "1"

MAX_MESSAGE_LENGTH = 10000
MAX_USERNAME_LENGTH = 100

DATABASE_TIMEOUT_SECONDS = 10
