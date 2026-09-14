"""
Sound Language Studio
---------------------

Module:
    core.config

Purpose:
    Defines application-wide configuration values, including paths,
    UI settings, audio, logging, API, and splash screen options.

ru:
    Содержит основные настройки приложения: пути,
    параметры интерфейса, аудио, логирования, API и заставки.
"""

from pathlib import Path

class Config:
    """Класс конфигурации приложения."""

    TITLE = "Sound Language Studio"

    USER_DATA_DIR = Path.home() / "SoundLanguageStudio"

    AUDIO_CACHE_PATH = USER_DATA_DIR / "tmp" / "audio_cache"

    THEME = "gui/theme.json"

    FPS = 60

    PLAN_SESSION_FILE = Path("data/cache/plan_session.json")

    ICON_APP = "SA_AppIconsGirl.png"

    ICON_PATH = "gui/assets/images/icons"

    APP_ICON = f"{ICON_PATH}/{ICON_APP}"

    # Fonts 
    FONT_PATH = "gui/assets/fonts/inter"
    FONT_REGULAR = "Inter_Regular.ttf"
    FONT_BOLD = "Inter_Bold.ttf"
    FONT_BOLDITALIC = "Inter_BoldItalic.ttf"
    FONT_ITALIC = "Inter_Italic.ttf"

    

    # Logging
    LOG_MODE = "logging"      # "print" | "logging" | "stop"
    LOG_FILE = Path("logs/sa_03.log")

    API_BASE_URL = "https://sa03-api-gxd7gve7a9gafnaz.polandcentral-01.azurewebsites.net/api"

    # Splash screen
    SHOW_SPLASH = True
    SPLASH_DURATION = 10.0
    SPLASH_IMAGE = "gui/assets/images/SLS_logo_info.png"
    SPLASH_SOUND_ENABLED = True
    SPLASH_SOUND = "gui/assets/sounds/sound_language_studio_intro_v2_cinematic.wav"