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
        PadSprite('images/vertical_pads.png', (0, 100)),
        PadSprite('images/vertical_pads.png', (0, 200)),
        PadSprite('images/vertical_pads.png', (0, 400)),
        PadSprite('images/vertical_pads.png', (1024, 100)),
        PadSprite('images/vertical_pads.png', (1024, 550)),
        PadSprite('images/vertical_pads.png', (824, 768)),
        PadSprite('images/vertical_pads.png', (824, 368)),
        PadSprite('images/vertical_pads.png', (210, 375)),
        PadSprite('images/vertical_pads.png', (824, 368)),
        PadSprite('images/race_pads.png', (900, 0)),
        PadSprite('images/race_pads.png', (724, 0)),
        PadSprite('images/race_pads.png', (524, 0)),
        PadSprite('images/race_pads.png', (224, 0)),
        PadSprite('images/race_pads.png', (1024, 768)),
        PadSprite('images/race_pads.png', (624, 768)),
        PadSprite('images/race_pads.png', (224, 768)),
        PadSprite('images/race_pads.png', (450, 130)),
        PadSprite('images/race_pads.png', (550, 130)),
        PadSprite('images/small_horizontal.png', (600, 615)),
        PadSprite('images/small_horizontal.png', (350, 615)),
        PadSprite('images/small_horizontal.png', (470, 270)),
        PadSprite('images/small_vertical.png', (600, 390)),
        PadSprite('images/small_vertical.png', (350, 390)),

        PadSprite('images/vertical_pads.png', (0,250)),
        PadSprite('images/vertical_pads.png', (0, 525)),
        PadSprite('images/vertical_pads.png', (1024, 250)),
        PadSprite('images/vertical_pads.png', (1024, 525)),
        PadSprite('images/race_pads.png', (250, 0)),
        PadSprite('images/race_pads.png', (760, 0)),
        PadSprite('images/race_pads.png', (500, 0)),
        PadSprite('images/race_pads.png', (250, 768)),
        PadSprite('images/race_pads.png', (760, 768)),
        PadSprite('images/race_pads.png', (500, 768))
    ]

    trophies = [Trophy((450, 320))]

    return pads, trophies, (970, 730), 60

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

        PadSprite('images/vertical_pads.png', (0,250)),
        PadSprite('images/vertical_pads.png', (0, 525)),
        PadSprite('images/vertical_pads.png', (1024, 250)),
        PadSprite('images/vertical_pads.png', (1024, 525)),
        PadSprite('images/race_pads.png', (250, 0)),
        PadSprite('images/race_pads.png', (760, 0)),
        PadSprite('images/race_pads.png', (500, 0)),
        PadSprite('images/race_pads.png', (250, 768)),
        PadSprite('images/race_pads.png', (760, 768)),
        PadSprite('images/race_pads.png', (500, 768))
    ]

    trophies = [Trophy((450, 320))]

    return pads, trophies, (30, 730), 60
