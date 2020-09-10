from game.functions.one_player import *

def show(snake, coin, cell_size):
    # show score
    text("Score : %d" % (len(snake)-1), 40, "lite", (70, 15))
    
    # show snake
    for cell in snake:
        rect("color2", (60+cell[0]*cell_size,60+cell[1]*cell_size,cell_size,cell_size))
    
    # show coin
    rect("color1", (60+coin[0]*cell_size,60+coin[1]*cell_size,cell_size,cell_size))
    
    pygame.display.flip()

def classic():
    cell_size = 60
    screen_size = [30, 16]
    range_x = (0, screen_size[0])
    range_y = (0, screen_size[1])
    die_in_wall = False
    
    scr()
    
    if not start():
        return 0
    
    # define snake
    start_x = randrange(*range_x)
    start_y = randrange(*range_y)
    snake = [(start_x, start_y)]
    
    # define first coin
    coin = new_coin(range_x, range_y, [snake])
    
    motion = "left"
    while True:
        scr()
        show(snake, coin, cell_size)
        
        move = False
        sleep(0.1)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or ( evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE ):
                if not stop():
                    return 0
            
            elif evento.type == pygame.KEYDOWN and evento.key in arrow_keys and not move:
                direct = arrow_keys[evento.key]
                if motion != directs[direct] or len(snake) == 1:
                    motion = direct
                    move = True
        
        # shift the snake's body and give direction to its head
        move_snake(snake, motion, die_in_wall, screen_size)
        
        # eat coin, append new cell to end of snake and define a new coin
        if snake[0] == coin:
            coin = eat_coin(snake, motion, die_in_wall, screen_size)
        
        # the snake's head hits its body -> game over
        if snake[0] in snake[1:]:
            game_over(len(snake)-1)
            return 0