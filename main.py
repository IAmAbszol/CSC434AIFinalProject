#initialize the screen
import pygame, math, sys, time, numpy as np
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
        self.win_text = self.font.render('', True, (0, 255, 0))
        self.loss_text = self.font.render('', True, (255, 0, 0))
        self.current_generation = 0
        self.small_font = pygame.font.Font(None, 32)
        self.generation = self.small_font.render('Generation ' + str(self.current_generation), False, (255, 0, 0))
        pygame.mixer.music.load('My_Life_Be_Like.mp3')
        self.pads, self.trophies, self.car_pos = levels.level1()
        self.pad_group = pygame.sprite.RenderPlain(*self.pads)
        self.trophy_group = pygame.sprite.RenderPlain(*self.trophies)

        self.genetic_algorithm = genetic.GeneticAlgorithm(pool_size=500)
        self.cheat = True

    # Uses euclidean distance to calculate closest pad, returns pad and distance
    def calculate_closest_pad(self, car):
        pad_number, distance = 0, sys.maxsize
        for index, pad in enumerate(self.pads):
            # top left
            tp, td = index, genetic.euclidean((car.position[0], pad.rect.topleft[0]),
                                              (car.position[1], pad.rect.topleft[1]))
            if td < distance:
                pad_number, distance = tp, td
            # top right
            tp, td = index, genetic.euclidean((car.position[0], pad.rect.topright[0]),
                                              (car.position[1], pad.rect.topright[1]))
            if td < distance:
                pad_number, distance = tp, td
            # bottom left
            tp, td = index, genetic.euclidean((car.position[0], pad.rect.bottomleft[0]),
                                              (car.position[1], pad.rect.bottomleft[1]))
            if td < distance:
                pad_number, distance = tp, td
            # bottom right
            tp, td = index, genetic.euclidean((car.position[0], pad.rect.bottomright[0]),
                                              (car.position[1], pad.rect.bottomright[1]))
            if td < distance:
                pad_number, distance = tp, td
        return pad_number, distance

    def run_level(self, level=1):

        self.win_condition = None
        t0 = time.time()
        cars = list(self.genetic_algorithm.construct_cars(self.car_pos))
        car_group = pygame.sprite.RenderPlain(*cars)


        self.generation = self.small_font.render('Generation ' + str(self.current_generation), False, (255, 0, 0))

        #LOOP
        while True:

            t1 = time.time()
            dt = t1 - t0

            deltat = self.clock.tick(30)
            seconds = round((20 - dt), 2)
            for event in pygame.event.get():
                if not hasattr(event, 'key'): continue
                if event.key == K_ESCAPE:
                    print("Exiting AI.")
                    sys.exit(0)

            # Main iteration loop
            for i in range(len(cars)):
                car_data = cars[i].get_car_data()
                car_data.extend([self.trophies[0].rect.x, self.trophies[0].rect.y, self.calculate_closest_pad(cars[i])[1], seconds, genetic.euclidean((cars[i].position[0], self.trophies[0].rect.x),
                                                                                                                                                      (cars[i].position[1], self.trophies[0].rect.y))])
                predictions = np.round(cars[i].decision(car_data), 0)
                dir = predictions.argmax() if not self.cheat else 0
                if dir == 0:
                    cars[i].k_up = 2
                elif dir == 1:
                    cars[i].k_down = -2
                elif dir == 2:
                    cars[i].k_left = -5
                elif dir == 3:
                    cars[i].k_right = 5
                if self.cheat:
                    self.cheat = False

            #COUNTDOWN TIMER
            if self.win_condition is None:
                timer_text = self.font.render(str(seconds), True, (255,255,0))
                if seconds <= 0:
                    self.win_condition = False
                    self.genetic_algorithm.evaluate_performance(cars, (self.trophies[0].rect.x, self.trophies[0].rect.y, self.calculate_closest_pad(cars[i])[1], seconds))
                    self.current_generation += 1
                    self.run_level()

            #RENDERING
            self.screen.fill((0,0,0))
            car_group.update(deltat)
            collisions = pygame.sprite.groupcollide(car_group, self.pad_group, False, False, collided = None)
            if collisions != {}:
                for car in collisions:
                    car_group.remove(car)
                if len(car_group) == 0:
                    #win_condition = False
                    self.genetic_algorithm.evaluate_performance(cars, (self.trophies[0].rect.x, self.trophies[0].rect.y, self.calculate_closest_pad(cars[i])[1], seconds))
                    self.current_generation += 1
                    self.run_level()

            trophy_collision = pygame.sprite.groupcollide(car_group, self.trophy_group, False, True)
            if trophy_collision != {}:
                for car in trophy_collision:
                    car_group.empty()
                    car_group.add(car)
                    seconds = seconds
                    timer_text = self.font.render("Finished!", True, (0,255,0))
                    self.win_condition = True
                    car.MAX_FORWARD_SPEED = 0
                    car.MAX_REVERSE_SPEED = 0
                    pygame.mixer.music.play(loops=0, start=0.0)
                    self.win_text = self.win_font.render('Press Space to Advance', True, (0,255,0))
                    if self.win_condition:
                        print(car.Chromosome.Genes)
                        car.k_right = -5

            self.pad_group.update(collisions)
            self.pad_group.draw(self.screen)
            car_group.draw(self.screen)
            self.trophy_group.draw(self.screen)
            #Counter Render
            self.screen.blit(timer_text, (20,60))
            self.screen.blit(self.win_text, (250, 700))
            self.screen.blit(self.loss_text, (250, 700))
            self.screen.blit(self.generation, (850, 60))
            pygame.display.flip()

