import pygame
#--------------------------------------
# темы для виджетов на базе pgame.rect
#--------------------------------------
class Theme:
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
    HSL_KNOB_HEIGHT = 20
    HSL_KNOB_RADIUS = 4

    # Текст значения
    HSL_TEXT_COLOR = pygame.Color("#91E5FF")


    # --------------------------------------------------
    # Dialog
    # --------------------------------------------------

    DIALOG_MIN_WIDTH = 320
    DIALOG_HEIGHT = 160

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

