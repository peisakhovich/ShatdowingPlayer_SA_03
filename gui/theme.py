import pygame
#--------------------------------------
# темы для виджетов на базе pgame.rect
#--------------------------------------
class Theme:

    # =====================================================
    # TextEdit
    # =====================================================

    TE_BACKGROUND_COLOR = pygame.Color("#303030")
    TE_BORDER_COLOR = pygame.Color("#6EAEDB")
    TE_BORDER_WIDTH = 2
    TE_RADIUS = 6

    TE_FOCUS_BORDER_COLOR = pygame.Color("#7FE8FF")
    TE_FOCUS_BORDER_WIDTH = 2

    TE_TEXT_COLOR = pygame.Color("#91E5FF")
    TE_CURSOR_COLOR = pygame.Color("#FFFFFF")

    TE_PADDING_X = 8
    TE_PADDING_Y = 6
    TE_SELECTION_COLOR = pygame.Color("#405A7A")

    TE_SCROLL_SPEED = 3
    TE_SCROLLBAR_WIDTH = 8

    #--------------------------------------
    # fore control_panel (prefix:TCP)
    #--------------------------------------

    TCP_BACKGROUND_COLOR=pygame.Color("#1E1A3A")
    TCP_BORDER_LINE_COLOR=pygame.Color("#3823f3")
    TCP_BORDER_LINE_WIDTH=2
    TCP_BORDER_LINE_RADIUS=10
 
    
    # --------------------------------------
    # Horizontal Slider (HSL)
    # --------------------------------------

    # Дорожка
    HSL_TRACK_COLOR = pygame.Color("#5A5A5A")
    HSL_TRACK_HEIGHT = 5
    HSL_TRACK_RADIUS = 2

    # Заполненная часть дорожки (слева от бегунка)
    HSL_PROGRESS_COLOR = pygame.Color("#3B82F6")

    # Бегунок
    HSL_KNOB_COLOR = pygame.Color("#F0F0F0")
    HSL_KNOB_BORDER_COLOR = pygame.Color("#404040")
    HSL_KNOB_BORDER_WIDTH = 2

    HSL_KNOB_WIDTH = 12
    HSL_KNOB_HEIGHT = 25
    HSL_KNOB_RADIUS = 4

    # Текст значения
    HSL_TEXT_COLOR = pygame.Color("#91E5FF")


    # --------------------------------------------------
    # Dialog
    # --------------------------------------------------

    DIALOG_MIN_WIDTH = 220
    DIALOG_HEIGHT = 120

    DIALOG_PADDING_X = 20
    DIALOG_PADDING_Y = 16

    DIALOG_HEADER_HEIGHT = 36
    DIALOG_RADIUS = 8

    DIALOG_BUTTON_HEIGHT = 30
    DIALOG_BUTTON_INTERVAL = 12

    DIALOG_BUTTON_PADDING_X = 16
    DIALOG_BUTTON_PADDING_Y = 6

    DIALOG_OVERLAY_ALPHA = 170

    DIALOG_BACKGROUND_COLOR = pygame.Color("#2D343C")
    DIALOG_BORDER_COLOR = pygame.Color("#1A4D5C")
    DIALOG_SEPARATOR_COLOR = pygame.Color("#4A5966")

    DIALOG_TITLE_COLOR = pygame.Color("#91E5FF")
    DIALOG_TEXT_COLOR = pygame.Color("#E0E0E0")

    DIALOG_BUTTON_COLOR = pygame.Color("#364049")
    DIALOG_BUTTON_HOVER_COLOR = pygame.Color("#4B6274")
    DIALOG_BUTTON_BORDER_COLOR = pygame.Color("#1085A8")
    DIALOG_BUTTON_TEXT_COLOR = pygame.Color("#91E5FF")

    DIALOG_OVERLAY_COLOR = pygame.Color("#000000")

    # --------------------------------------------------
    # UI LAYER: TEXT_BUTTON
    # --------------------------------------------------

    TB_HEIGHT = 30

    TB_PADDING_X = 16
    TB_PADDING_Y = 6

    TB_BACKGROUND_COLOR = pygame.Color("#0E4792")
    TB_BACKGROUND_HOVER_COLOR = pygame.Color("#811165")
    TB_BACKGROUND_PRESSED_COLOR = pygame.Color("#7EBE52")

    TB_BORDER_COLOR = pygame.Color("#5947F8")
    TB_BORDER_WIDTH = 1
    TB_FOCUS_BORDER_COLOR = pygame.Color("#7FE8FF")
    TB_FOCUS_BORDER_WIDTH = 3

    TB_RADIUS = 8

    TB_TEXT_COLOR = pygame.Color("#91E5FF")
    TB_TEXT_PRESSED_COLOR = pygame.Color("#FFFFFF")

    # --------------------------------------------------
    # UI LAYER: CHECK_BOX
    # --------------------------------------------------

    CB_SIZE = 18
    CB_INTERVAL = 8
    CB_RADIUS = 3
    CB_BORDER_WIDTH = 2
    CB_CHECK_WIDTH = 3
    CB_CHECK_PADDING = 4

    CB_BACKGROUND_COLOR = pygame.Color("#0E4792")
    CB_BACKGROUND_HOVER_COLOR = pygame.Color("#681515")
    CB_BORDER_COLOR = pygame.Color("#5947F8")
    CB_CHECK_COLOR = pygame.Color("#91E5FF")
    CB_TEXT_COLOR = pygame.Color("#91E5FF")

    # =====================================================
    # TextWindow
    # =====================================================

    TW_BACKGROUND_COLOR = pygame.Color("#303030")
    TW_BORDER_COLOR = pygame.Color("#6EAEDB")
    TW_TEXT_COLOR = pygame.Color("#91E5FF")
    TW_BORDER_WIDTH = 2
    TW_RADIUS = 6
    TW_PADDING_X = 8
    TW_PADDING_Y = 6

