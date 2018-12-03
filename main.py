# initialize the screen
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

        self.pads, self.trophies, self.car_pos, self.global_time = levels.level1()
        self.pad_group = pygame.sprite.RenderPlain(*self.pads)
        self.trophy_group = pygame.sprite.RenderPlain(*self.trophies)

        self.genetic_algorithm = genetic.GeneticAlgorithm(pool_size=10)
        self.cheat = False

    # Uses euclidean distance to return FORWARD, BACKWARD, LEFT, RIGHT euclidean distances
    def projection(self, x, y, orientation, scalar):
        # forward
        o_x = round(math.cos(math.radians(orientation)) * scalar, 3)
        o_y = round(math.sin(math.radians(orientation)) * scalar, 3)
        set_d1 = (x + o_x), \
                 (y - o_y)
        # backward
        set_d2 = (x + o_x), \
                 (y + o_y)

        # left/right requires orientation swap
        d_orientation = (orientation - 90) % 360
        o_x = round(math.cos(math.radians(d_orientation)) * scalar, 3)
        o_y = round(math.sin(math.radians(d_orientation)) * scalar, 3)
        # left
        set_d3 = (x - o_x), \
                 (y + o_y)
        # right
        set_d4 = (x + o_x), \
                 (y - o_y)

        return set_d1, set_d2, set_d3, set_d4

    def in_area(self, pad, dx, dy):
        if pad.rect.topleft[0] <= dx <= pad.rect.topright[0]:
            if pad.rect.topleft[1] <= dy <= pad.rect.bottomleft[1]:
                return True
        return False

    def calculate_closest_pad_by_direction(self, car):
        directions = [sys.maxsize for i in range(0, 4)]
        for pad in self.pads:
            for scale in range(20, 140):
            #scale = 90
                for index, direction in enumerate(
                        self.projection(car.position[0], car.position[1], car.orientation, scale)):
                    if self.in_area(pad, direction[0], direction[1]) and directions[index] == sys.maxsize:
                        directions[index] = (scale/10)
                        #directions[index] = 1

        return directions

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

    def run_level(self, level=4):

        # Fix for double run of 1
        if level == 1:
            self.pads, self.trophies, self.car_pos, self.global_time = levels.level1()
        elif level == 2:
            self.pads, self.trophies, self.car_pos, self.global_time = levels.level2()
        elif level == 3:
            self.pads, self.trophies, self.car_pos, self.global_time = levels.level3()
        elif level == 4:
            self.pads, self.trophies, self.car_pos, self.global_time = levels.level4()
        elif level == 5:
            self.pads, self.trophies, self.car_pos, self.global_time = levels.level5()

        self.pad_group = pygame.sprite.RenderPlain(*self.pads)
        self.trophy_group = pygame.sprite.RenderPlain(*self.trophies)

        self.win_condition = None
        t0 = time.time()
        cars = list(self.genetic_algorithm.construct_cars(self.car_pos))
        car_group = pygame.sprite.RenderPlain(*cars)

        self.generation = self.small_font.render('Generation ' + str(self.current_generation), False, (255, 0, 0))

        # LOOP
        while True:

            for event in pygame.event.get():
                if not hasattr(event, 'key'): continue
                if event.key == K_ESCAPE:
                    print("Exiting AI.")
                    sys.exit(0)

            # Main iteration loop
            computation_time = time.time()
            for i in range(len(cars)):
                if cars[i].alive:
                    # if event.key == K_SPACE:
#                    down = event.type == KEYDOWN
                    if self.win_condition:
                        pygame.mixer.music.stop()
                        self.run_level(level=(level))
                    '''
                    if event.key == K_RIGHT:
                        cars[i].k_right = down * -5
                    elif event.key == K_LEFT:
                        cars[i].k_left = down * 5
                    elif event.key == K_UP:
                        cars[i].k_up = down * 2
                    elif event.key == K_DOWN:
                        cars[i].k_down = down * -2
                    '''
                    car_data = cars[i].get_car_data()
                    distances = self.calculate_closest_pad_by_direction(cars[i])
                    data = [
                            distances[0],
                            distances[1],
                            distances[2],
                            distances[3],
                            cars[i].speed,
                    ]
                    predictions = cars[i].decision(data)
                    dir = predictions[:].argmax()
#                    print("{} - {} --> {}".format(data, predictions, dir))
#                    dir = -1
                    if dir == 0:
                        cars[i].k_up = 2
                    elif dir == 1:
                        cars[i].k_down = -2
                    elif dir == 2:
                        cars[i].k_left = 5
                    elif dir == 3:
                        cars[i].k_right = -5

                cars[i].add_history(dir, distances=distances)

            computation_time = time.time() - computation_time
            t1 = time.time()
            dt = t1 - t0 - computation_time

            deltat = self.clock.tick(30)
            seconds = round((self.global_time - dt), 2)

            # COUNTDOWN TIMER
            if self.win_condition is None:
                timer_text = self.font.render(str(seconds), True, (255, 255, 0))
                if seconds <= 0:
                    self.win_condition = False
                    self.genetic_algorithm.evaluate_performance(cars,
                                                                (self.trophies[0].rect.x, self.trophies[0].rect.y))
                    self.current_generation += 1
                    self.run_level(level)

            # RENDERING
            self.screen.fill((0, 0, 0))
            car_group.update(deltat)
            collisions = pygame.sprite.groupcollide(car_group, self.pad_group, False, False, collided=None)
            if collisions != {}:
                for car in collisions:
                    for index, c in enumerate(cars):
                        if c is car:
                            cars[index].alive = False
                    car_group.remove(car)
                if len(car_group) == 0:
                    # win_condition = False
                    self.genetic_algorithm.evaluate_performance(cars,
                                                                (self.trophies[0].rect.x, self.trophies[0].rect.y))
                    self.current_generation += 1
                    self.run_level(level)

            trophy_collision = pygame.sprite.groupcollide(car_group, self.trophy_group, False, True)
            if trophy_collision != {}:
                for car in trophy_collision:
                    car_group.empty()
                    car_group.add(car)
                    seconds = seconds
                    timer_text = self.font.render("Finished!", True, (0, 255, 0))
                    self.win_condition = True
                    car.MAX_FORWARD_SPEED = 0
                    car.MAX_REVERSE_SPEED = 0
                    pygame.mixer.music.play(loops=0, start=0.0)
                    if self.win_condition:
                        car.k_right = -5

            self.pad_group.update(collisions)
            self.pad_group.draw(self.screen)
            car_group.draw(self.screen)
            self.trophy_group.draw(self.screen)
            # Counter Render
            self.screen.blit(timer_text, (20, 60))
            self.screen.blit(self.win_text, (250, 700))
            self.screen.blit(self.loss_text, (250, 700))
            self.screen.blit(self.generation, (850, 60))
            pygame.display.flip()
