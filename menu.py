from globals_ import *
import pygame
#---------------------------Games---------------------
from game.classic import classic
from game.in_time import in_time
from game.berlin_wall import berlin_wall
from game.tron import tron
pygame.init()
#---------------------------Best----------------------
def read_bests(which): # read file and store best scores in a list
    bests = open(bests_file_name)
    best_list = bests.readlines()
    bests.close()
    
    names = []
    if which == 1:
        best_list = best_list[:best_list.index("\n")]
        for line in best_list:
            line = line[:-1].split()
            names += [(int(line[1]), line[0])]
    elif which == 2:
        best_list = best_list[best_list.index("\n")+1:]
        for line in best_list:
            line = line[:-1].split()
            names.append([int(line[1])-int(line[3]),int(line[1]),int(line[3]),line[0],line[2]])
    
    return sorted(names)[::-1]

def show_best_1player():
    names = read_bests(1)
    
    text("Name", 50, "color1", (1100, 200))
    text("Score", 50, "color1", (1400, 200))
    
    for index in range(min(10, len(names))):
        text(names[index][1], 50, "color2", (1100, 270+index*70))
        text(str(names[index][0]), 50, "color2", (1400, 270+index*70))


def show_best_2player():
    alphasize = {'a': 22, 'b': 20, 'c': 19, 'd': 23, 'e': 20, 'f': 12, 'g': 22, 'h': 21, 'i': 7,
             'j': 11,'k': 22, 'l': 9, 'm': 30, 'n': 20, 'o': 22, 'p': 20, 'q': 22, 'r': 12,
             's': 18, 't': 16,'u': 22, 'v': 18, 'w': 31, 'x': 23, 'y': 23, 'z': 20, '0': 21,
             '1': 18, '2': 21, '3': 19, '4': 22, '5': 19, '6': 19, '7': 19, '8': 22, '9': 19}
    
    names = read_bests(2)
    
    text("Name", 50, "color1", (1106, 200))
    text("Score", 50, "color1", (1251, 200))
    text("Name", 50, "color1", (1378, 200))
    
    for index in range(min(10, len(names))):
        
        name_coor = (1202-sum([alphasize[ll] for ll in names[index][3]]), 270+index*70)
        text(names[index][3], 50, "color2", name_coor)
        
        text("(", 50, "color2", (1222, 270+index*70))
        text("-", 50, "color2", (1292, 270+index*70))
        text(")", 50, "color2", (1358, 270+index*70))
        
        text(names[index][4], 50, "color2", (1378, 270+index*70))
        
        score_coor = (1266 - 12 * len(str(names[index][1])), 270+index*70)
        text("%d" % names[index][1], 50, "color2", score_coor)
        
        score_coor = (1339 - 13 * len(str(names[index][2])), 270+index*70)
        text("%d" % names[index][2], 50, "color2", score_coor)

def show_best(best_mode):
    rect("bg", (950,90,757,930))
        
    if best_mode == 0:
        show_best_1player()
    elif best_mode == 1:
        show_best_2player()
    
    rect(["color2", "color1"][best_mode], (1165,91,130,72))
    text("1P", 83, "bg", (1199, 105))
    
    rect(["color1", "color2"][best_mode], (1300,91,130,72))
    text("2P", 83, "bg", (1331, 105))
    
    pygame.display.flip()

def best(mode):
    best_mode = 0
    while True:
        show_best(best_mode)
        
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return mode
                
                elif evento.key == pygame.K_UP:
                    return mode - 1
                
                elif evento.key == pygame.K_DOWN:
                    return mode + 1
                
                elif evento.key == pygame.K_LEFT:
                    best_mode = 0
                
                elif evento.key == pygame.K_RIGHT:
                    best_mode = 1

#-------------------------Setting---------------------
def show_setting(setting_snake, color_mode, colors):
    setting_plus = [[0,-60],[60,0],[0,+60],[-60,0]]
    
    text("MODE COLOR", 65, "color1", (1090, 180))
    
    # show selector
    rect("bg", (1141,260,540,650))
    rect("color2", (1151+(110*color_mode[0])-10,270+(110*color_mode[1])-10,100,100))
    rect("bg", (1151+(110*color_mode[0])-5,270+(110*color_mode[1])-5,90,90))
    
    jj = 0
    for col1 in colors: # show available colors
        ii = 0
        for col2 in colors:
            if col1 != col2:
                rect(colors[col1], (1151+(110*ii),270+(110*jj),80,80)) # color1
                rect("bg", (1166+(110*ii),285+(110*jj),50,50))
                rect(colors[col2], (1171+(110*ii),290+(110*jj),40,40)) # color2
                ii += 1
        jj += 1
    
    if setting_snake["start"]: # show start
        rect("color1", (1713,90,60,60))
        for i in range(11):
            sleep(0.05)
            rect("color2", (993,990-(30*i),60,30))
            pygame.display.flip()
        rect("bg", (993,990,60,30))
        
        setting_snake["start"] = False
    
    else: # move and show
        sleep(0.07)
        
        # move setting-snake
        last_cell = setting_snake["coor"][-1]
        for ics in range(4,0,-1):
            setting_snake["coor"][ics] = setting_snake["coor"][ics-1]
        setting_snake["coor"][0] = (setting_snake["coor"][0][0] + setting_plus[setting_snake["line"]][0],
                                    setting_snake["coor"][0][1] + setting_plus[setting_snake["line"]][1])
        
        # change line of setting-snake
        if setting_snake["coor"][0][0] == 993 and setting_snake["line"] == 3:
            setting_snake["line"] = 0
        if setting_snake["coor"][0][1] == 90 and setting_snake["line"] == 0:
            setting_snake["line"] = 1
        if setting_snake["coor"][0][0] == 1713 and setting_snake["line"] == 1:
            setting_snake["line"] = 2
        if setting_snake["coor"][0][1] == 930 and setting_snake["line"] == 2:
            setting_snake["line"] = 3
            
        # show setting-snake
        rect("bg", (last_cell[0],last_cell[1],60,60)) # last cell
        rect("color1", (1713,90,60,60)) # apple
        for ics in setting_snake["coor"]:
            rect("color2", (ics[0],ics[1],60,60))
        
    pygame.display.flip()

def setting(mode):
    global color1, color2
    
    colors = {"PINK": (170,0,120),
          "BLUE": (0,120,120),
          "GREEN": (0,120,0),
          "YELLOW": (160,160,0),
          "ORANGE": (180,90,0),
          "RED": (120,0,0)}
    setting_snake = {"start": True,
                     "line": 0,
                     "coor": [(993,690),(993,750),(993,810),(993,870),(993,930)]}
    color_mode = [1, 5]
    
    rect("bg", (950,90,757,930))
    while True:
        show_setting(setting_snake, color_mode, colors)
        
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return mode
                
                elif evento.key == pygame.K_KP_ENTER or evento.key == pygame.K_RETURN:
                    color1 = colors[list(colors.keys())[color_mode[1]]]
                    if color_mode[0] >= color_mode[1]:
                        color2 = colors[list(colors.keys())[color_mode[0]+1]]
                    else:
                        color2 = colors[list(colors.keys())[color_mode[0]]]
                    change_color("color1", color1)
                    change_color("color2", color2)
                    scr()
                    show_menu(mode)
                    
                elif evento.key == pygame.K_UP:
                    color_mode[1] = {0:0, 1:0, 2:1, 3:2, 4:3, 5:4}[color_mode[1]]
                
                elif evento.key == pygame.K_DOWN:
                    color_mode[1] = {0:1, 1:2, 2:3, 3:4, 4:5, 5:5}[color_mode[1]]
                
                elif evento.key == pygame.K_LEFT:
                    color_mode[0] = {0:0, 1:0, 2:1, 3:2, 4:3, 5:4}[color_mode[0]]
                
                elif evento.key == pygame.K_RIGHT:
                    color_mode[0] = {0:1, 1:2, 2:3, 3:4, 4:5, 5:5}[color_mode[0]]

#----------------------------Exit---------------------
def show_exit(mode):
    rect("bg", (950,90,757,930))
    text("ARE YOU SURE TO EXIT?", 70, "color1", (1000, 433))
    text("YES", 60, ["color1", "color2"][mode], (1181, 507))
    text("NO", 60, ["color2", "color1"][mode], (1349, 507))
    pygame.display.flip()

def exit_game(mode):
    show_menu(mode)
    
    exit_mode = 0
    while True:
        show_exit(exit_mode)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                show_exit(1)
                pygame.quit()
                sys.exit(0)
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    show_exit(1)
                    pygame.quit()
                    sys.exit(0)
                
                elif evento.key == pygame.K_KP_ENTER or evento.key == pygame.K_RETURN:
                    if exit_mode:
                        pygame.quit()
                        sys.exit(0)
                    else:
                        return mode
                
                elif evento.key == pygame.K_UP:
                    return mode - 1
                
                elif evento.key == pygame.K_RIGHT:
                    exit_mode = 0
                
                elif evento.key == pygame.K_LEFT:
                    exit_mode = 1

#------------------------Select-game------------------
def show_select_game(games, number_of_games, select):
    scr()
    show_menu(0)
    
    for index in range(number_of_games):
        game = games[index]
        color = "color2" if index == select else "color1"
        text(game[1], 80, color, (1050, 240+120*index))
        text("%d PLAYER" % game[2], 40, color, (1050, 290+120*index))
    
    pygame.display.flip()
    

def select_game():
    games = [[classic, "Classic", 1],
             [in_time, "In Time", 2],
             [berlin_wall, "Berlin Wall", 2],
             [tron, "Tron", 2]]
    number_of_games = len(games)
    
    select = 0
    while True:
        show_select_game(games, number_of_games, select)
        
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return 0
                
                elif evento.key == pygame.K_KP_ENTER or evento.key == pygame.K_RETURN:
                    pygame.mixer.usic.load('nagin.mp3')
                    pygame.mixer.music.play()
                    games[select][0]()
                
                elif evento.key == pygame.K_DOWN:
                    select = select + 1 if select < number_of_games - 1 else number_of_games - 1
                
                elif evento.key == pygame.K_UP:
                    select = select - 1 if select > 0 else 0
                
                elif evento.key == pygame.K_LEFT:
                    return 0

def menu():
    
    mode = 0
    while True:
        scr()
        show_me()
        show_menu(mode)
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                mode = exit_game(3)
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    mode = exit_game(3)
                
                elif evento.key == pygame.K_KP_ENTER or evento.key == pygame.K_RETURN:
                    if mode == 0:
                        select_game()
                    
                    elif mode == 1:
                        mode = best(mode)
                    
                    elif mode == 2:
                        setting(mode)
                    
                    elif mode == 3:
                        mode = exit_game(mode)
                    
                elif evento.key == pygame.K_UP:
                    mode = mode - 1 if mode > 0 else 0
                
                elif evento.key == pygame.K_DOWN:
                    mode = mode + 1 if mode < 3 else 3
