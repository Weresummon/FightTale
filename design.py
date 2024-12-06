# design.py

import pygame
import os  # Убедитесь, что этот импорт присутствует

# Цветовые константы
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 139)  # Тёмно-синий
CYAN = (0, 255, 255)      # Циановый

# Цвета для интерфейсов
COLOR_BATTLE_BG = (0, 0, 0)            # Чёрный
COLOR_BATTLE_ACCENT = DARK_BLUE        # Тёмно-синий
COLOR_BATTLE_TEXT = WHITE              # Белый
COLOR_HEALTH_BAR = (255, 140, 0)       # Тёмно-оранжевый

COLOR_MENU_BG = (0, 0, 0)
COLOR_MENU_ACCENT = DARK_BLUE          # Тёмно-синий
COLOR_MENU_TEXT = WHITE                # Белый

COLOR_VICTORY_BG = (0, 255, 0)
COLOR_VICTORY_TEXT = (0, 0, 0)
COLOR_DEFEAT_TEXT = (255, 0, 0)

TK_COLOR_MENU_BG = "#000000"
TK_COLOR_MENU_ACCENT = "#0000FF"        # Тёмно-синий
TK_COLOR_MENU_TEXT = "#FFFFFF"

# Загрузка шрифтов
FONT_PATH = "fonts"  # Убедитесь, что эта папка существует и содержит Jura.ttf и Kanit.ttf

try:
    FONT_MENU = pygame.font.Font(os.path.join(FONT_PATH, 'Jura.ttf'), 40)
except FileNotFoundError:
    print("Jura.ttf не найден. Используется системный шрифт.")
    FONT_MENU = pygame.font.SysFont('Arial', 40)

try:
    FONT_GAME = pygame.font.Font(os.path.join(FONT_PATH, 'Kanit.ttf'), 24)
except FileNotFoundError:
    print("Kanit.ttf не найден. Используется системный шрифт.")
    FONT_GAME = pygame.font.SysFont('Arial', 24)

# Цветовые схемы
color_schemes = {
    "scheme1": {
        # Цвета схемы 1
        "COLOR_BATTLE_BG": (0, 0, 0),
        "COLOR_BATTLE_ACCENT": (0, 0, 139),     # Тёмно-синий
        "COLOR_BATTLE_TEXT": (255, 255, 255),   # Белый
        "COLOR_HEALTH_BAR": (255, 140, 0),      # Тёмно-оранжевый

        "COLOR_MENU_BG": (0, 0, 0),
        "COLOR_MENU_ACCENT": (0, 0, 139),       # Тёмно-синий
        "COLOR_MENU_TEXT": (255, 255, 255),     # Белый

        "COLOR_VICTORY_BG": (0, 255, 0),
        "COLOR_VICTORY_TEXT": (0, 0, 0),
        "COLOR_DEFEAT_TEXT": (255, 0, 0),

        "TK_COLOR_MENU_BG": "#000000",
        "TK_COLOR_MENU_ACCENT": "#00008B",  # Тёмно-синий
        "TK_COLOR_MENU_TEXT": "#FFFFFF",

        # Новые цвета для кнопок
        "BUTTON_BORDER_COLOR_PYGAME": (0, 0, 139),       # Тёмно-синий
        "BUTTON_FILL_COLOR_PYGAME": (0, 0, 0),           # Чёрный
        "BUTTON_TEXT_COLOR_PYGAME": (0, 255, 255),       # Циановый

        "BUTTON_BORDER_COLOR_TK": "#00008B",              # Тёмно-синий
        "BUTTON_FILL_COLOR_TK": "#000000",                # Чёрный
        "BUTTON_TEXT_COLOR_TK": "#00FFFF",                # Циановый
    },
    "scheme2": {
        # Цвета схемы 2
        "COLOR_BATTLE_BG": (0, 0, 0),
        "COLOR_BATTLE_ACCENT": (255, 165, 0),  # Оранжевый
        "COLOR_BATTLE_TEXT": (255, 255, 255),  # Белый
        "COLOR_HEALTH_BAR": (255, 140, 0),

        "COLOR_MENU_BG": (0, 0, 0),
        "COLOR_MENU_ACCENT": (255, 165, 0),    # Оранжевый
        "COLOR_MENU_TEXT": (255, 255, 255),    # Белый

        "COLOR_VICTORY_BG": (0, 255, 0),
        "COLOR_VICTORY_TEXT": (255, 255, 255),
        "COLOR_DEFEAT_TEXT": (255, 0, 0),

        "TK_COLOR_MENU_BG": "#000000",
        "TK_COLOR_MENU_ACCENT": "#FFA500",  # Оранжевый
        "TK_COLOR_MENU_TEXT": "#FFFFFF",

        # Новые цвета для кнопок
        "BUTTON_BORDER_COLOR_PYGAME": (255, 165, 0),       # Оранжевый
        "BUTTON_FILL_COLOR_PYGAME": (0, 0, 0),             # Чёрный
        "BUTTON_TEXT_COLOR_PYGAME": (255, 255, 255),       # Белый

        "BUTTON_BORDER_COLOR_TK": "#FFA500",                # Оранжевый
        "BUTTON_FILL_COLOR_TK": "#000000",                  # Чёрный
        "BUTTON_TEXT_COLOR_TK": "#FFFFFF",                  # Белый
    },
    "scheme3": {
        # Цвета схемы 3
        "COLOR_BATTLE_BG": (0, 0, 0),
        "COLOR_BATTLE_ACCENT": (0, 0, 139),     # Тёмно-синий
        "COLOR_BATTLE_TEXT": (255, 255, 255),   # Белый
        "COLOR_HEALTH_BAR": (255, 140, 0),

        "COLOR_MENU_BG": (0, 0, 0),
        "COLOR_MENU_ACCENT": (0, 0, 139),       # Тёмно-синий
        "COLOR_MENU_TEXT": (255, 255, 255),     # Белый

        "COLOR_VICTORY_BG": (0, 255, 0),
        "COLOR_VICTORY_TEXT": (0, 0, 0),
        "COLOR_DEFEAT_TEXT": (255, 0, 0),

        "TK_COLOR_MENU_BG": "#000000",
        "TK_COLOR_MENU_ACCENT": "#00008B",  # Тёмно-синий
        "TK_COLOR_MENU_TEXT": "#FFFFFF",

        # Новые цвета для кнопок
        "BUTTON_BORDER_COLOR_PYGAME": (0, 0, 139),       # Тёмно-синий
        "BUTTON_FILL_COLOR_PYGAME": (0, 0, 0),           # Чёрный
        "BUTTON_TEXT_COLOR_PYGAME": (0, 255, 255),       # Циановый

        "BUTTON_BORDER_COLOR_TK": "#00008B",              # Тёмно-синий
        "BUTTON_FILL_COLOR_TK": "#000000",                # Чёрный
        "BUTTON_TEXT_COLOR_TK": "#00FFFF",                # Циановый
    },
}

# Установка текущей цветовой схемы
current_scheme = "scheme1"

# Инициализация переменных на уровне модуля
COLOR_BATTLE_BG = None
COLOR_BATTLE_ACCENT = None
COLOR_BATTLE_TEXT = None
COLOR_HEALTH_BAR = None

COLOR_MENU_BG = None
COLOR_MENU_ACCENT = None
COLOR_MENU_TEXT = None

COLOR_VICTORY_BG = None
COLOR_VICTORY_TEXT = None
COLOR_DEFEAT_TEXT = None

TK_COLOR_MENU_BG = None
TK_COLOR_MENU_ACCENT = None
TK_COLOR_MENU_TEXT = None

# Новые цвета для кнопок разделены на Pygame и Tkinter
BUTTON_BORDER_COLOR_PYGAME = None
BUTTON_FILL_COLOR_PYGAME = None
BUTTON_TEXT_COLOR_PYGAME = None

BUTTON_BORDER_COLOR_TK = None
BUTTON_FILL_COLOR_TK = None
BUTTON_TEXT_COLOR_TK = None

# Функция для установки цветовой схемы
def set_color_scheme(scheme_name):
    global COLOR_BATTLE_BG, COLOR_BATTLE_ACCENT, COLOR_BATTLE_TEXT, COLOR_HEALTH_BAR
    global COLOR_MENU_BG, COLOR_MENU_ACCENT, COLOR_MENU_TEXT
    global COLOR_VICTORY_BG, COLOR_VICTORY_TEXT, COLOR_DEFEAT_TEXT
    global TK_COLOR_MENU_BG, TK_COLOR_MENU_ACCENT, TK_COLOR_MENU_TEXT
    global BUTTON_BORDER_COLOR_PYGAME, BUTTON_FILL_COLOR_PYGAME, BUTTON_TEXT_COLOR_PYGAME
    global BUTTON_BORDER_COLOR_TK, BUTTON_FILL_COLOR_TK, BUTTON_TEXT_COLOR_TK

    scheme = color_schemes.get(scheme_name, color_schemes["scheme1"])

    COLOR_BATTLE_BG = scheme["COLOR_BATTLE_BG"]
    COLOR_BATTLE_ACCENT = scheme["COLOR_BATTLE_ACCENT"]
    COLOR_BATTLE_TEXT = scheme["COLOR_BATTLE_TEXT"]
    COLOR_HEALTH_BAR = scheme["COLOR_HEALTH_BAR"]

    COLOR_MENU_BG = scheme["COLOR_MENU_BG"]
    COLOR_MENU_ACCENT = scheme["COLOR_MENU_ACCENT"]
    COLOR_MENU_TEXT = scheme["COLOR_MENU_TEXT"]

    COLOR_VICTORY_BG = scheme["COLOR_VICTORY_BG"]
    COLOR_VICTORY_TEXT = scheme["COLOR_VICTORY_TEXT"]
    COLOR_DEFEAT_TEXT = scheme["COLOR_DEFEAT_TEXT"]

    TK_COLOR_MENU_BG = scheme["TK_COLOR_MENU_BG"]
    TK_COLOR_MENU_ACCENT = scheme["TK_COLOR_MENU_ACCENT"]
    TK_COLOR_MENU_TEXT = scheme["TK_COLOR_MENU_TEXT"]

    BUTTON_BORDER_COLOR_PYGAME = scheme["BUTTON_BORDER_COLOR_PYGAME"]
    BUTTON_FILL_COLOR_PYGAME = scheme["BUTTON_FILL_COLOR_PYGAME"]
    BUTTON_TEXT_COLOR_PYGAME = scheme["BUTTON_TEXT_COLOR_PYGAME"]

    BUTTON_BORDER_COLOR_TK = scheme["BUTTON_BORDER_COLOR_TK"]
    BUTTON_FILL_COLOR_TK = scheme["BUTTON_FILL_COLOR_TK"]
    BUTTON_TEXT_COLOR_TK = scheme["BUTTON_TEXT_COLOR_TK"]

# Применение текущей цветовой схемы
set_color_scheme(current_scheme)
