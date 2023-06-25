import pygame as pg
from collections import namedtuple
from enum import Enum
import random
import numpy as np


#reset
#reward
#play(action) -> direction
# game_iteration
# is_collision
# get_state
TILESIZE =20
WIDTH = 800
Speed = 700
pg.init()
window = 800
tile_size = 20
smallfont = pg.font.SysFont("comicsansms", 25)
class Direction(Enum):
    Right = 1
    Left = 2
    Up =3
    Down = 4

Point = namedtuple('Point', 'x, y')

class SnakeGameAI:
    
        def __init__(self, w=window, h=window):
            self.w = w
            self.h = h
            self.display = pg.display.set_mode((self.w, self.h))
            pg.display.set_caption('Snake')
            self.clock = pg.time.Clock()
            self.reset()
            self.direction = Direction.Right
            self.score = 0
            self.head = Point(self.w/2, self.h/2)
            self.snake = [self.head, Point(self.head.x-tile_size, self.head.y), Point(self.head.x-(2*tile_size), self.head.y)]
            self.score = 0
            self.food = None
            self._place_food()
            self.frame_iteration = 0 
        
        def reset(self):
            self.direction = Direction.Right
            self.head = Point(self.w/2, self.h/2)
            self.snake = [self.head, Point(self.head.x-tile_size, self.head.y), Point(self.head.x-(2*tile_size), self.head.y)]
            self.score = 0
            self.food = None
            self._place_food()
            self.frame_iteration = 0
        
        
        def _place_food(self):
            x = random.randint(0, (self.w-tile_size)//tile_size)*tile_size
            y = random.randint(0, (self.h-tile_size)//tile_size)*tile_size
            self.food = Point(x,y)
            if self.food in self.snake:
                self._place_food() #recursion
                
        
        
            
        def is_collision(self,pt=None):
            if pt is None:
                pt=self.head
            if pt.x> self.w-tile_size or pt.x < 0 or pt.y > self.h-tile_size or pt.y < 0:
                return True
            if pt in self.snake[1:]:
                return True
            return False
        
        def _update_ui(self):
            self.display.fill((0,0,0))
            
            for pt in self.snake:
                pg.draw.rect(self.display, (0,255,0), pg.Rect(pt.x, pt.y, tile_size, tile_size))
                pg.draw.rect(self.display, (0,0,255), pg.Rect(pt.x+4, pt.y+4, 12, 12))
                
            pg.draw.rect(self.display, (255,0,0), pg.Rect(self.food.x, self.food.y, tile_size, tile_size))
            text = smallfont.render("Score: " + str(self.score), True, (255,255,255))
            self.display.blit(text, [0,0])
            pg.display.flip()
        
        def _move(self,action):
            #[1,0,0] -> straight
            #[0,1,0] -> right
            #[0,0,1] -> left
            
            clock_wise = [Direction.Right, Direction.Down, Direction.Left, Direction.Up]
            idx = clock_wise.index(self.direction)
            
            if np.array_equal(action, [1,0,0]):
                new_dir = clock_wise[idx] #no change
            elif np.array_equal(action, [0,1,0]):
                new_dir = clock_wise[(idx+1)%4] #right turn r->d->l->u
            else: # [0,0,1]
                new_dir = clock_wise[(idx-1)%4] #left turn r->u->l->d
            
            self.direction = new_dir
            
            
            x = self.head.x
            y = self.head.y
            if self.direction == Direction.Right:
                x += tile_size
            elif self.direction == Direction.Left:
                x -= tile_size
            elif self.direction == Direction.Up:
                y -= tile_size
            elif self.direction == Direction.Down:
                y += tile_size
                
            self.head = Point(x,y)
        
        def play_step(self, action):
            self.frame_iteration += 1
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

            self._move(action)
            self.snake.insert(0, self.head)
            
            
            reward = 0
            
            game_over = False
            if self.is_collision() or self.frame_iteration > 100*len(self.snake):
                game_over = True
                reward = -10
                return game_over, self.score,reward
                
            if self.head == self.food:
                self.score += 1
                reward =10
                self._place_food()
            else:
                self.snake.pop()
                
            self._update_ui()
            self.clock.tick(Speed)
            return game_over, self.score, reward
            