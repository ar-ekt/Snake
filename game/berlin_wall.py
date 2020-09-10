from game.functions.two_player import *

def is_round_over(snakes, wall_movement, screen_size):
    snakes_win = [False, False]
    
    snakes_win[1] |= snakes[0][0][0] in [-1, screen_size[0]+wall_movement]
    snakes_win[1] |= snakes[0][0][1] in [-1, screen_size[1]]
    snakes_win[1] |= snakes[0][0] in snakes[0][1:]
    
    snakes_win[0] |= snakes[1][0][0] in [-1+wall_movement, screen_size[0]]
    snakes_win[0] |= snakes[1][0][1] in [-1, screen_size[1]]
    snakes_win[0] |= snakes[1][0] in snakes[1][1:]
    
    if snakes_win[0] and snakes_win[1]:
        return 2
    elif snakes_win[1]:
        return 1
    elif snakes_win[0]:
        return 0
    else:
        return -1

def show(snakes, coins, wall_movement, names, scores, color_p, cell_size):
    alphasize = {'a': 16, 'b': 20, 'c': 16, 'd': 17, 'e': 19, 'f': 13, 'g': 17, 'h': 18, 'i': 9,
             'j': 8,'k': 18, 'l': 10, 'm': 25, 'n': 18, 'o': 18, 'p': 18, 'q': 17, 'r': 14,
             's': 15, 't': 10,'u': 20, 'v': 21, 'w': 21, 'x': 18, 'y': 21, 'z': 17, '0': 16,
             '1': 12, '2': 18, '3': 17, '4': 15, '5': 17, '6': 15, '7': 15, '8': 15, '9': 17}
    color_red = (120,0,0)
    
    scr()
    
    for index in range(2):
        name_str = "%s : %d" % (names[index], scores[index])
        name_width = 70 if not index else 1827-sum([alphasize[letter] for letter in name_str.replace(" : ","")])
        text(name_str, 40, color_p[index], (name_width, 15))
    
    for cell in snakes[0]:
        rect(color_p[0],(60+cell[0]*cell_size,60+cell[1]*cell_size,cell_size,cell_size))
    for cell in snakes[1]:
        rect(color_p[1],(980+cell[0]*cell_size,60+cell[1]*cell_size,cell_size,cell_size))
    
    rect(color_red, (60+coins[0][0]*cell_size,60+coins[0][1]*cell_size,cell_size,cell_size))
    rect(color_red, (980+coins[1][0]*cell_size,60+coins[1][1]*cell_size,cell_size,cell_size))
    rect(lite, ((wall_movement*cell_size)+940,60,cell_size,960))
    
    pygame.display.flip()

def berlin_wall():
    cell_size = 40
    screen_size = [22, 24]
    range_x = (0, screen_size[0])
    range_y = (0, screen_size[1])
    die_in_wall = True
    
    # color of players
    color_p = select_game_color()
    if not color_p:
        return 0
    
    # number of rounds to win
    rounds_to_win = number_of_rounds()
    if not rounds_to_win:
        return 0
    
    # show dots and enter player's names
    names = game_start_2player(color_p)
    if not names:
        return 0
    
    round_num = 1
    round_winner = -1
    scores = [0, 0]
    
    while True:
        
        show_start_round_2player([scores[0], scores[1]], names, color_p, round_num, round_winner)
        
        if not is_ready_2player(color_p):
            return 0
        
        # define snakes
        snakes = [[(10,11)], [(10,11)]]
        
        # define first coins
        coins = [None, None]
        for index in range(2):
            coins[index] = new_coin(range_x, range_y, [snakes[index]])
        
        # wall movement
        wall_movement = 0
        
        pre_motions = ["", ""]
        motions = ["stop", "stop"]
        exit_round = True
        while exit_round:
            
            sleep(0.1)
            
            moves = [False, False]
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE and not stop():
                        return 0
                    
                    if evento.key in arrow_keys:
                        direct, player = arrow_keys[evento.key]
                        if not moves[player]:
                            if (motions[player] != directs[direct] or len(snakes[player]) == 1) and (motions[player] != "stop" or pre_motions[player] == "" or direct != directs[pre_motions[player]]):
                                pre_motions[player] = ""
                                motions[player] = direct    
                                moves[player] = True
                            
                            elif motions[player] == directs[direct]:
                                pre_motions[player] = motions[player]
                                motions[player] = "stop"
                                moves[player] = True
            
            for index in range(2):
                if motions[index] != "stop" or len(snakes[index]) == 1:
                    move_snake(snakes[index], motions[index], True, screen_size)
            
            if snakes[0][0] == coins[0]:
                wall_movement += 1
                coins = eat_coin(snakes[0], motions[0], die_in_wall, screen_size, wall_movement, snakes[1], True)
            
            elif snakes[1][0] == coins[1]:
                wall_movement -= 1
                coins = eat_coin(snakes[1], motions[1], die_in_wall, screen_size, wall_movement, snakes[0], True)
            
            round_winner = is_round_over(snakes, wall_movement, screen_size)
            if round_winner != -1:
                if round_winner != 2:
                    scores[round_winner] += 1
                exit_round = False
            
            show(snakes, coins, wall_movement, names, scores, color_p, cell_size)
        
        sleep(1)
        round_num += 1
        if rounds_to_win in scores:
            winner = scores.index(rounds_to_win)
            game_over_2player(snakes, names, color_p, winner, False)
            return 0