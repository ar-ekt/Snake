from globals_ import *

arrow_keys = {pygame.K_UP: "up",
              pygame.K_DOWN: "down",
              pygame.K_RIGHT: "right",
              pygame.K_LEFT: "left"}
directs = {"up": "down", "down": "up", "right": "left", "left": "right"}

def start():
    ignore_coors = [[(480, 630), (510, 1410)]]
    show_dots(120, (2,62), (2,34), ignore_coors)
    
    text("CLICK TO START", 150, "color2", (540, 515))
    
    pygame.display.flip()
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return 0
                return 1

def game_over(score, write_in_file = True):
    rect("bg", (637,517,646,133))
    text("GAME OVER", 150, "color1", (644, 515))
    pygame.display.flip()
    
    sleep(1)
    
    cursor = 0
    name = ""
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if (evento.key == pygame.K_KP_ENTER or evento.key == pygame.K_RETURN) and len(name) != 0:
                    bests = open(bests_file_name)
                    best = bests.readlines()
                    best.insert(best.index("\n"), "%s %d\n" % (name, score))
                    bests.close()
                    bests = open(bests_file_name,"w")
                    bests.write("".join(best))
                    bests.close()
                    return 0
                
                elif evento.key == pygame.K_BACKSPACE and len(name) != 0:
                    name = name[:-1]
                
                elif ("0" <= evento.unicode <= "9" or "a" <= evento.unicode.lower() <= "z") and len(name) <= 16:
                    name += evento.unicode.lower()
        
        rect("bg", (637,610,646,40))
        str_name = "Name: %s%s" % (name, "|" if 0 <= cursor % 100 <= 49 else "")
        text(str_name, 50, "color2", (644, 615))
        
        pygame.display.flip()
        cursor += 1