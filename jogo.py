import pygame
import random



def inicializa():
    pygame.init()
    window = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('233 CELSIUS')
    return window




def recebe_eventos():
    game = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False




        
    return game


def desenha(window):
    window.fill((0, 0, 0))
    pygame.display.update()
    
    return window

def game_loop(window):
    game = recebe_eventos()
    while game:

        desenha(window)


        game = recebe_eventos()
    pygame.QUIT()



if __name__ == '__main__':
    w = inicializa()
    game_loop(w)

