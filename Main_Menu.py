import pygame, math, sys, time, main
from pygame.locals import *

import argparse

# Process any arguments passed in through command line
parse = argparse.ArgumentParser()
parse.add_argument("-f", "--file", help="File that contains any number of gene sets, must be in pre-existing list notation.")
parse.add_argument("-ne", "--noevolve", action="store_true", help="Disables genetic evolution.")
parse.add_argument("-p", "--pool", help="Overrides how many cars are spawned.")
args = vars(parse.parse_args())

pygame.init()
screen = pygame.display.set_mode((1024, 768))
while 1:
    screen.fill((0,0,0))
    for event in pygame.event.get():
                if not hasattr(event, 'key'): continue
                if event.key == K_SPACE:
                    genes = None
                    if args["file"]:
                        with open(args["file"], "r") as f:
                            # Remove first character '[' and last two ']\n'
                            # Future would allow multiple gene sets to be placed within text file for
                            # multi evaluation
                            gene_list = f.readlines()[0][1:-2]
                            genes = [float(i) for i in gene_list.split(",")]
                    if args["pool"] is None:
                        main_game = main.Main()
                    else:
                        main_game = main.Main(pool=int(args["pool"]))
                    main_game.run_level(noevolve=args["noevolve"], genes=genes)
                elif event.key == K_ESCAPE: sys.exit(0)  
    img = pygame.image.load("images/main_menu_image.png")
    screen.blit(img,(0,0))
    pygame.display.flip()
