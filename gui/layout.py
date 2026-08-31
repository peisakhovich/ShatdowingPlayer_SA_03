import pygame

class Layout:
    # --------------------------------------------------
    # UI LAYER: WINDOWS Размеры окна
    # --------------------------------------------------
    WIDTH = 900
    HEIGHT = 700

    WINDOW_SIZE = (WIDTH, HEIGHT)

    # -------------------------
    # UI LAYER: CONTROL_PANEL
    # -------------------------
  
    CP_HEIGHT=130
    CP_RECT=pygame.Rect( 0, HEIGHT-CP_HEIGHT , WIDTH, CP_HEIGHT  )


    # -------------------------
    # UI LAYER: CHECK BOX BAR in ControlPanel
    # -------------------------

    CB_DEFS = {
        "loop": ("repeat current", False),
        "randomize": ("random order", False),
    }
    CB_X=280
    CB_Y=10
    CB_INTERVAL=22
    CB_FONT_SIZE=12
  

    # -------------------------
    # UI LAYER: BUTTON BAR in ControlPanel
    # -------------------------
    BTN_DEFS = [ "first","prev","play","pause","next","last","stop","quit","settings","db" ]
    

    BTN_WIDTH = 32
    BTN_HEIGHT = 32

    BTN_SIZE = (BTN_WIDTH, BTN_HEIGHT)
    BTN_INTERVAL = 10 # Interval between buttons

    LEN_BUTTONS = (
            len(BTN_DEFS) * BTN_WIDTH +
            (len(BTN_DEFS) - 1) * BTN_INTERVAL
        )
    
    BTN_START_X = CP_RECT.width - CP_RECT.x - LEN_BUTTONS - BTN_WIDTH
    BTN_START_Y = CP_RECT.centery - BTN_HEIGHT // 2

    # -------------------------
    # UI LAYER: SLIDER BAR in ControlPanel
    # -------------------------
    SLIDER_DEFS = [
        {
            "name": "voice_speed",
            "caption": "Voice Speed",
            "start": 1.0,
            "range": (0.1, 1.2),
            "formatter": lambda v: f"{v:.2f}x",
        },
        {
            "name": "factor_pause_before_translation",
            "caption": "Factor Pause before Translation",
            "start": 1.0,
            "range": (0.1, 4.0),
            "formatter": lambda v: f"{v:.2f}x",
        },
        {
            "name": "pause_between_sentences",
            "caption": "Pause between Sentences",
            "start": 2000,
            "range": (0, 8000),
            "formatter": lambda v: f"{v/1000:.1f} s",
        }
    ]
    HSL_X=10
    HSL_Y=24
    HSL_TRACK_WIDTH=180
    HSL_FONT_SIZE=11

    # -------------------------
    # UI LAYER: SETTINGS WINDOW
    # -------------------------

    SETTINGS_WIDTH = 550
    SETTINGS_HEIGHT = 700

    SETTINGS_RECT = pygame.Rect(
        (WIDTH - SETTINGS_WIDTH) // 2,
        (HEIGHT - SETTINGS_HEIGHT) // 2,
        SETTINGS_WIDTH,
        SETTINGS_HEIGHT
    )

    # -------------------------
    # UI LAYER: DATABASE WINDOW
    # DB_CONTROL PANEL
    # -------------------------

    DB_BTN_INTERVAL = 20 # Interval between buttons
    DB_WIDTH = WIDTH-DB_BTN_INTERVAL*2
    DB_HEIGHT = HEIGHT-DB_BTN_INTERVAL*2

    DB_RECT = pygame.Rect(
        DB_BTN_INTERVAL,
        DB_BTN_INTERVAL,
        DB_WIDTH,
        DB_HEIGHT
    )

    DB_BTN_DEFS = [ "settodb","dbtoset","settoexcel","exceltoset","dropset","login","register" ]

    DB_CP_HEIGHT=100
    DB_CP_RECT=pygame.Rect(   DB_RECT.left, DB_RECT.bottom - DB_CP_HEIGHT , DB_WIDTH, DB_CP_HEIGHT  )

    DB_BTN_WIDTH = 64
    DB_BTN_HEIGHT = 32

    DB_BTN_SIZE = (DB_BTN_WIDTH, DB_BTN_HEIGHT)
    
    DB_LEN_BUTTONS = (
            len(DB_BTN_DEFS) * DB_BTN_WIDTH +
            (len(DB_BTN_DEFS) - 1) * DB_BTN_INTERVAL
        )
    
    DB_BTN_START_X = DB_CP_RECT.width - DB_CP_RECT.x - DB_LEN_BUTTONS - DB_BTN_WIDTH
    DB_BTN_START_Y = DB_CP_RECT.centery - DB_BTN_HEIGHT // 2