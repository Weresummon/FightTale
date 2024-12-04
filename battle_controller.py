# battle_controller.py

import pygame
import random
import math
from design import (
    FONT_GAME,
    COLOR_BATTLE_BG, COLOR_BATTLE_ACCENT, COLOR_BATTLE_TEXT,
    COLOR_HEALTH_BAR,
    COLOR_VICTORY_BG, COLOR_VICTORY_TEXT, COLOR_DEFEAT_TEXT,
    BUTTON_BORDER_COLOR, BUTTON_FILL_COLOR, BUTTON_TEXT_COLOR
)

# Константы
FIELD_WIDTH, FIELD_HEIGHT = 400, 300
FIELD_X, FIELD_Y = 200, 150
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class Monster:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.max_health = health

    def attack(self):
        # To be overridden by subclasses
        return [], []

class DummyMonster(Monster):
    def __init__(self, name="Dummy", health=100):
        super().__init__(name, health)

    def attack(self):
        bullets, beams = generate_bullets(), generate_beams()
        return bullets, beams

class GoblinMonster(Monster):
    def __init__(self, name="Goblin", health=80):
        super().__init__(name, health)

    def attack(self):
        bullets = []
        beams = generate_goblin_beams()
        return bullets, beams

def start_battle(screen, user, monster):
    if user is None:
        print("Ошибка: пользователь не выбран.")
        return

    player_name = user['name']
    player_health = user['health']
    player_max_health = user['health']
    monster_name = monster.name
    monster_health = monster.health
    monster_max_health = monster.health
    player_turn = True
    clock = pygame.time.Clock()
    turn_timer = 1000
    last_turn_time = pygame.time.get_ticks()

    soul_pos = [FIELD_X + FIELD_WIDTH // 2, FIELD_Y + FIELD_HEIGHT // 2]
    bullets = []
    beams = []

    monster_attack_count = 0  # Счётчик атак монстра

    # Переменная для неуязвимости игрока
    invulnerable_until = 0

    # Переменные для тряски
    shake_duration = 0
    shake_intensity = 0
    shake_offset = [0, 0]

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                pos = pygame.mouse.get_pos()
                # Предполагается, что кнопка "Fight" находится в определённой области
                # Настройте координаты в зависимости от позиции кнопки
                # Например, кнопка "Fight" имеет прямоугольник (50, 500, 100, 40)
                if 50 <= pos[0] <= 150 and 500 <= pos[1] <= 540:  # Кнопка "Fight"
                    # Запускаем мини-игру атаки
                    damage = attack_minigame(screen)
                    monster.health -= damage
                    monster_health = monster.health
                    print(f"Монстр получил урон {damage}, осталось {monster_health} HP!")
                    player_turn = False
                    last_turn_time = pygame.time.get_ticks()
                    monster_attack_count = 0  # Сбрасываем счётчик атак при начале хода монстра

                    # Тряска окна при получении урона монстром
                    if damage > 0:
                        shake_duration = 300  # Миллисекунды
                        shake_intensity = min(damage, 20)  # Ограничиваем интенсивность

        if not player_turn:
            if current_time - last_turn_time >= turn_timer and not bullets and not beams:
                if monster_attack_count < 3:
                    bullets, beams = monster.attack()
                    print(f"Монстр {monster.name} использует атаку!")
                    monster_attack_count += 1
                else:
                    # Ход монстра завершён, возвращаем ход игроку
                    player_turn = True
                    monster_attack_count = 0  # Сбрасываем счётчик атак
                    last_turn_time = pygame.time.get_ticks()
                    print("Ход переходит к игроку.")

            # Обработка движения души игрока
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and soul_pos[1] > FIELD_Y:
                soul_pos[1] -= 2.5
            if keys[pygame.K_DOWN] and soul_pos[1] < FIELD_Y + FIELD_HEIGHT - 20:
                soul_pos[1] += 2.5
            if keys[pygame.K_LEFT] and soul_pos[0] > FIELD_X:
                soul_pos[0] -= 2.5
            if keys[pygame.K_RIGHT] and soul_pos[0] < FIELD_X + FIELD_WIDTH - 20:
                soul_pos[0] += 2.5

        # Обновление тряски
        if shake_duration > 0:
            shake_offset[0] = random.randint(-shake_intensity, shake_intensity)
            shake_offset[1] = random.randint(-shake_intensity, shake_intensity)
            shake_duration -= clock.get_time()
            if shake_duration < 0:
                shake_duration = 0
                shake_offset = [0, 0]
        else:
            shake_offset = [0, 0]

        # Создаём временную поверхность для тряски
        temp_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        temp_surface.fill(COLOR_BATTLE_BG)

        # Рисуем UI и все элементы на временной поверхности
        draw_ui(temp_surface, monster_health, monster_max_health, player_health, player_max_health)
        player_name_text = FONT_GAME.render(f"Player: {player_name}", True, COLOR_BATTLE_TEXT)
        temp_surface.blit(player_name_text, (20, 100))

        # Отрисовка атак монстра
        if not player_turn:
            if bullets:
                player_health, shake = handle_monster_turn(temp_surface, soul_pos, bullets, player_health, current_time, invulnerable_until)
                user['health'] = player_health
                if shake:
                    shake_duration = 200
                    shake_intensity = 5
            if beams:
                player_health, beams, invulnerable_until, shake = handle_beam_attack(temp_surface, soul_pos, beams, player_health, current_time, invulnerable_until)
                user['health'] = player_health
                if shake:
                    shake_duration = 200
                    shake_intensity = 5

        # Отрисовка игрового поля и души игрока
        if player_turn:
            draw_buttons(temp_surface)
        else:
            draw_game_field(temp_surface, soul_pos, current_time, invulnerable_until)

        # Проверка конца игры
        if player_health <= 0:
            show_end_screen(screen, "Game Over")
            running = False
        elif monster_health <= 0:
            show_end_screen(screen, "You Win!")
            running = False

        # Вывод временной поверхности на экран с учетом тряски
        screen.blit(temp_surface, shake_offset)
        pygame.display.flip()
        clock.tick(60)

def draw_ui(screen, monster_health, monster_max_health, player_health, player_max_health):
    # Отрисовка полосок здоровья
    # Полоска здоровья монстра
    draw_health_bar(screen, 20, 20, 200, 20, monster_health, monster_max_health, COLOR_HEALTH_BAR, (100, 100, 100))
    # Полоска здоровья игрока
    draw_health_bar(screen, 20, 60, 200, 20, player_health, player_max_health, COLOR_HEALTH_BAR, (100, 100, 100))

    # Подписи к полоскам
    font = FONT_GAME
    monster_text = font.render("Monster HP", True, COLOR_BATTLE_TEXT)
    player_text = font.render("Player HP", True, COLOR_BATTLE_TEXT)
    screen.blit(monster_text, (230, 15))
    screen.blit(player_text, (230, 55))

def draw_health_bar(screen, x, y, width, height, current_health, max_health, bar_color, back_color):
    # Отрисовка заднего фона полоски
    pygame.draw.rect(screen, back_color, (x, y, width, height))
    # Вычисление длины заполненной части
    health_ratio = max(current_health / max_health, 0)
    fill_width = int(width * health_ratio)
    # Отрисовка заполненной части
    pygame.draw.rect(screen, bar_color, (x, y, fill_width, height))

def draw_buttons(screen):
    font = FONT_GAME
    buttons = ["Fight", "Act", "Item", "Mercy"]
    for idx, button in enumerate(buttons):
        button_rect = pygame.Rect(50 + idx * 150, 500, 100, 40)
        # Обводка кнопки
        pygame.draw.rect(screen, BUTTON_BORDER_COLOR, button_rect, 2)  # Толщина линии 2
        # Заполнение кнопки
        pygame.draw.rect(screen, BUTTON_FILL_COLOR, button_rect.inflate(-4, -4))  # Уменьшаем размер для обводки
        # Текст кнопки
        button_text = font.render(button, True, BUTTON_TEXT_COLOR)
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)

def draw_game_field(screen, soul_pos, current_time, invulnerable_until):
    # Отрисовка игрового поля
    pygame.draw.rect(screen, COLOR_BATTLE_ACCENT, (FIELD_X, FIELD_Y, FIELD_WIDTH, FIELD_HEIGHT), 2)

    # Определение цвета души
    if current_time < invulnerable_until:
        soul_color = WHITE
    else:
        soul_color = RED

    # Определяем центр сердца
    heart_center = (int(soul_pos[0] + 10), int(soul_pos[1] + 10))  # 10 - половина размера квадрата (20//2)
    heart_size = 20  # Размер сердца (будет масштабирован до 20x20)

    # Рисуем пиксельное сердце вместо квадрата
    draw_pixel_heart(screen, soul_color, heart_center, heart_size)

def draw_pixel_heart(surface, color, center, size):
    """
    Рисует пиксельное сердце на заданной поверхности.

    :param surface: Поверхность Pygame для рисования.
    :param color: Цвет сердца.
    :param center: Кортеж (x, y) для центра сердца.
    :param size: Размер сердца в пикселях (20x20).
    """
    # Матрица сердца 10x10
    heart_10x10 = [
        "0001100000",
        "0011110000",
        "0111111000",
        "1111111100",
        "1111111100",
        "0111111000",
        "0011110000",
        "0001100000",
        "0000000000",
        "0000000000"
    ]

    # Размер одного пикселя сердца (2x2)
    pixel_size = size // len(heart_10x10)  # 20 // 10 = 2

    for y, row in enumerate(heart_10x10):
        for x, pixel in enumerate(row):
            if pixel == '1':
                pygame.draw.rect(
                    surface,
                    color,
                    (center[0] + (x - 5) * pixel_size, center[1] + y * pixel_size, pixel_size, pixel_size)
                )

def handle_monster_turn(screen, soul_pos, bullets, player_hp, current_time, invulnerable_until):
    new_bullets = []
    shake = False
    for bullet in bullets:
        bullet[1] += bullet[2]
        pygame.draw.circle(screen, WHITE, (bullet[0], bullet[1]), 10)
        soul_rect = pygame.Rect(soul_pos[0], soul_pos[1], 20, 20)
        bullet_rect = pygame.Rect(bullet[0] - 10, bullet[1] - 10, 20, 20)
        if soul_rect.colliderect(bullet_rect):
            if current_time >= invulnerable_until:
                player_hp -= 5
                invulnerable_until = current_time + 500  # Неуязвимость на 0.5 секунды
                shake = True  # Тряска при получении урона
        else:
            if bullet[1] <= FIELD_Y + FIELD_HEIGHT + 10:
                new_bullets.append(bullet)
    bullets[:] = new_bullets
    return player_hp, shake

def handle_beam_attack(screen, soul_pos, beams, player_hp, current_time, invulnerable_until):
    new_beams = []
    shake = False
    for beam in beams:
        elapsed_time = current_time - beam["timer"]

        # Параметры луча
        if beam["direction"] == "horizontal":
            position = beam["position"]
            start_pos = (FIELD_X, position)
            end_pos = (FIELD_X + FIELD_WIDTH, position)
        elif beam["direction"] == "vertical":
            position = beam["position"]
            start_pos = (position, FIELD_Y)
            end_pos = (position, FIELD_Y + FIELD_HEIGHT)
        elif beam["direction"] == "diagonal":
            start_pos, end_pos = beam["beam_line"]

        # Задаём толщину луча
        beam_thickness = 8

        # Этап телеграфирования
        if beam["state"] == "telegraph":
            if elapsed_time <= 500:
                # Отрисовываем полупрозрачный луч
                overlay = pygame.Surface((FIELD_WIDTH, FIELD_HEIGHT), pygame.SRCALPHA)
                overlay.set_alpha(128)
                beam_start = (start_pos[0] - FIELD_X, start_pos[1] - FIELD_Y)
                beam_end = (end_pos[0] - FIELD_X, end_pos[1] - FIELD_Y)
                pygame.draw.line(overlay, beam["color"], beam_start, beam_end, beam_thickness)
                screen.blit(overlay, (FIELD_X, FIELD_Y))
                new_beams.append(beam)
            else:
                beam["state"] = "active"
                beam["timer"] = current_time
                new_beams.append(beam)
        # Этап активного луча
        elif beam["state"] == "active":
            if elapsed_time <= 1500:
                # Отрисовываем активный луч с указанным цветом
                pygame.draw.line(screen, beam["color"], start_pos, end_pos, beam_thickness)
                # Проверка столкновения
                soul_rect = pygame.Rect(soul_pos[0], soul_pos[1], 20, 20)
                if beam["direction"] == "horizontal":
                    beam_rect = pygame.Rect(FIELD_X, start_pos[1] - beam_thickness // 2, FIELD_WIDTH, beam_thickness)
                    if soul_rect.colliderect(beam_rect):
                        if current_time >= invulnerable_until:
                            player_hp -= 5
                            invulnerable_until = current_time + 500  # Неуязвимость на 0.5 секунды
                            shake = True
                elif beam["direction"] == "vertical":
                    beam_rect = pygame.Rect(start_pos[0] - beam_thickness // 2, FIELD_Y, beam_thickness, FIELD_HEIGHT)
                    if soul_rect.colliderect(beam_rect):
                        if current_time >= invulnerable_until:
                            player_hp -= 5
                            invulnerable_until = current_time + 500
                            shake = True
                elif beam["direction"] == "diagonal":
                    if line_collision(soul_rect, start_pos, end_pos, thickness=beam_thickness):
                        if current_time >= invulnerable_until:
                            player_hp -= 5
                            invulnerable_until = current_time + 500
                            shake = True
                new_beams.append(beam)
            else:
                # Луч завершился
                pass
    return player_hp, new_beams, invulnerable_until, shake

def generate_bullets():
    bullets = []
    # Случайный выбор паттерна атаки снарядами
    attack_type = random.choice(["random_fall", "line_fall"])
    if attack_type == "random_fall":
        for _ in range(5):
            x = random.randint(FIELD_X + 10, FIELD_X + FIELD_WIDTH - 10)
            y = FIELD_Y - 10
            speed = random.randint(3, 6)
            bullets.append([x, y, speed])
    elif attack_type == "line_fall":
        for x in range(FIELD_X + 20, FIELD_X + FIELD_WIDTH - 20, 50):
            y = FIELD_Y - 10
            speed = random.randint(3, 6)
            bullets.append([x, y, speed])
    return bullets

def generate_beams():
    beams = []
    num_beams = random.randint(2, 5)  # Генерируем от 2 до 5 лучей
    for _ in range(num_beams):
        beam_direction = random.choice(["horizontal", "vertical", "diagonal"])
        beam = {
            "direction": beam_direction,
            "state": "telegraph",
            "timer": pygame.time.get_ticks(),
            "color": RED  # Default beam color
        }
        # Устанавливаем позицию или линию луча в зависимости от направления
        if beam_direction == "horizontal":
            position = random.randint(FIELD_Y + 10, FIELD_Y + FIELD_HEIGHT - 10)
            beam["position"] = position
        elif beam_direction == "vertical":
            position = random.randint(FIELD_X + 10, FIELD_X + FIELD_WIDTH - 10)
            beam["position"] = position
        elif beam_direction == "diagonal":
            beam["beam_line"] = random.choice([
                ((FIELD_X, FIELD_Y), (FIELD_X + FIELD_WIDTH, FIELD_Y + FIELD_HEIGHT)),
                ((FIELD_X + FIELD_WIDTH, FIELD_Y), (FIELD_X, FIELD_Y + FIELD_HEIGHT))
            ])
        beams.append(beam)
    return beams

def generate_goblin_beams():
    beams = []
    beam_length = 100  # Короткие лучи

    # Левый луч: из левого верхнего угла внутрь
    start_pos_left = (FIELD_X, FIELD_Y)
    end_pos_left = (FIELD_X + beam_length, FIELD_Y + beam_length)
    beams.append({
        "direction": "diagonal",
        "state": "telegraph",
        "timer": pygame.time.get_ticks(),
        "beam_line": (start_pos_left, end_pos_left),
        "color": WHITE  # Белый цвет для Goblin
    })

    # Правый луч: из правого верхнего угла внутрь
    start_pos_right = (FIELD_X + FIELD_WIDTH, FIELD_Y)
    end_pos_right = (FIELD_X + FIELD_WIDTH - beam_length, FIELD_Y + beam_length)
    beams.append({
        "direction": "diagonal",
        "state": "telegraph",
        "timer": pygame.time.get_ticks(),
        "beam_line": (start_pos_right, end_pos_right),
        "color": WHITE  # Белый цвет для Goblin
    })

    return beams

def line_collision(rect, start_pos, end_pos, thickness=5):
    # Проверка столкновения между прямоугольником и линией заданной толщины
    # Создаём маску для линии и проверяем пересечение с маской прямоугольника
    line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    pygame.draw.line(line_surf, (255, 255, 255, 255), start_pos, end_pos, thickness)
    line_mask = pygame.mask.from_surface(line_surf)

    rect_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(rect_surf, (255, 255, 255, 255), rect)
    rect_mask = pygame.mask.from_surface(rect_surf)

    offset = (0, 0)
    collision_point = rect_mask.overlap(line_mask, offset)
    return collision_point is not None

def attack_minigame(screen):
    # Параметры мини-игры
    minigame_running = True
    clock = pygame.time.Clock()
    line_x = FIELD_X  # Начальная позиция линии по X
    line_speed = 5    # Скорость движения линии
    line_direction = 1  # Направление движения (1 - вправо)

    # Центр окна для определения урона
    center_x = FIELD_X + FIELD_WIDTH // 2

    damage = 0

    while minigame_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Останавливаем линию и рассчитываем урон
                    distance_from_center = abs(line_x - center_x)
                    max_distance = FIELD_WIDTH // 2
                    # Чем ближе к центру, тем больше урон
                    damage = max(0, int(30 * (1 - (distance_from_center / max_distance))))
                    minigame_running = False

        # Движение линии
        line_x += line_speed * line_direction
        if line_x >= FIELD_X + FIELD_WIDTH or line_x <= FIELD_X:
            line_direction *= -1  # Меняем направление движения

        # Отрисовка мини-игры
        screen.fill(COLOR_BATTLE_BG)

        # Отрисовка окна мини-игры
        pygame.draw.rect(screen, COLOR_BATTLE_ACCENT, (FIELD_X, FIELD_Y, FIELD_WIDTH, FIELD_HEIGHT), 2)

        # Отрисовка линии
        pygame.draw.line(screen, RED, (line_x, FIELD_Y), (line_x, FIELD_Y + FIELD_HEIGHT), 3)

        # Отрисовка указателя центра
        pygame.draw.line(screen, COLOR_BATTLE_TEXT, (center_x, FIELD_Y), (center_x, FIELD_Y + FIELD_HEIGHT), 1)

        pygame.display.flip()
        clock.tick(60)

    return damage

def show_end_screen(screen, message):
    if message == "You Win!":
        bg_color = COLOR_VICTORY_BG
        text_color = COLOR_VICTORY_TEXT
    else:
        bg_color = COLOR_VICTORY_BG  # Можно установить отдельный цвет для поражения
        text_color = COLOR_DEFEAT_TEXT

    screen.fill(bg_color)
    font = FONT_GAME
    end_text = font.render(message, True, text_color)
    screen.blit(end_text, ((WINDOW_WIDTH - end_text.get_width()) // 2,
                           (WINDOW_HEIGHT - end_text.get_height()) // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
