import pygame as pg
from random import randrange

pg.init()
window = 800
tile_size = 20
range =(tile_size // 2, window - tile_size // 2, tile_size)
get_rand_pos = lambda: (randrange(*range), randrange(*range))

snake = pg.rect.Rect(0,0, tile_size-2, tile_size-2)

snake.center = get_rand_pos()
length =1
snake_direction = (0, 0)
time,time_step = 0, 40

smallfont = pg.font.SysFont("comicsansms", 45)

segments = [snake.copy()]

food = snake.copy() 
food.center = get_rand_pos()




screen = pg.display.set_mode((window, window))
clock = pg.time.Clock()

dirct ={pg.K_UP:1, pg.K_DOWN:1, pg.K_LEFT:1,pg.K_RIGHT:1}

def score(score):
    text = smallfont.render("Score: "+str(score), True, 'white')
    screen.blit(text, [300,0])

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and dirct[pg.K_UP]:
                snake_direction=(0,-tile_size)
                dirct ={pg.K_UP:1, pg.K_DOWN:0, pg.K_LEFT:1,pg.K_RIGHT:1}  
            if event.key == pg.K_DOWN and dirct[pg.K_DOWN]:
                snake_direction=(0,tile_size)
                dirct ={pg.K_UP:0, pg.K_DOWN:1, pg.K_LEFT:1,pg.K_RIGHT:1}  
            if event.key == pg.K_LEFT and dirct[pg.K_LEFT]:
                snake_direction=(-tile_size,0)
                dirct ={pg.K_UP:1, pg.K_DOWN:1, pg.K_LEFT:1,pg.K_RIGHT:0}     
            if event.key == pg.K_RIGHT and dirct[pg.K_RIGHT]:
                snake_direction=(tile_size,0) 
                dirct ={pg.K_UP:1, pg.K_DOWN:1, pg.K_LEFT:0,pg.K_RIGHT:1}  
            
    screen.fill((0, 0, 0))
    
    self_easting = pg.Rect.collidelist(snake,segments[:-1]) != -1
    
    
    if snake.left < 0 or snake.right > window or snake.top < 0 or snake.bottom > window or self_easting:
        snake_direction = (0, 0)
        snake.center = get_rand_pos()
        length = 1
        segments = [snake.copy()]
        food.center = get_rand_pos()
    
    
    if snake.colliderect(food):
        length += 1
        food.center = get_rand_pos()
    
    
    pg.draw.rect(screen, 'blue', food)
    
    [pg.draw.rect(screen, 'green', s) for s in segments]
    
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_direction)
        segments.append(snake.copy())
        segments = segments[-length:]
    
    score(length-1)
    pg.display.update()
    clock.tick(60)