from pathlib import Path

class Config:

    TITLE = "SA_03 Shadowing App"

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

    #AUDIO_CACHE_PATH = "SA_O3/data/audio_cache"
    AUDIO_CACHE_PATH = f"C:\\Users\\liudm\\SadowingApp\\tmp\\audio_cache"

    # Logging
    LOG_MODE = "print"      # "print" | "logging" | "stop"
    LOG_FILE = Path("logs/sa_03.log")

    API_BASE_URL = "https://sa03-api-gxd7gve7a9gafnaz.polandcentral-01.azurewebsites.net/api"