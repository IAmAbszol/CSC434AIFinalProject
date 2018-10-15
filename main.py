#initialize the screen
import pygame, math, sys, time
from pygame.locals import *

from ai import genetic
import levels

class Main():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 768))
        # GAME CLOCK
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 75)
        self.win_font = pygame.font.Font(None, 50)
        self.win_condition = None
        self.win_text = self.font.render('', True, (0, 255, 0))
        self.loss_text = self.font.render('', True, (255, 0, 0))
        pygame.mixer.music.load('My_Life_Be_Like.mp3')
        self.t0 = time.time()
        self.pads, self.trophies, self.car_pos = levels.level1()
        self.pad_group = pygame.sprite.RenderPlain(*self.pads)
        self.trophy_group = pygame.sprite.RenderPlain(*self.trophies)

    def run_level(self, level=1):

        genetic_algorithm = genetic.GeneticAlgorithm()
        cars = genetic_algorithm.construct_cars(self.car_pos)
        car_group = pygame.sprite.RenderPlain(*cars)

        #LOOP
        while True:

            t1 = time.time()
            dt = t1 - self.t0

            deltat = self.clock.tick(30)
            for event in pygame.event.get():
                if not hasattr(event, 'key'): continue
                if event.key == K_ESCAPE:
                    print("Exiting AI.")
                    sys.exit(0)

                #elif self.win_condition == True and event.key == K_SPACE: levels.level2()
                #elif self.win_condition == False and event.key == K_SPACE:
                    #load_level()
                    #t0 = t1

            # Main iteration loop
            for i in range(len(cars)):
                predictions = cars[i].decision(cars[i].get_car_data().extend([self.trophies[0].rect.x, self.trophies[0].rect.y]))
                if predictions[0] > .5:
                    cars[i].k_up = 2
                if predictions[1] > .5:
                    cars[i].k_down = -2
                if predictions[2] > .5:
                    cars[i].k_left = -5
                if predictions[3] > .5:
                    cars[i].k_right = 5

            #COUNTDOWN TIMER
            seconds = round((20 - dt),2)
            if win_condition == None:
                timer_text = self.font.render(str(seconds), True, (255,255,0))
                if seconds <= 0:
                    win_condition = False
                    timer_text = self.font.render("Time!", True, (255,0,0))
                    loss_text = self.win_font.render('Press Space to Retry', True, (255,0,0))


            #RENDERING
            self.screen.fill((0,0,0))
            car_group.update(deltat)
            collisions = pygame.sprite.groupcollide(car_group, self.pad_group, False, False, collided = None)
            if collisions != {}:
                for car in collisions:
                    car_group.remove(car)
                if len(car_group) == 0:
                    win_condition = False

            trophy_collision = pygame.sprite.groupcollide(car_group, self.trophy_group, False, True)
            if trophy_collision != {}:
                for car in trophy_collision:
                    car_group.empty()
                    car_group.add(car)
                    seconds = seconds
                    timer_text = self.font.render("Finished!", True, (0,255,0))
                    win_condition = True
                    car.MAX_FORWARD_SPEED = 0
                    car.MAX_REVERSE_SPEED = 0
                    pygame.mixer.music.play(loops=0, start=0.0)
                    win_text = self.win_font.render('Press Space to Advance', True, (0,255,0))
                    if win_condition == True:
                        car.k_right = -5

            self.pad_group.update(collisions)
            self.pad_group.draw(self.screen)
            car_group.draw(self.screen)
            self.trophy_group.draw(self.screen)
            #Counter Render
            self.screen.blit(timer_text, (20,60))
            self.screen.blit(win_text, (250, 700))
            self.screen.blit(loss_text, (250, 700))
            pygame.display.flip()

