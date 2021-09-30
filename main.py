import pygame
import sys
from logics import *


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
MARGIN = 15
WIDTH = BLOCKS * SIZE_BLOCK + (BLOCKS + 1) * MARGIN
HEIGHT = WIDTH + 140
TITLE_REC = pygame.Rect(0, 0, WIDTH, 140)
SCORE = 0

mas[1][2] = 2
mas[3][0] = 4
print(get_empty_list(mas))
pretty_print(mas)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')
my_icon = pygame.image.load('images\\title.png')
pygame.display.set_icon(my_icon)
background_music = pygame.mixer.Sound('sounds\\Daft_Punk_Solar_Sailer.wav')
background_music.play(loops=-1)
sound_effect = pygame.mixer.Sound('sounds\\my_new_sound.wav')


draw_interface(SCORE)
pygame.display.update()
while is_zero_in_mas(mas) or can_move(mas):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        elif event.type == pygame.KEYDOWN:
            delta = 0
            if event.key == pygame.K_LEFT:
                mas, delta = move_left(mas)
                sound_effect.play()
            elif event.key == pygame.K_RIGHT:
                mas, delta = move_right(mas)
                sound_effect.play()
            elif event.key == pygame.K_UP:
                mas, delta = move_up(mas)
                sound_effect.play()
            elif event.key == pygame.K_DOWN:
                mas, delta = move_down(mas)
                sound_effect.play()
            SCORE += delta
            empty = get_empty_list(mas)
            random.shuffle(empty)
            random_num = empty.pop()
            x, y = get_index_from_number(random_num)
            mas = insert_2_or_4(mas, x, y)
            print(f'Заполнен элемент под номером: {random_num}')
            draw_interface(SCORE, delta)
            pygame.display.update()
