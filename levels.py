import pygame

"""
    levels.py
    Houses all possible levels for the game to choose from.

    Selection occurs by invoking the selected level
    and by having a return tuple of (pad_sprite, trophies, car[x,y]).

    Must still be rendered into the main game.
"""

class PadSprite(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super(PadSprite, self).__init__()
        self.normal = pygame.image.load(image)
        self.hit = pygame.image.load('images/collision.png')
        self.rect = pygame.Rect(self.normal.get_rect())
        self.rect.center = position

    def update(self, hit_list):
        if self in hit_list:
            self.image = self.hit
        else:
            self.image = self.normal

class Trophy(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/trophy.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def level1():
    pads = [
        PadSprite('images/race_pads.png', (0,10)),
        PadSprite('images/race_pads.png', (600, 10)),
        PadSprite('images/race_pads.png', (1100, 10)),
        PadSprite('images/race_pads.png', (100, 150)),
        PadSprite('images/race_pads.png', (600, 150)),
        PadSprite('images/race_pads.png', (100, 300)),
        PadSprite('images/race_pads.png', (800, 300)),
        PadSprite('images/race_pads.png', (400, 450)),
        PadSprite('images/race_pads.png', (700, 450)),
        PadSprite('images/race_pads.png', (200, 600)),
        PadSprite('images/race_pads.png', (900, 600)),
        PadSprite('images/race_pads.png', (400, 750)),
        PadSprite('images/race_pads.png', (800, 750))
    ]

    trophies = [Trophy((285, 0))]

    return pads, trophies, (10, 730)

def level2():
    pads = [
        PadSprite('images/vertical_pads.png', (0, 100)),
        PadSprite('images/vertical_pads.png', (0, 200)),
        PadSprite('images/vertical_pads.png', (0, 400)),
        PadSprite('images/vertical_pads.png', (1024, 100)),
        PadSprite('images/vertical_pads.png', (1024, 550)),
        PadSprite('images/vertical_pads.png', (200, 768)),
        PadSprite('images/vertical_pads.png', (200, 368)),
        PadSprite('images/vertical_pads.png', (800, 375)),
        PadSprite('images/vertical_pads.png', (200, 368)),
        PadSprite('images/race_pads.png', (60, 0)),
        PadSprite('images/race_pads.png', (300, 0)),
        PadSprite('images/race_pads.png', (700, 0)),
        PadSprite('images/race_pads.png', (900, 0)),
        PadSprite('images/race_pads.png', (1024, 768)),
        PadSprite('images/race_pads.png', (624, 768)),
        PadSprite('images/race_pads.png', (224, 768)),
        PadSprite('images/race_pads.png', (450, 130)),
        PadSprite('images/race_pads.png', (550, 130)),
        PadSprite('images/small_horizontal.png', (670, 615)),
        PadSprite('images/small_horizontal.png', (470, 615)),
        PadSprite('images/small_horizontal.png', (470, 270)),
        PadSprite('images/small_vertical.png', (350, 490)),
        PadSprite('images/small_vertical.png', (350, 390)),
        PadSprite('images/small_vertical.png', (600, 390)),
    ]

    trophies = [Trophy((450, 320))]

    return pads, trophies, (30, 730)

def level3():
    pads = [
        PadSprite('images/small_vertical.png', (0, 550)),
        PadSprite('images/small_vertical.png', (0, 390)),
        PadSprite('images/small_vertical.png', (0, 190)),
        PadSprite('images/small_vertical.png', (0, 90)),
        PadSprite('images/small_vertical.png', (100, -100)),
        PadSprite('images/small_vertical.png', (100, 290)),
        PadSprite('images/small_vertical.png', (100, 390)),
        PadSprite('images/small_vertical.png', (100, 490)),
        PadSprite('images/small_vertical.png', (200, 590)),
        PadSprite('images/small_vertical.png', (200, 290)),
        PadSprite('images/small_vertical.png', (200, 690)),
        PadSprite('images/small_vertical.png', (300, 590)),
        PadSprite('images/small_vertical.png', (300, 290)),
        PadSprite('images/small_vertical.png', (400, 535)),
        PadSprite('images/small_vertical.png', (400, 225)),
        PadSprite('images/small_vertical.png', (470, 490)),
        PadSprite('images/small_vertical.png', (600, 690)),
        PadSprite('images/small_vertical.png', (600, 290)),
        PadSprite('images/small_vertical.png', (600, 190)),
        PadSprite('images/small_vertical.png', (700, 690)),
        PadSprite('images/small_vertical.png', (700, 290)),
        PadSprite('images/small_vertical.png', (800, 690)),
        PadSprite('images/small_vertical.png', (800, 290)),
        PadSprite('images/small_vertical.png', (900, -50)),
        PadSprite('images/small_vertical.png', (1000, 690)),
        PadSprite('images/small_vertical.png', (1000, 290)),
        PadSprite('images/race_pads.png', (338, 170)),
        PadSprite('images/race_pads.png', (600, 170)),
    ]

    trophies = [Trophy((450, 320))]

    return pads, trophies, (30, 730)