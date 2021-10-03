import pygame
import sys
import json
import os
import time
from logics import *
from database import *

COLOR_TEXT = (255, 128, 0)
COLORS = {
    0: (128, 128, 128),
    2: (255, 255, 255),
    4: (255, 255, 128),
    8: (255, 255, 0),
    16: (255, 128, 255),
    32: (255, 128, 128),
    64: (255, 128, 0),
    128: (255, 0, 128),
    256: (255, 0, 0),
    512: (128, 255, 255),
    1024: (128, 255, 128),
    2048: (128, 255, 0),
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DRP = (79, 39, 58)
BLOCKS = 4
SIZE_BLOCK = 140
MARGIN = 10
WIDTH = BLOCKS * SIZE_BLOCK + (BLOCKS + 1) * MARGIN
HEIGHT = WIDTH + 140
TITLE_REC = pygame.Rect(0, 0, WIDTH, 140)
BEST_USERS = get_best()


def init_const():
    global mas, score
    mas = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    empty = get_empty_list(mas)
    random.shuffle(empty)
    random_num_1 = empty.pop()
    random_num_2 = empty.pop()
    x1, y1 = get_index_from_number(random_num_1)
    x2, y2 = get_index_from_number(random_num_2)
    mas = insert_2_or_4(mas, x1, y1)
    mas = insert_2_or_4(mas, x2, y2)
    score = 0


mas = None
score = None
USER_NAME = None
path = os.getcwd()
if 'data.txt' in os.listdir(path):
    with open('data.txt') as my_file:
        data = json.load(my_file)
        mas = data['mas']
        score = data['score']
        USER_NAME = data['user']
    full_path = os.path.join(path, 'data.txt')
    os.remove(full_path)
else:
    init_const()


def draw_top_users():
    font_result = pygame.font.SysFont('arial black', 28)
    font_user = pygame.font.SysFont('arial black', 22)
    text_header = font_result.render('Best scores: ', True, COLOR_TEXT)
    screen.blit(text_header, (350, 5))
    for index, user in enumerate(BEST_USERS):
        user_name, user_score = user
        s = f"{index + 1}. {user_name}: {user_score}"
        text_user = font_user.render(s, True, COLOR_TEXT)
        screen.blit(text_user, (350, 40 + 30 * index))
        print(index, user_name, user_score)


def draw_interface(score, delta=0):
    pygame.draw.rect(screen, WHITE, TITLE_REC)
    font = pygame.font.SysFont('arial black', 50)
    font_score = pygame.font.SysFont('arial black', 36)
    font_delta = pygame.font.SysFont('arial black', 24)
    text_score = font_score.render('Score: ', True, COLOR_TEXT)
    text_score_value = font_score.render(f'{score}', True, COLOR_TEXT)
    screen.blit(text_score, (20, 25))
    screen.blit(text_score_value, (200, 25))
    if delta != 0:
        text_delta = font_delta.render(f'+{delta}', True, COLOR_TEXT)
        screen.blit(text_delta, (200, 65))
    pretty_print(mas)
    draw_top_users()
    for row in range(BLOCKS):
        for column in range(BLOCKS):
            value = mas[row][column]
            text = font.render(f'{value}', True, BLACK)
            w = column * SIZE_BLOCK + (column + 1) * MARGIN
            h = row * SIZE_BLOCK + (row + 1) * MARGIN + SIZE_BLOCK
            pygame.draw.rect(screen, COLORS[value], (w, h, SIZE_BLOCK, SIZE_BLOCK))
            if value != 0:
                font_w, font_h = text.get_size()
                text_x = w + (SIZE_BLOCK - font_w) / 2
                text_y = h + (SIZE_BLOCK - font_h) / 2
                screen.blit(text, (text_x, text_y))


print(get_empty_list(mas))
pretty_print(mas)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')
my_icon = pygame.image.load('images\\title.png')
pygame.display.set_icon(my_icon)
background_music = pygame.mixer.Sound('sounds\\Frozen_in_Time.mp3')
background_music.stop()
sound_effect_1 = pygame.mixer.Sound('sounds\\Enter.mp3')
sound_effect_2 = pygame.mixer.Sound('sounds\\Backspace.mp3')
sound_new_record = pygame.mixer.Sound('sounds\\arcade_bonus.wav')
sound_game_over = pygame.mixer.Sound('sounds\\game_over.wav')


def draw_intro():
    my_image = pygame.image.load('images\\wallpaper.jpg')
    my_font = pygame.font.SysFont('arial black', 60)
    my_second_font = pygame.font.SysFont('arial black', 24)
    text_welcome = my_font.render('Welcome, User!', True, COLOR_TEXT)
    text_M = my_second_font.render(f'M - restart music', True, COLOR_TEXT)
    text_N = my_second_font.render(f'N - stop music', True, COLOR_TEXT)
    text_Q = my_second_font.render(f'Q - quit game', True, COLOR_TEXT)
    name = 'Enter name:'
    is_find_name = False

    while not is_find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() or event.unicode.isdigit():
                    if name == 'Enter name:':
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_SPACE:
                    name += event.unicode
                elif event.key == pygame.K_RETURN:
                    if len(name) > 2:
                        global USER_NAME
                        USER_NAME = name
                        is_find_name = True
                        break
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit(0)

        screen.fill(BLACK)
        text_name = my_font.render(name, True, COLOR_TEXT)
        rect_name = text_name.get_rect()
        rect_name.center = screen.get_rect().center

        screen.blit(pygame.transform.scale(my_image, [1920, 1080]), [0, -300])
        screen.blit(text_welcome, (50, 250))
        screen.blit(text_name, rect_name)
        screen.blit(text_M, (200, 565))
        screen.blit(text_N, (220, 600))
        screen.blit(text_Q, (225, 635))
        pygame.display.update()
    screen.fill(BLACK)


def draw_game_over():
    global USER_NAME, mas, score, BEST_USERS
    my_image = pygame.image.load('images\\wallpaper.jpg')
    my_font = pygame.font.SysFont('arial black', 60)
    my_second_font = pygame.font.SysFont('arial black', 24)
    text_game_over = my_font.render('Game over!', True, COLOR_TEXT)
    text_score = my_font.render(f'Your score: {score}', True, COLOR_TEXT)
    text_SPACE = my_second_font.render(f'SPACE - restart game', True, COLOR_TEXT)
    text_RETURN = my_second_font.render(f'RETURN - new game', True, COLOR_TEXT)
    text_Q = my_second_font.render(f'Q - quit game', True, COLOR_TEXT)
    best_score = BEST_USERS[0][1]
    if score > best_score:
        text = "New Record!!!"
        background_music.stop()
        sound_new_record.play()
    else:
        text = f"Record: {best_score}"
        background_music.stop()
        sound_game_over.play()
    text_record = my_font.render(text, True, COLOR_TEXT)
    insert_result(USER_NAME, score)
    BEST_USERS = get_best()
    make_decision = False
    while not make_decision:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # restart game with old name
                    if event.key == pygame.K_n:
                        background_music.stop()
                    elif event.key == pygame.K_m:
                        background_music.play(loops=-1)
                    make_decision = True
                    init_const()
                elif event.key == pygame.K_RETURN:
                    # start with new name
                    if event.key == pygame.K_n:
                        background_music.stop()
                    elif event.key == pygame.K_m:
                        background_music.play(loops=-1)
                    make_decision = True
                    USER_NAME = None
                    init_const()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit(0)
        screen.fill(BLACK)
        screen.blit(pygame.transform.scale(my_image, [1920, 1080]), [0, -300])
        screen.blit(text_game_over, (120, 200))
        screen.blit(text_score, (30, 280))
        screen.blit(text_record, (90, 360))
        screen.blit(text_SPACE, (170, 565))
        screen.blit(text_RETURN, (180, 600))
        screen.blit(text_Q, (230, 635))
        pygame.display.update()
        screen.fill(BLACK)


def save_game():
    data = {
        'user': USER_NAME,
        'score': score,
        'mas': mas
    }
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)


def game_loop():
    global score, mas
    draw_interface(score)
    pygame.display.update()
    is_mas_move = False
    while is_zero_in_mas(mas) or can_move(mas):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game()
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                delta = 0
                if event.key == pygame.K_LEFT:
                    mas, delta, is_mas_move = move_left(mas)
                    if is_mas_move == True:
                        sound_effect_1.play()
                    else:
                        sound_effect_2.play()
                elif event.key == pygame.K_RIGHT:
                    mas, delta, is_mas_move = move_right(mas)
                    if is_mas_move == True:
                        sound_effect_1.play()
                    else:
                        sound_effect_2.play()
                elif event.key == pygame.K_UP:
                    mas, delta, is_mas_move = move_up(mas)
                    if is_mas_move == True:
                        sound_effect_1.play()
                    else:
                        sound_effect_2.play()
                elif event.key == pygame.K_DOWN:
                    mas, delta, is_mas_move = move_down(mas)
                    if is_mas_move == True:
                        sound_effect_1.play()
                    else:
                        sound_effect_2.play()
                elif event.key == pygame.K_n:
                    background_music.stop()
                elif event.key == pygame.K_m:
                    background_music.play(loops=-1)
                elif event.key == pygame.K_q:
                    save_game()
                    pygame.quit()
                    sys.exit(0)
                score += delta
                if is_zero_in_mas(mas) and is_mas_move:
                    empty = get_empty_list(mas)
                    random.shuffle(empty)
                    random_num = empty.pop()
                    x, y = get_index_from_number(random_num)
                    mas = insert_2_or_4(mas, x, y)
                    is_mas_move = False
                draw_interface(score, delta)
                pygame.display.update()


while True:
    if USER_NAME is None:
        draw_intro()
    time.sleep(0.8)
    game_loop()
    time.sleep(1)
    draw_game_over()
