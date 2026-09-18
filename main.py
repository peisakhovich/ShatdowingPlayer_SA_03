"""
Sound Language Studio
---------------------

Module:
    main

Purpose:
    Application entry point.

ru:
    Точка входа приложения.
"""

from pathlib import Path
import shutil

from dotenv import load_dotenv

from core.application import Application


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
ENV_DEFAULT_FILE = BASE_DIR / ".env_default"


def prepare_environment():
    if not ENV_FILE.exists():
        shutil.copy2(ENV_DEFAULT_FILE, ENV_FILE)

    load_dotenv(ENV_FILE)


def main():
    prepare_environment()

    app = Application()
    app.run()


if __name__ == "__main__":
    main()