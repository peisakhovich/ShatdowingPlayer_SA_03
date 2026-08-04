import pygame

class Layout:
    # --------------------------------------------------
    # UI LAYER: WINDOWS Размеры окна
    # --------------------------------------------------
    WIDTH = 800
    HEIGHT = 600

    WINDOW_SIZE = (WIDTH, HEIGHT)

    # -------------------------
    # UI LAYER: CONTROL_PANEL
    # -------------------------
  
    CP_HEIGHT=100
    CP_RECT=pygame.Rect( 0, HEIGHT-CP_HEIGHT , WIDTH, CP_HEIGHT  )


    # -------------------------
    # UI LAYER: CHECK BOX BAR
    # -------------------------

    CB_DEFS = [
        ("show_text",        "show text",        True),
        ("voice_text",       "voice text",       True),
        ("show_translation", "show translation", True),
        ("voice_translation","voice translation",True),
    ]
    CB_X=250
    CB_Y=5
    CB_INTERVAL=20
  

    # -------------------------
    # UI LAYER: BUTTON BAR
    # -------------------------
    BTN_DEFS = [ "start","prev","play","pause","next","end","stop","quit","settings" ]

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

