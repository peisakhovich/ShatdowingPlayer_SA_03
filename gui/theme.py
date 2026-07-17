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
    HSL_TRACK_HEIGHT = 6
    HSL_TRACK_RADIUS = 3

    # Заполненная часть дорожки (слева от бегунка)
    HSL_PROGRESS_COLOR = pygame.Color("#3B82F6")

    # Бегунок
    HSL_KNOB_COLOR = pygame.Color("#F0F0F0")
    HSL_KNOB_BORDER_COLOR = pygame.Color("#404040")
    HSL_KNOB_BORDER_WIDTH = 1

    HSL_KNOB_WIDTH = 14
    HSL_KNOB_HEIGHT = 22
    HSL_KNOB_RADIUS = 7

    # Текст значения
    HSL_TEXT_COLOR = pygame.Color("#FFFFFF")


