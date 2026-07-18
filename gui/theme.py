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


