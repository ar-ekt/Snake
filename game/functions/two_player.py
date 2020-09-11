from globals_ import *

arrow_keys = {pygame.K_w: ["up", 0], pygame.K_UP: ["up", 1],
              pygame.K_s: ["down", 0], pygame.K_DOWN: ["down", 1],
              pygame.K_d: ["right", 0], pygame.K_RIGHT: ["right", 1],
              pygame.K_a: ["left", 0], pygame.K_LEFT: ["left", 1]}

directs = {"up": "down", "down": "up", "right": "left", "left": "right"}

alphasize = {'a': 16, 'b': 20, 'c': 16, 'd': 17, 'e': 19, 'f': 13, 'g': 17, 'h': 18, 'i': 9,
             'j': 8,'k': 18, 'l': 10, 'm': 25, 'n': 18, 'o': 18, 'p': 18, 'q': 17, 'r': 14,
             's': 15, 't': 10,'u': 20, 'v': 21, 'w': 21, 'x': 18, 'y': 21, 'z': 17, '0': 16,
             '1': 12, '2': 18, '3': 17, '4': 15, '5': 17, '6': 15, '7': 15, '8': 15, '9': 17}

def input_name(which, color_p):
    name = ""
    cursor = 0
    loop = True
    while loop:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.type == pygame.QUIT or ( evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE ):
                    return 0
                
                elif which == 1 and evento.key == pygame.K_TAB and len(name) != 0:
                    loop = False
                    cursor = 50
                
                elif which == 2 and evento.key in [pygame.K_KP_ENTER, pygame.K_RETURN] and len(name) != 0:
                    loop = False
                    cursor = 50
                
                elif evento.key == pygame.K_BACKSPACE and len(name) != 0:
                    name = name[:-1]
                
                elif ("0" <= evento.unicode <= "9" or "a" <= evento.unicode.lower() <= "z") and len(name) <= 10:
                    name += evento.unicode.lower()
            
        clean_coor = (337,586,458,40) if which == 1 else (1114,586,458,40)
        rect("bg", clean_coor)
        
        str_name = "Name: %s%s" % (name, "|" if 0 <= cursor % 100 <= 49 else "")
        name_coor = (338, 587) if which == 1 else (1115, 587)
        text(str_name, 50, color_p, name_coor)
        
        pygame.display.flip()
        cursor += 1
        
    return name

def is_ready_2player(color_p):
    ready = [False, False]
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return 0
                
                if evento.key == pygame.K_TAB:
                    ready[0] = not ready[0]
                
                if evento.key == pygame.K_KP_ENTER or evento.key == pygame.K_RETURN:
                    ready[1] = not ready[1]
        
        rect("bg",(336,633,366,38))
        tab_str = "Ready" if ready[0] else "Press Tab to continue"
        text(tab_str, 50, color_p[0], (338, 633))
        
        rect("bg",(1190,633,394,38))
        enter_str = "Ready" if ready[1] else "Press Enter to continue"
        text(enter_str, 50, color_p[1], (1192, 633))
        
        pygame.display.flip()
        if all(ready):
            sleep(0.5)
            return 1

def show_start_round_2player(scores, names, color_p, round_num, round_winner):
    alphasize = {'a': 16, 'b': 20, 'c': 16, 'd': 17, 'e': 19, 'f': 13, 'g': 17, 'h': 18, 'i': 9,
             'j': 8,'k': 18, 'l': 10, 'm': 25, 'n': 18, 'o': 18, 'p': 18, 'q': 17, 'r': 14,
             's': 15, 't': 10,'u': 20, 'v': 21, 'w': 21, 'x': 18, 'y': 21, 'z': 17, '0': 16,
             '1': 12, '2': 18, '3': 17, '4': 15, '5': 17, '6': 15, '7': 15, '8': 15, '9': 17}
    
    scr()
    
    ignore_coors = [[(600, 690), (300, 840)], [(600, 690), (1080, 1620)], [(480, 630), (720, 1140)]]
    show_dots(120, (2,62), (2,34), ignore_coors)
    
    for index in range(2):
        name_str = "%s : %d" % (names[index], scores[index])
        name_width = 70 if not index else 1827-sum([alphasize[letter] for letter in name_str.replace(" : ","")])
        text(name_str, 40, color_p[index], (name_width, 15))
    
    text("Round %d" % round_num, 150, "color1", (740, 501))
    
    if round_winner == 2:
        text("Tie", 40, "color1", (926, 595))
    elif round_winner in [0, 1]:
        round_winner_str = "%s wins round %d" % (names[round_winner], round_num-1)
        text(round_winner_str, 40, color_p[round_winner], (820, 595))
    
    pygame.display.flip()

def game_start_2player(color_p):
    scr()
    
    ignore_coors = [[(450, 720), (300, 840)], [(450, 720), (1080, 1620)]]
    show_dots(120, (2,62), (2,34), ignore_coors)
    
    text("PLAYER1", 150, color_p[0], (332, 500))
    
    text("PLAYER2", 150, color_p[1], (1110, 500))
    
    text("Name: ", 50, color_p[1], (1115, 587))
    
    name1 = input_name(1, color_p[0])
    if not name1:
        return 0
    
    name2 = input_name(2, color_p[1])
    if not name2:
        return 0
        
    ready = [False, False]
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return 0
                
                elif evento.key == pygame.K_TAB:
                    ready[0] = not ready[0]
                
                elif evento.key in [pygame.K_KP_ENTER, pygame.K_RETURN]:
                    ready[1] = not ready[1]
        
        rect("bg", (336,633,394,38))
        tab_str = "Ready" if ready[0] else "Press Enter to continue"
        text(tab_str, 50, color_p[0], (338, 633))
        
        rect("bg", (1113,633,394,38))
        enter_str = "Ready" if ready[1] else "Press Enter to continue"
        text(enter_str, 50, color_p[1], (1115, 633))
        
        pygame.display.flip()
        
        if all(ready):
            sleep(0.5)
            return name1, name2

def game_over_2player(snakes, names, color_p, winner, write_in_file = True):
    loser = 1 - winner
    
    if write_in_file:
        bests = open(bests_file_name, "a")
        line_add = "%s %d %s %d\n" % (names[winner], len(snakes[winner])-1, names[loser], len(snakes[loser])-1)
        bests.write(line_add)
        bests.close()
    
    scr()
    
    sleep(0.5)
    
    if winner == 2:
        text("TIE", 150, "color1", (870, 501))
    else:
        win_str = "PLAYER %d WINS" % (winner + 1)
        text(win_str, 150, color_p[winner], (590, 501))
        text(names[winner], 70, color_p[winner], (590, 590))
    pygame.display.flip()
    
    sleep(0.5)
    
    rect("bg", (684,686,556,42))
    text("Press Enter to continue", 70, "color1", (687, 688))
    pygame.display.flip()
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN and evento.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                return 0

def number_of_rounds():
    gray = (180,180,180)
    
    scr()
    
    show_dots(120, (2,62), (2,34), [[(420, 690), (450, 1410)]])
    
    text("Number of rounds to win", 80, gray, (620, 500))
    
    mode = -1
    rounds = 3
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return 0
                
                elif evento.key == pygame.K_KP_ENTER or evento.key == pygame.K_RETURN:
                    return rounds
                
                elif evento.key == pygame.K_UP and rounds < 9:
                    rounds += 1
                    mode = 0
                
                elif evento.key == pygame.K_DOWN and rounds > 1:
                    rounds -= 1
                    mode = 1
                
        rect(gray, (900,565,70,74));
        text("%d" % rounds, 80, "color1", (920, 578))
        
        color = "color2" if mode == 0 else "color1"
        polygon(color, ((1000,565),(1020,597),(980,597)))
        
        color = "color2" if mode == 1 else "color1"
        polygon(color, ((1000,639),(1020,607),(980,607)))
        
        pygame.display.flip()

def select_game_color():
    arrow_keys = {pygame.K_w: ["up", 0],    pygame.K_UP:    ["up", 1],
                  pygame.K_s: ["down", 0],  pygame.K_DOWN:  ["down", 1],
                  pygame.K_d: ["right", 0], pygame.K_RIGHT: ["right", 1],
                  pygame.K_a: ["left", 0],  pygame.K_LEFT:  ["left", 1]}
    
    direct_plus = {"up": [0, -1], "down": [0, +1], "left": [-1, 0], "right": [+1, 0]}
    
    corners = [{(115, 510): "right", (475, 90): "left", (115, 90): "down", (475, 930): "left", (115, 930): "up", (475, 510): ["up", "down"]},
               {(1745, 510): "left", (1385, 930): "right", (1745, 930): "up", (1385, 90): "right", (1745, 90): "down", (1385, 510): ["down", "up"]}]
    
    # Coordinate and RGB of colors can be selected
    colors = {(3, 0): (90,0,40),   (2, 1): (90,0,90),   (3, 1): (60,0,120), (4, 1): (120,0,200), (1, 2): (150,0,90),
              (2, 2): (250,0,150), (3, 2): (0,0,100),   (4, 2): (0,30,140), (5, 2): (0,70,70),   (0, 3): (0,70,250),
              (1, 3): (0,140,140), (2, 3): (0,240,240), (3, 3): (0,60,0),   (4, 3): (0,80,50),   (5, 3): (0,150,30),
              (6, 3): (0,200,0),   (1, 4): (0,250,70),  (2, 4): (70,110,0), (3, 4): (150,170,0), (4, 4): (150,250,0),
              (5, 4): (230,250,0), (2, 5): (150,40,0),  (3, 5): (140,60,0), (4, 5): (200,100,0), (3, 6): (250,150,0)}
    
    sides = [{"snake": [(115,690), (115,750), (115,810), (115,870), (115,930)],
              "select": [False, [2,3]], "direct": "up", "end": []},
             
             {"snake": [(1745,330), (1745,270), (1745,210), (1745,150), (1745,90)],
              "select": [False, [4,3]], "direct": "down", "end": []}]
    
    which8 = False
    get_in = True
    while True:
        scr()
        
        rect("bg", (570,150,780,780))
        
        for index in range(2):
            select_width = 580 + 110 * sides[index]["select"][1][0]
            select_height = 160 + 110 * sides[index]["select"][1][1]
            rect("color%d" % (index+1), (select_width,select_height,100,100))
            rect("bg", (select_width+5,select_height+5,90,90))
        
        for coor in colors:
            rect(colors[coor], (590+110*coor[0],170+110*coor[1],80,80))
        
        for index in range(2):
            if sides[index]["select"][0]:
                rect("color%d" % (index+1), (610+110*sides[index]["select"][1][0],190+110*sides[index]["select"][1][1],40,40))
        
        if get_in:
            for index in range(11):
                sleep(0.07)
                rect(colors[tuple(sides[0]["select"][1])], (115,990-30*index,60,30))
                rect(colors[tuple(sides[1]["select"][1])], (1745,60+30*index,60,30))
                pygame.display.flip()
            rect("bg",(115,990,60,30))
            rect("bg",(1745,60,60,30))
            get_in = False
        
        else:
            sleep(0.1)
            
            for index in range(2):
                sides[index]["end"] = sides[index]["snake"][-1]
                shift_snake(sides[index]["snake"])
                head = list(sides[index]["snake"][0])
                head[0] += direct_plus[sides[index]["direct"]][0] * 60
                head[1] += direct_plus[sides[index]["direct"]][1] * 60
                head = tuple(head)
                sides[index]["snake"][0] = head
                
                if head in corners[index]:
                    if head == [(475, 510), (1385, 510)][index]:
                        sides[index]["direct"] = corners[index][head][which8]
                        if index:
                            which8 = not which8
                    else:
                        sides[index]["direct"] = corners[index][head]
                
                rect("bg", (sides[index]["end"][0],sides[index]["end"][1],60,60))
                for cell in sides[index]["snake"]:
                    color = colors[tuple(sides[index]["select"][1])]
                    rect(color, (cell[0],cell[1],60,60))
            
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if sides[1]["select"][0] and sides[0]["select"][0]:
                rect("color1", (610+110*sides[0]["select"][1][0],190+110*sides[0]["select"][1][1],40,40))
                rect("color2", (610+110*sides[1]["select"][1][0],190+110*sides[1]["select"][1][1],40,40))
                pygame.display.flip()
                sleep(0.5)
                
                color_p1 = colors[tuple(sides[0]["select"][1])]
                color_p2 = colors[tuple(sides[1]["select"][1])]
                return color_p1, color_p2
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return 0
                
                elif evento.key == pygame.K_KP_ENTER or evento.key == pygame.K_RETURN:
                    sides[1]["select"][0] = not sides[1]["select"][0]
                
                elif evento.key == pygame.K_TAB:
                    sides[0]["select"][0] = not sides[0]["select"][0]
                
                elif evento.key in arrow_keys:
                    direct, player = arrow_keys[evento.key]
                    plus = direct_plus[direct]
                    new_select = sides[player]["select"][1].copy()
                    new_select[0] += plus[0]
                    new_select[1] += plus[1]
                    if not sides[player]["select"][0] and tuple(new_select) in colors and new_select != sides[1 - player]["select"][1]:
                        sides[player]["select"][1] = new_select
