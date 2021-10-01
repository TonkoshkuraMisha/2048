import pygame
import sys
from logics import *
from database import get_best, cursor


BEST_USERS = get_best()

def draw_top_users():
    font_result = pygame.font.SysFont('simsun', 42)
    font_user = pygame.font.SysFont('simsun', 36)
    text_header = font_result.render('Best scores: ', True, COLOR_TEXT)
    screen.blit(text_header, (400, 5))
    for index, user in enumerate(BEST_USERS):
        user_name, user_score = user
        s = f"{index+1}. {user_name}: {user_score}"
        text_user = font_user.render(s, True, COLOR_TEXT)
        screen.blit(text_user, (400, 40 + 30*index))
        print(index, user_name, user_score)


def draw_interface(SCORE, delta=0):
    pygame.draw.rect(screen, WHITE, TITLE_REC)
    font = pygame.font.SysFont('Arial Black', 50)
    font_score = pygame.font.SysFont('simsun', 70)
    font_delta = pygame.font.SysFont('simsun', 50)
    text_score = font_score.render('Score: ', True, COLOR_TEXT)
    text_score_value = font_score.render(f'{SCORE}', True, COLOR_TEXT)
    screen.blit(text_score, (20, 35))
    screen.blit(text_score_value, (250, 35))
    if delta != 0:
        text_delta = font_delta.render(f'+{delta}', True, COLOR_TEXT)
        screen.blit(text_delta, (250, 90))
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


mas = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]
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

BLOCKS = 4
SIZE_BLOCK = 140
MARGIN = 10
WIDTH = BLOCKS * SIZE_BLOCK + (BLOCKS + 1) * MARGIN
HEIGHT = WIDTH + 140
TITLE_REC = pygame.Rect(0, 0, WIDTH, 140)
SCORE = 0
USER_NAME = None

mas[1][2] = 2
mas[3][0] = 4

print(get_empty_list(mas))
pretty_print(mas)

# for user in get_best():
#   print(user)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')
my_icon = pygame.image.load('images\\title.png')
pygame.display.set_icon(my_icon)
background_music = pygame.mixer.Sound('sounds\\Daft_Punk_Solar_Sailer.wav')
background_music.play(loops=-1)
sound_effect = pygame.mixer.Sound('sounds\\button_press.wav')


def draw_intro():
    # my_image = pygame.image.load('images\\title.png')
    my_image = pygame.image.load('images\\wallpaper.jpg')
    my_font = pygame.font.SysFont('Arial Black', 60)
    text_welcome = my_font.render('Welcome, User!', True, WHITE)
    name = 'Enter name: '
    is_find_name = False

    while not is_find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() or event.unicode.isdigit():
                    if name == 'Enter name: ':
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

        screen.fill(BLACK)
        text_name = my_font.render(name, True, WHITE)
        rect_name = text_name.get_rect()
        rect_name.center = screen.get_rect().center

        screen.blit(pygame.transform.scale(my_image, [1920, 1080]), [0, -200])
        screen.blit(text_welcome, (50, 15))
        screen.blit(text_name, rect_name)
        pygame.display.update()
    screen.fill(BLACK)

def draw_game_over():
    my_image = pygame.image.load('images\\wallpaper.jpg')
    my_font = pygame.font.SysFont('Arial Black', 60)
    text_game_over = my_font.render('Game over!', True, WHITE)
    text_score = my_font.render(f'Your score:', True, WHITE)
    BEST_SCORE = BEST_USERS[0][1]

    if SCORE > BEST_SCORE:
        text = 'New Record!!!'
    elif SCORE == BEST_SCORE:
        text = f'Record: {BEST_SCORE}'
    text_record = my_font.render(text, True, WHITE)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        screen.fill(BLACK)
        screen.blit(text_game_over, (120, 260))
        screen.blit(text_score, (120, 360))
        screen.blit(text_record, (290, 460))
        screen.blit(pygame.transform.scale(my_image, [1920, 1080]), [0, -200])
        pygame.display.update()

draw_intro()




draw_interface(SCORE)
pygame.display.update()
# while is_zero_in_mas(mas) or can_move(mas):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit(0)
#
#         elif event.type == pygame.KEYDOWN:
#             delta = 0
#             if event.key == pygame.K_LEFT:
#                 mas, delta = move_left(mas)
#                 sound_effect.play()
#             elif event.key == pygame.K_RIGHT:
#                 mas, delta = move_right(mas)
#                 sound_effect.play()
#             elif event.key == pygame.K_UP:
#                 mas, delta = move_up(mas)
#                 sound_effect.play()
#             elif event.key == pygame.K_DOWN:
#                 mas, delta = move_down(mas)
#                 sound_effect.play()
#             SCORE += delta
#
#             if is_zero_in_mas(mas):
#                 empty = get_empty_list(mas)
#                 random.shuffle(empty)
#                 random_num = empty.pop()
#                 x, y = get_index_from_number(random_num)
#                 mas = insert_2_or_4(mas, x, y)
#                 print(f'Заполнен элемент под номером: {random_num}')
#             draw_interface(SCORE, delta)
#             pygame.display.update()
#     print(USER_NAME)

draw_game_over()