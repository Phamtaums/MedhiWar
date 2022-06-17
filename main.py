import pygame
pygame.init()

from game import Game

if __name__ == '__main__':                # chargement de la base du module
    pygame.init()                         # chargement des composants
    game = Game()                         # instancié la classe game
    game.run()                          # exécution du programme