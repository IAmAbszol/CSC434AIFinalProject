# initialize the screen
import pygame, math, sys, time
import random
from pygame.locals import *
from shapely.geometry import Polygon

from ai import genetic
import levels


class Main():

    def __init__(self, pool=250):
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

        self.pads, self.trophies, self.car_pos, self.global_time = 0, 0, 0, 0
        self.level = [levels.level1(), levels.level2()]

        self.genetic_algorithm = genetic.GeneticAlgorithm(pool_size=pool)

    # Uses euclidean distance to return FORWARD, BACKWARD, LEFT, RIGHT euclidean distances
    def projection(self, x, y, orientation, scalar):
        # LHS Triangle
        d_orientation = (orientation + 50) % 360
        o_x = round(math.cos(math.radians(d_orientation)) * scalar, 3)
        o_y = round(math.sin(math.radians(d_orientation)) * scalar, 3)
        set_d1 = (x + o_x), \
                 (y - o_y)
        # RHS
        d_orientation = (orientation - 50) % 360
        o_x = round(math.cos(math.radians(d_orientation)) * scalar, 3)
        o_y = round(math.sin(math.radians(d_orientation)) * scalar, 3)
        set_d2 = (x + o_x), \
                 (y - o_y)
        return set_d1, set_d2

    def in_area(self, car, pad, x1, y1, x2, y2):
        p1 = Polygon([(car.position[0], car.position[1]),
                      (x1, y1),
                      ((x1 + x2) / 2, (y1 + y2) / 2)])
        p2 = Polygon([(car.position[0], car.position[1]),
                      (x2, y2),
                      ((x1 + x2) / 2, (y1 + y2) / 2)])
        r1 = Polygon([pad.rect.topleft, pad.rect.topright, pad.rect.bottomright, pad.rect.bottomleft])
        return p1.intersection(r1).area, p2.intersection(r1).area

    def calculate_closest_pad_by_direction(self, car):
        directions = [0 for i in range(0, 3)]
        for pad in self.pads:
            # Allows for change in spread
            scale = 30 * car.speed
            lhs, rhs = self.projection(car.position[0], car.position[1], car.orientation, scale)

            t_lhs, t_rhs = self.in_area(car, pad, lhs[0], lhs[1], rhs[0], rhs[1])
            if t_lhs > 0:
                directions[1] = t_lhs
            if t_rhs > 0:
                directions[2] = t_rhs
            if sum(directions) == (t_lhs + t_rhs) and t_lhs > 0 and t_rhs > 0:
                directions[0] = 1

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

    def run_level(self, noevolve=False, genes=None, level=None):

        if level is None:
            self.pads, self.trophies, self.car_pos, self.global_time = self.level[random.randint(0, len(self.level) - 1)]

        self.pad_group = pygame.sprite.RenderPlain(*self.pads)
        self.trophy_group = pygame.sprite.RenderPlain(*self.trophies)

        self.win_condition = None
        t0 = time.time()
        cars = list(self.genetic_algorithm.construct_cars(self.car_pos, genes=genes))
        car_group = pygame.sprite.RenderPlain(*cars)

        self.generation = self.small_font.render('Generation ' + str(self.current_generation), False, (255, 0, 0))

        # LOOP
        while True:

            for event in pygame.event.get():
                if not hasattr(event, 'key'): continue
                if event.key == K_ESCAPE:
                    print("Exiting AI.")
                    self.genetic_algorithm.display_report()
                    sys.exit(0)

            # Main iteration loop
            computation_time = time.time()
            for i in range(len(cars)):
                if cars[i].alive:
                    if self.win_condition:
                        pygame.mixer.music.stop()
                        self.genetic_algorithm.evaluate_performance(cars,
                                                                    (self.trophies[0].rect.x, self.trophies[0].rect.y), noevolve=noevolve)
                        self.run_level(genes=genes)
                    car_data = cars[i].get_car_data()
                    distances = self.calculate_closest_pad_by_direction(cars[i])
                    data = [
                            distances[0],
                            distances[1],
                            distances[2],
							cars[i].speed,
                    ]
                    predictions = cars[i].decision(data)
                    dir = predictions[:].argmax()
                    if dir == 0:
                        cars[i].k_up = 2
                    elif dir == 1:
                        cars[i].k_left = 5
                    elif dir == 2:
                        cars[i].k_right = -5
                    # Turn quite hard, wall approaching
                    elif dir == 3:
                        cars[i].k_left = 10
                    elif dir == 4:
                        cars[i].k_right = 10
                    elif dir == 5:
                        cars[i].k_down = 2

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
                    for car in cars:
                        if len(set(list(zip([history.X for history in car.history], [history.Y for history in car.history])))) > 10:
                            car.alive = False
                    self.genetic_algorithm.evaluate_performance(cars,
                                                                (self.trophies[0].rect.x, self.trophies[0].rect.y), noevolve=noevolve)
                    self.current_generation += 1
                    self.run_level(genes=genes)

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
                                                            (self.trophies[0].rect.x, self.trophies[0].rect.y), noevolve=noevolve)
                self.current_generation += 1
                self.run_level(genes=genes)

            trophy_collision = pygame.sprite.groupcollide(car_group, self.trophy_group, False, True)
            if trophy_collision != {}:
                for car in trophy_collision:
                    car.win = True
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

            # Remove bad cars
            for index, c in enumerate(cars):
                if not c.alive:
                    car_group.remove(c)
