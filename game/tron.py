from game.functions.two_player import *

def is_game_over(snakes, range_x, range_y):
    snakes_win = [False, False]
    
    for index in range(2):
        snakes_win[index] |= snakes[1-index][0] in snakes[1-index][1:]
        snakes_win[index] |= snakes[1-index][0] in snakes[index]
        snakes_win[index] |= snakes[1-index][0][0] not in range(*range_x)
        snakes_win[index] |= snakes[1-index][0][1] not in range(*range_y)
    
    if snakes_win[0] and snakes_win[1]:
        return 2
    elif snakes_win[1]:
        return 1
    elif snakes_win[0]:
        return 0
    else:
        return -1

def show(snakes, names, color_p, cell_size):
    alphasize = {'a': 16, 'b': 20, 'c': 16, 'd': 17, 'e': 19, 'f': 13, 'g': 17, 'h': 18, 'i': 9,
             'j': 8,'k': 18, 'l': 10, 'm': 25, 'n': 18, 'o': 18, 'p': 18, 'q': 17, 'r': 14,
             's': 15, 't': 10,'u': 20, 'v': 21, 'w': 21, 'x': 18, 'y': 21, 'z': 17, '0': 16,
             '1': 12, '2': 18, '3': 17, '4': 15, '5': 17, '6': 15, '7': 15, '8': 15, '9': 17}
    
    scr()
        
    for index in range(2):
        color_p_ = color_p[index]
        
        # show names
        name_str = "%s" % names[index]
        name_width = 70 if not index else 1837-sum([alphasize[letter] for letter in name_str])
        text(name_str, 40, color_p_, (name_width, 15))
    
        # show snakes
        for cell in snakes[index]:
            rect(color_p_, (60+cell[0]*cell_size,60+cell[1]*cell_size,cell_size,cell_size))

def tron():
    cell_size = 20
    screen_size = [90, 48]
    range_x = (0, screen_size[0])
    range_y = (0, screen_size[1])
    die_in_wall = True
    
    snakes = [[(1, 1)], [(screen_size[0]-2, screen_size[1]-2)]]
    
    # player's colors
    color_p = [(0, 240, 240), (200, 100, 0)]
    
    # show dots and enter player's names
    names = game_start_2player(color_p)
    if not names:
        return 0
    
    motions = ["right", "left"]
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
            snakes[index] = [snakes[index][0]] + snakes[index]
            move_head(snakes[index], motions[index], die_in_wall, screen_size)
        
        winner = is_game_over(snakes, range_x, range_y)
        if winner != -1:
            game_over_2player(snakes, names, color_p, winner, False)
            return 0
           
        show(snakes, names, color_p, cell_size)
        
        pygame.display.flip()