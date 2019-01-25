#!/usr/bin/env python
"""
anty.py

Stupid implementation of Langton's ant with options to specify the angle the
ant turns, as well as number of ants.

Press 'S' to save an image of the current bugs, filname promt at command line.

"""


import pygame
from pygame.locals import QUIT, KEYDOWN, K_s
from random import randint
from math import cos, sin, radians, sqrt

class Ant(object):
    """WHAT IS THIS? DOCSTRINGS FOR ANTS?
    """


    def __init__(self, ants=None, angle=None, random_pos=False):
        """ants is the amount of ants
        angle is turn angle in degrees
        random_pos is booleanish, determines if ant spawns in center or not
        Ant(1,90) gives a classic Langton's ant
        Ant(5,30,True) gives 5 30 degree anarchy ants.
        """

        try:
            self.ants = [[] for i in range(ants)]
        except:
            self.gief_ants()

        try:
            self.angle = float(angle)
        except:
            self.gief_angle()


        self.get_thetas(self.angle)
        self.ui_init()        
        self.spawn_ant(random_pos)
        self.going = True


    def ui_init(self):
        """Why do birds suddenly appear.
        """
        pygame.init()        
        background = pygame.Surface((800,800))
        background.fill((200,200,200))
        self.screen = pygame.display.set_mode((background.get_width(), 
                                               background.get_height()))
        self.screen.blit(background, (0,0))
        pygame.display.set_caption("{} turning by {} degrees".format(
                                            len(self.ants), self.angle))
        
    def gief_ants(self):
        """Promt user for number of ants, on error assumes 1 ant.
        """
        try:
            self.ants = [[] for i in range(int(raw_input("How many ants: ")))]
        except ValueError as e:
            print e
            print "Not hotdog, assuming 1 ant"
            self.ants = [[]]

    def gief_angle(self):
        """Promt user for turn angle, on error assumes 90 degrees.
        """        
        try:
            self.angle = float(raw_input("Turn angle in degrees(1-359): "))
        except ValueError as e:
            print e
            print "Computer says no.. Assuming 90 degrees"
            self.angle = 90


    def get_thetas(self, angle):
        """You get it, angle is in degrees
        """
        self.cos_t = cos(radians(angle))
        self.sin_t = sin(radians(angle))
        
    
    def spawn_ant(self, random_position):
        """Spawns ant(s) either at random locations or at the center.
        """
        if random_position:
            self.ants = [[randint(100, self.screen.get_width()-100) +0.5,
                  randint(100, self.screen.get_height()-100) +0.5]
                  for i in self.ants]
        else:
            self.ants = [[400.5,400.5] for i in self.ants]

        self.ants_last_cell = [(-1,0) for i in self.ants]
        self.ant_dir = [[-0.01,0] for i in self.ants]


    def black_or_white(self,pixel):
        """Check if a pixel is 'white' or 'not hotdog',
        pixel can be any color
        """
        if (pixel[0] + pixel[1] + pixel[2]) / 3 > 120:
            return "white"
        return "not hotdog"


    def search_and_swap(self):
        """Checks if the ant(s) has arrived at a new pixel, if so,
        flips it and turn the ant
        """
        for i, ant in enumerate(self.ants):
            this_ant =  (int(ant[0]), int(ant[1])) 
            if this_ant != self.ants_last_cell[i]:
                pixel = self.screen.get_at(this_ant)
                self.ants_last_cell[i] = this_ant
                if self.black_or_white(pixel) == "white":
                    x = self.ant_dir[i][0]*self.cos_t - \
                        self.ant_dir[i][1]*self.sin_t
                    y = self.ant_dir[i][0]*self.sin_t + \
                        self.ant_dir[i][1]*self.cos_t
                    self.screen.set_at(this_ant, (30,30,30))
                else:
                    x = -self.ant_dir[i][0]*self.cos_t + \
                        self.ant_dir[i][1]*self.sin_t
                    y = -self.ant_dir[i][0]*self.sin_t - \
                        self.ant_dir[i][1]*self.cos_t
                    self.screen.set_at(this_ant, (255,255,255))
                self.ant_dir[i][0] = x
                self.ant_dir[i][1] = y

                
    def move_it(self):
        """Moves all the ants one step
        """
        for i in range(len(self.ants)):
            self.ants[i][0] += self.ant_dir[i][0]
            self.ants[i][1] += self.ant_dir[i][1]
                    

    def ant_on_the_loose(self):
        """Check if ants are running off the display, if they are, they get
        removed. When no ants remain, the run() loop terminates.
        """
        dead_ants = []
        for i in range(len(self.ants)):
            if self.ants[i][0] >= self.screen.get_width() or self.ants[i][0] < 0 \
              or self.ants[i][1] >= self.screen.get_height() or self.ants[i][1] < 0:            
                dead_ants.append(i)
        for i in dead_ants:
            del self.ants[i]
            del self.ant_dir[i]
            del self.ants_last_cell[i]
            
        if len(self.ants) < 1:
            self.going = False

                
    def save_img(self):
        """Saves an image of the current ant(s), promt at commandline
        """
        dest = raw_input("File to save to: ")
        pygame.image.save(self.screen, dest)             
        print "Saving to {}".format(dest)

                   
    def update(self):
        self.search_and_swap()
        self.move_it()
        self.ant_on_the_loose()


    def run(self):
        """Checks for events and fire updates
        runs 1000 loops for each display update, because.
        """
        update_time = 1000
        while self.going:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.going = False
                elif event.type == KEYDOWN:
                    if event.key == K_s:
                        self.save_img()

            self.update()
    
            update_time += 1
            
            if update_time > 1000:
                pygame.display.flip()
                update_time = 0

        pygame.quit()


if __name__ == "__main__":
    Ant().run()




        
