#---------------------------Modules-------------------
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
from time import sleep, localtime
from pygame.locals import *
from random import randrange

def init():
    global screen
    global bg, lite, color1, color2, color3
    global bests_file_name, image_file_name
    
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Snake")
    pygame.mouse.set_visible(0)
    
    #-----------------------------colors-------------------
    bg = (0,0,0)          # BLACK - background
    lite = (255,255,255)  # WHITE - spcially use for borders
    color1 = (120,0,0)    # RED
    color2 = (0,120,120)  # BLUE
    color3 = (120,120,0)  # YELLOW
    
    bests_file_name = "data/snake-bests.txt"
    image_file_name = "data/me.png"
    
def change_color(color, rgb):
    global color1, color2
    if color == "color1":  color1 = rgb
    if color == "color2":  color2 = rgb

def text(txt, size, color, coor, font_name = ""):
    global screen, bg, lite, color1, color2
    color = {"bg": bg, "lite": lite, "color1": color1, "color2": color2}[color] if type(color) == str else color
    
    font = pygame.font.SysFont(font_name, size)
    label = font.render(txt, 1, color)
    screen.blit(label, coor)

def rect(color, coor):
    global screen, bg, lite, color1, color2
    color = {"bg": bg, "lite": lite, "color1": color1, "color2": color2}[color] if type(color) == str else color
    
    pygame.draw.rect(screen, color, coor)

def polygon(color, coor):
    global screen, bg, lite, color1, color2
    color = {"bg": bg, "lite": lite, "color1": color1, "color2": color2}[color] if type(color) == str else color
    
    pygame.draw.polygon(screen, color, coor)

def scr():
    rect("bg", (0,0,1920,1080))
    
    for border in ((55,55,5,970), (55,55,1810,5), (1860,55,5,970), (55,1020,1810,5)):
        rect("lite", border)

def start_page():
    scr()

    cell_size = 56
    cells = [(242, 522), (302, 522), (362, 522), (422, 522), (422, 462),
             (422, 402), (362, 402), (302, 402), (242, 402), (242, 342),
             (242, 282), (302, 282), (362, 282), (422, 282), (542, 522),
             (542, 462), (542, 402), (542, 342), (542, 282), (602, 342),
             (632, 402), (662, 462), (722, 522), (722, 462), (722, 402),
             (722, 342), (722, 282), (842, 522), (842, 462), (842, 402),
             [(842, 342), (902, 402)], [(842, 282), (962, 402)], (902, 282),
             (962, 282), (1022, 282), (1022, 342), (1022, 402), (1022, 462),
             (1022, 522), (1142, 522), (1142, 462), (1142, 402),
             [(1142, 342), (1202, 402)], [(1142, 282), (1262, 342), (1262, 462)],
             [(1322, 282), (1322, 522)], (1442, 522), [(1442, 462), (1502, 522)],
             [(1442, 402), (1562, 522)], [(1442, 342), (1622, 522), (1502, 402)],
             [(1442, 282), (1562, 402)], [(1502, 282), (1622, 402)],
             (1562, 282), (1622, 282)]

    for cell in cells:
        cell = [cell] if type(cell) == tuple else cell
        for pixel in cell:
            rect("color1", (pixel[0], pixel[1], cell_size, cell_size))
        pygame.display.flip()
        sleep(0.07)
    sleep(0.5)

    text('Github.com/Ar-Ekt', 100, "color2", (652, 747))
    pygame.display.flip()
    sleep(3)

def show_me():
    global image_file_name
    me_img = pygame.image.load(image_file_name)
    rect("bg", (950,90,850,930))
    screen.blit(me_img, (950,140))

def show_menu(mode):
    modes = ["PLAY", "BEST", "SETTING", "EXIT"]
    
    for index in range(4):
        color = "color2" if index == mode else "color1"
        coor = (350, 215 + 200 * index)
        text(modes[index], 100, color, coor)

def show_dots(number_of_dots, range_x, range_y, ignore_coors):
    dot_counter = 0
    while dot_counter <= number_of_dots:
        dot_x = randrange(*range_x)
        dot_y = randrange(*range_y)
        
        flag_continue = False
        for coor in ignore_coors:
            if dot_y*30 in range(coor[0][0], coor[0][1]+1) and dot_x*30 in range(coor[1][0], coor[1][1]+1):
                flag_continue = True
                break
        if flag_continue:
            continue
        
        dot_color = "color1" if dot_counter % 2 else "color2"
        rect(dot_color, (dot_x*30,dot_y*30,30,30))
        dot_counter += 1

def stop():
    select = 1
    while True:
        rect("bg", (816,513,291,142))
        
        text("STOP", 150, "color1", (821, 515))
        
        text("MENU", 50, ["color2", "color1"][select], (990, 615))
        
        text("RESUME", 50, ["color1", "color2"][select], (821, 615))
        
        pygame.display.flip()
                
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return 1
                
                elif evento.key == pygame.K_KP_ENTER or evento.key == pygame.K_RETURN:
                    return select
                
                elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_LEFT:
                    select = 1 - select

def add_snake_end(snake, motion, die_in_wall, screen_size):
    new_cell = list(snake[-1])
    if (len(snake) == 1 and motion == "up") or (len(snake) != 1 and snake[-1][0] == snake[-2][0] and snake[-1][1] - snake[-2][1] == 1):
        new_cell[1] = new_cell[1] + 1 if new_cell[1] != screen_size[1] - 1 or die_in_wall else 0
    
    elif (len(snake) == 1 and motion == "down") or (len(snake) != 1 and snake[-1][0] == snake[-2][0] and snake[-1][1] - snake[-2][1] == -1):
        new_cell[1] = new_cell[1] - 1 if new_cell[1] != 0 or die_in_wall else screen_size[1] - 1
    
    elif (len(snake) == 1 and motion == "left") or (len(snake) != 1 and snake[-1][1] == snake[-2][1] and snake[-1][0] - snake[-2][0] == 1):
        new_cell[0] = new_cell[0] + 1 if new_cell[0] != screen_size[0] - 1 or die_in_wall else 0
    
    elif (len(snake) == 1 and motion == "right") or (len(snake) != 1 and snake[-1][1] == snake[-2][1] and snake[-1][0] - snake[-2][0] == -1):
        new_cell[0] = new_cell[0] - 1 if new_cell[0] != 0 or die_in_wall else screen_size[0] - 1
    
    snake.append(tuple(new_cell))

def new_coin(range_x, range_y, snakes):
    while True:
        coin_x = randrange(range_x[0], range_x[1])
        coin_y = randrange(range_y[0], range_y[1])
        if all([(coin_x,coin_y) not in snake for snake in snakes]):
            return (coin_x, coin_y)

def eat_coin(snake, motion, die_in_wall, screen_size, wall_movement = 0, snake2 = [], two_coins = False, motion2 = "", both_add = False):
    add_snake_end(snake, motion, die_in_wall, screen_size)
    if both_add:
        add_snake_end(snake2, motion2, die_in_wall, screen_size)
    
    if not two_coins:
        coin = new_coin((0,screen_size[0]), (0,screen_size[1]), [snake, snake2])
        return coin
    else:
        coin1 = new_coin((0,screen_size[0]+wall_movement), (0,screen_size[1]), [snake])
        coin2 = new_coin((wall_movement,screen_size[0]), (0,screen_size[1]), [snake2])
        return [coin1, coin2]

def shift_snake(snake): # shift the snake towards its head
    for index in range(len(snake)-1,0,-1):
        snake[index] = snake[index-1]

def move_head(snake, motion, die_in_wall, screen_size): # move the snake's head
    head = list(snake[0])
    if motion == "up":
        head[1] = head[1] - 1 if head[1] != 0 or die_in_wall else screen_size[1] - 1
    elif motion == "down":
        head[1] = head[1] + 1 if head[1] != screen_size[1] - 1 or die_in_wall else 0
    elif motion == "right":
        head[0] = head[0] + 1 if head[0] != screen_size[0] - 1 or die_in_wall else 0
    elif motion == "left":
        head[0] = head[0] - 1 if head[0] != 0 or die_in_wall else screen_size[0] - 1
    snake[0] = tuple(head)

def move_snake(snake, motion, die_in_wall, screen_size):
    shift_snake(snake)
    move_head(snake, motion, die_in_wall, screen_size)
