from game.functions.two_player import *

def show_time(game_time):
    if 1 <= game_time["extra"] <= 15:
        text("+30", 40, "lite", (983, 15))
        game_time["extra"] += 1
    
    time_str = "%d : %.2d" % (game_time["minute"], game_time["second"])
    text(time_str, 40, "color1", (900, 15))

def show(snakes, coin, names, color_p, cell_size, game_time, time1):
    alphasize = {'a': 16, 'b': 20, 'c': 16, 'd': 17, 'e': 19, 'f': 13, 'g': 17, 'h': 18, 'i': 9,
             'j': 8,'k': 18, 'l': 10, 'm': 25, 'n': 18, 'o': 18, 'p': 18, 'q': 17, 'r': 14,
             's': 15, 't': 10,'u': 20, 'v': 21, 'w': 21, 'x': 18, 'y': 21, 'z': 17, '0': 16,
             '1': 12, '2': 18, '3': 17, '4': 15, '5': 17, '6': 15, '7': 15, '8': 15, '9': 17}
    
    scr()
        
    for index in range(2):
        color_p_ = color_p[index]
        
        # show names
        name_str = "%s : %d" % (names[index], len(snakes[index])-1)
        name_width = 70 if not index else 1827-sum([alphasize[letter] for letter in name_str.replace(" : ", "")])
        text(name_str, 40, color_p_, (name_width, 15))
    
        # show snakes
        for cell in snakes[index]:
            rect(color_p_, (60+cell[0]*cell_size,60+cell[1]*cell_size,cell_size,cell_size))
    
    # show coin
    coin_color = (120,0,0)
    rect(coin_color, (60+coin[0]*cell_size,60+coin[1]*cell_size,cell_size,cell_size))
    
    time2 = localtime()[5]
    if time2-time1 == 1 or time1-time2 == 59:
        game_time["second"] -= 1
        if game_time["second"] == -1:
            game_time["second"] = 59
            game_time["minute"] -= 1
        
        # time is up
        if game_time["minute"] == game_time["second"] == 0:
            show_time(game_time)
            
            # if scores were equal, 30 seconds will be added to the time
            if len(snakes[0]) == len(snakes[1]):
                game_time["second"] = 30
                game_time["extra"] = 1
            
            # otherwise one of the players has won and the game ends
            else:
                winner = 0 if len(snakes[0]) > len(snakes[1]) else 1
                game_over_2player(snakes, names, color_p, winner)
                return 0, 0
    
    show_time(game_time)
    
    return 1, time2

def in_time():
    cell_size = 60
    screen_size = [30, 16]
    range_x = (0, screen_size[0])
    range_y = (0, screen_size[1])
    die_in_wall = False
    
    snakes = [[], []]
    
    # define first snake
    start_x = randrange(*range_x)
    start_y = randrange(*range_y)
    snakes[0] = [(start_x, start_y)]
    
    # define second snake
    while True:
        start_x = randrange(*range_x)
        start_y = randrange(*range_y)
        if (start_x, start_y) not in snakes[0]:
            snakes[1] += [(start_x, start_y)]
            break
    
    # define first coin
    coin = new_coin(range_x, range_y, snakes)
    
    # select player's colors
    color_p = select_game_color()
    if not color_p:
        return 0
    
    # show dots and enter player's names
    names = game_start_2player(color_p)
    if not names:
        return 0
    
    motions = ["left", "left"]
    game_time = {"minute": 2, "second": 0, "extra": 0}
    time1 = localtime()[5]
    while True:
        moves = [False, False]
        sleep(0.1)
        
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE and not stop():
                    return 0
                
                if evento.key in arrow_keys:
                    direct, player = arrow_keys[evento.key]
                    if not moves[player] and (motions[player] != directs[direct] or len(snakes[player]) == 1):
                        motions[player] = direct
                        moves[player] = True
        
        for index in range(2):
            # shift the snake's body and give direction to its head
            move_snake(snakes[index], motions[index], die_in_wall, screen_size)
        
            # eat coin, append new cell to end of snake and define a new coin
            if snakes[index][0] == coin:
                coin = eat_coin(snakes[index], motions[index], die_in_wall, screen_size, snake2 = snakes[1-index])
        
            # the snake's head hits its body -> the snake get smaller
            if snakes[index][0] in snakes[index][1:]:
                snakes[index] = snakes[index][:snakes[index][1:].index(snakes[index][0])+1]
           
        time1 = show(snakes, coin, names, color_p, cell_size, game_time, time1)
        if not time1[0]:
            return 0
        time1 = time1[1]
        
        pygame.display.flip()