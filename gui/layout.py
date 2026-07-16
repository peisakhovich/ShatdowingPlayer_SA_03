class Layout:
    # --------------------------------------------------
    # Размеры окна
    # --------------------------------------------------
    WIDTH = 1000
    HEIGHT = 600

    WINDOW_SIZE = (WIDTH, HEIGHT)

    # -------------------------
    # UI LAYER: BUTTON BAR
    # -------------------------
    BUTTON_DEFS = [ "start","prev","play","pause","next","end","stop",    ]

    # --------------------------------------------------
    # Кнопки управления
    # --------------------------------------------------
    BTN_WIDTH = 32
    BTN_HEIGHT = 32

    BTN_SIZE = (BTN_WIDTH, BTN_HEIGHT)
    BTN_INTERVAL = 10 # Interval between buttons

    LEN_BUTTONS = (len(BUTTON_DEFS)+1)*((BTN_SIZE[1]+BTN_INTERVAL))+BTN_INTERVAL
    BTN_START = (WIDTH-LEN_BUTTONS,HEIGHT-(BTN_SIZE[1]+BTN_INTERVAL)*4 ) # (x, y) координаты верхнего левого угла начала кнопок
    BTN_PARAM = ( BTN_START[0], BTN_START[1], BTN_SIZE[0],BTN_SIZE[1], BTN_INTERVAL)