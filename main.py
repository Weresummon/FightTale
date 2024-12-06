# main.py

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"  # Установите нужные координаты X,Y
import pygame
pygame.init()  # Инициализация Pygame перед импортом других модулей

import tkinter as tk
from tkinter import messagebox

from battle_controller import start_battle
from monsters import get_all_monsters
import design

# --- API Функции ---
def fetch_data_from_wiki(keyword):
    import requests
    from bs4 import BeautifulSoup

    url = f"https://undertale.fandom.com/wiki/{keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {
        "title": keyword,
        "link": url,
        "description": ""
    }

    paragraphs = soup.find_all('p', limit=3)
    description = " ".join(p.get_text(strip=True) for p in paragraphs)
    if description:
        data["description"] = description

    with open(f'{keyword}_data.json', 'w', encoding='utf-8') as json_file:
        import json
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    return data

def show_data_in_messagebox(data):
    popup = tk.Toplevel()
    popup.title(data['title'])

    # Получаем текущий размер окна Pygame
    pygame_window_x, pygame_window_y = 100, 100  # Соответствует SDL_VIDEO_WINDOW_POS
    play_button_x, play_button_y, play_button_width, play_button_height = WINDOW_WIDTH // 2 - 100, 300, 200, 60

    # Вычисляем позицию для окна Tkinter
    tk_window_width, tk_window_height = 300, 200
    tk_x = pygame_window_x + play_button_x
    tk_y = pygame_window_y + play_button_y + play_button_height + 10  # 10 пикселей отступа

    popup.geometry(f"{tk_window_width}x{tk_window_height}+{tk_x}+{tk_y}")
    popup.configure(bg=design.TK_COLOR_MENU_BG)

    text = tk.Text(popup, wrap='word', font=('Arial', 14), bg=design.TK_COLOR_MENU_BG, fg=design.TK_COLOR_MENU_TEXT)
    text.insert('1.0', f"Title: {data['title']}\n\n")
    text.insert('end', f"Link: {data['link']}\n\n")
    text.insert('end', f"Description: {data['description']}\n")
    text.config(state='disabled')
    text.pack(expand=True, fill='both')

    close_button = tk.Button(popup, text="Закрыть", command=popup.destroy, font=('Arial', 12),
                             bg=design.BUTTON_FILL_COLOR_TK, fg=design.BUTTON_TEXT_COLOR_TK)
    close_button.pack(pady=10)

def frisk_request():
    data = fetch_data_from_wiki("Frisk")
    show_data_in_messagebox(data)

def tobyfox_request():
    data = fetch_data_from_wiki("Toby_Fox")
    show_data_in_messagebox(data)

def api_menu():
    root = tk.Tk()
    root.title("Wiki Fetcher")
    root.configure(bg=design.TK_COLOR_MENU_BG)

    # Кнопки для запросов
    frisk_button = tk.Button(root, text="Запрос Фриск", command=frisk_request,
                             bg=design.BUTTON_FILL_COLOR_TK, fg=design.BUTTON_TEXT_COLOR_TK, font=('Arial', 12))
    frisk_button.pack(pady=10)

    tobyfox_button = tk.Button(root, text="Запрос Тоби Фокса", command=tobyfox_request,
                               bg=design.BUTTON_FILL_COLOR_TK, fg=design.BUTTON_TEXT_COLOR_TK, font=('Arial', 12))
    tobyfox_button.pack(pady=10)

    input_label = tk.Label(root, text="Введите ключевые слова:",
                           bg=design.TK_COLOR_MENU_BG, fg=design.TK_COLOR_MENU_TEXT)
    input_label.pack(pady=5)

    input_entry = tk.Entry(root, width=40)
    input_entry.pack(pady=5)

    def fetch_from_input():
        user_input = input_entry.get().strip()
        if not user_input:
            messagebox.showerror("Error", "Введите хотя бы одно слово для поиска.")
            return
        try:
            data = fetch_data_from_wiki(user_input)
            show_data_in_messagebox(data)
        except Exception as e:
            messagebox.showerror("Error", f"Ошибка получения данных: {e}")

    fetch_button = tk.Button(root, text="Получить данные", command=fetch_from_input,
                             bg=design.BUTTON_FILL_COLOR_TK, fg=design.BUTTON_TEXT_COLOR_TK, font=('Arial', 12))
    fetch_button.pack(pady=10)

    root.mainloop()

# --- Основные функции ---
def select_account():
    users = [
        {"name": "Player1", "health": 100, "max_health": 100, "feature": "решительность"},
        {"name": "Player2", "health": 120, "max_health": 120, "feature": "вера", "shield_active": False},
        {"name": "Player3", "health": 90, "max_health": 90, "feature": "душа смелости", "speed_multiplier": 1, "acceleration": 1}
    ]

    root = tk.Tk()
    root.title("Выбор аккаунта")

    # Получаем текущий размер окна Pygame
    pygame_window_x, pygame_window_y = 100, 100  # Соответствует SDL_VIDEO_WINDOW_POS
    play_button_x, play_button_y, play_button_width, play_button_height = WINDOW_WIDTH // 2 - 100, 300, 200, 60

    # Вычисляем позицию для окна Tkinter
    tk_window_width, tk_window_height = 300, 200
    tk_x = pygame_window_x + play_button_x
    tk_y = pygame_window_y + play_button_y + play_button_height + 10  # 10 пикселей отступа

    root.geometry(f"{tk_window_width}x{tk_window_height}+{tk_x}+{tk_y}")
    root.configure(bg=design.TK_COLOR_MENU_BG)

    label = tk.Label(root, text="Выберите аккаунт:",
                     bg=design.TK_COLOR_MENU_BG, fg=design.TK_COLOR_MENU_TEXT)
    label.pack(pady=10)

    selected_user = {}

    def select_user(user):
        nonlocal selected_user
        selected_user = user
        root.destroy()

    for user in users:
        btn = tk.Button(root, text=user["name"], command=lambda u=user: select_user(u),
                        bg=design.BUTTON_FILL_COLOR_TK, fg=design.BUTTON_TEXT_COLOR_TK, font=('Arial', 12))
        btn.pack(pady=5)

    root.mainloop()
    return selected_user

def select_monster():
    monsters = get_all_monsters()

    root = tk.Tk()
    root.title("Выбор монстра")
    root.configure(bg=design.TK_COLOR_MENU_BG)

    label = tk.Label(root, text="Выберите монстра:",
                     bg=design.TK_COLOR_MENU_BG, fg=design.TK_COLOR_MENU_TEXT)
    label.pack(pady=10)

    selected_monster = None

    def select_monster_action(monster):
        nonlocal selected_monster
        selected_monster = monster
        root.destroy()

    for monster in monsters:
        btn = tk.Button(root, text=monster.name, command=lambda m=monster: select_monster_action(m),
                        bg=design.BUTTON_FILL_COLOR_TK, fg=design.BUTTON_TEXT_COLOR_TK, font=('Arial', 12))
        btn.pack(pady=5)

    root.mainloop()
    return selected_monster

def main_menu():
    global WINDOW_WIDTH, WINDOW_HEIGHT  # Чтобы обновлять глобальные переменные при изменении размера окна

    running = True
    clock = pygame.time.Clock()

    # Определение начальных размеров окна
    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

    # Создаём окно в режиме RESIZABLE
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Undertale Battle Game")

    # Определение прямоугольников кнопок
    def get_button_rects(width, height):
        return {
            "Play": pygame.Rect(width // 2 - 100, 300, 200, 60),
            "API": pygame.Rect(width // 2 - 100, 400, 200, 60),
            "Settings": pygame.Rect(width // 2 - 100, 500, 200, 60)
        }

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                # Обновляем размеры окна
                WINDOW_WIDTH, WINDOW_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                buttons = get_button_rects(WINDOW_WIDTH, WINDOW_HEIGHT)
                if buttons["Play"].collidepoint(event.pos):
                    user = select_account()
                    if not user:
                        continue  # Если пользователь не выбрал аккаунт, возвращаемся в меню

                    monster = select_monster()
                    if not monster:
                        continue  # Если монстр не выбран, возвращаемся в меню

                    # Запускаем бой
                    start_battle(screen, user, monster)
                elif buttons["API"].collidepoint(event.pos):
                    api_menu()  # Открытие меню API
                elif buttons["Settings"].collidepoint(event.pos):
                    settings_menu()  # Открытие меню настроек

        # Отрисовка главного меню
        screen.fill(design.COLOR_MENU_BG)  # Используем цвет из design

        # Отрисовка заголовка
        title_font = design.FONT_MENU
        title_text = title_font.render("Undertale Battle Game", True, design.COLOR_MENU_TEXT)
        screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 150))

        # Получаем текущие размеры окна
        buttons = get_button_rects(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Отрисовка кнопок
        font = design.FONT_MENU

        # Кнопка "Play"
        pygame.draw.rect(screen, design.BUTTON_BORDER_COLOR_PYGAME, buttons["Play"], 2)  # Обводка
        pygame.draw.rect(screen, design.BUTTON_FILL_COLOR_PYGAME, buttons["Play"].inflate(-4, -4))  # Заполнение
        play_text = font.render("Play", True, design.BUTTON_TEXT_COLOR_PYGAME)
        play_text_rect = play_text.get_rect(center=buttons["Play"].center)
        screen.blit(play_text, play_text_rect)

        # Кнопка "API"
        pygame.draw.rect(screen, design.BUTTON_BORDER_COLOR_PYGAME, buttons["API"], 2)
        pygame.draw.rect(screen, design.BUTTON_FILL_COLOR_PYGAME, buttons["API"].inflate(-4, -4))
        api_text = font.render("API", True, design.BUTTON_TEXT_COLOR_PYGAME)
        api_text_rect = api_text.get_rect(center=buttons["API"].center)
        screen.blit(api_text, api_text_rect)

        # Кнопка "Settings"
        pygame.draw.rect(screen, design.BUTTON_BORDER_COLOR_PYGAME, buttons["Settings"], 2)
        pygame.draw.rect(screen, design.BUTTON_FILL_COLOR_PYGAME, buttons["Settings"].inflate(-4, -4))
        settings_text = font.render("Settings", True, design.BUTTON_TEXT_COLOR_PYGAME)
        settings_text_rect = settings_text.get_rect(center=buttons["Settings"].center)
        screen.blit(settings_text, settings_text_rect)

        pygame.display.flip()
        clock.tick(60)

def settings_menu():
    root = tk.Tk()
    root.title("Настройки")
    root.configure(bg=design.TK_COLOR_MENU_BG)

    label = tk.Label(root, text="Выберите цветовую схему:",
                     bg=design.TK_COLOR_MENU_BG, fg=design.TK_COLOR_MENU_TEXT)
    label.pack(pady=10)

    schemes = list(design.color_schemes.keys())
    current_scheme = design.current_scheme  # Эта переменная сейчас не используется, но может быть полезна в будущем

    def apply_scheme(scheme_name):
        design.set_color_scheme(scheme_name)
        root.destroy()

    for scheme in schemes:
        btn = tk.Button(root, text=scheme, command=lambda s=scheme: apply_scheme(s),
                        bg=design.BUTTON_FILL_COLOR_TK, fg=design.BUTTON_TEXT_COLOR_TK, font=('Arial', 12))
        btn.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main_menu()
