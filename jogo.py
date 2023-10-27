import pygame
import random



def inicializa():
    pygame.init()
    window = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('233 CELSIUS')
    fundos = {}
    fundos[1] = pygame.image.load('img/1.png')
    fundos[2] = pygame.image.load('img/2.png')
    fundos[3] = pygame.image.load('img/3.png')
    fundos[4] = pygame.image.load('img/4.png')
    fundos[5] = pygame.image.load('img/5.png')
    fundos[6] = pygame.image.load('img/6.png')
    fundos[7] = pygame.image.load('img/7.png')
    fundos[8] = pygame.image.load('img/8.png')
    fundos[9] = pygame.image.load('img/9.png')
    fundos[10] = pygame.image.load('img/10.png')
    fundos[11] = pygame.image.load('img/11.png')
    fundos[12] = pygame.image.load('img/12.png')
    fundos[13] = pygame.image.load('img/13.png')
    fundos[14] = pygame.image.load('img/14.png')
    assets ={'valor' : 1}



    return window, fundos, assets

def colisao_ponto_retangulo(ponto_x, ponto_y, rect_x, rect_y, rect_w, rect_h):
    if (
    rect_x <= ponto_x and 
    ponto_x <= rect_x + rect_w and 
    rect_y <= ponto_y and 
    ponto_y <= rect_y + rect_h
):
        return True
    else:
        return False


def recebe_eventos(window, fundos, assets):
    game = True
    e = 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.MOUSEBUTTONDOWN:

                x, y = pygame.mouse.get_pos()
                if colisao_ponto_retangulo(x, y, 0, 0, 1920, 1080) == True:
                    assets['valor']+=1





        
    return game


def desenha(window, fundos, assets):
    window.fill((0, 0, 0))
    window.blit(fundos[assets['valor']], (0,0))

    pygame.display.update()
    
    return window

def game_loop(window, fundos, assets):
    game = recebe_eventos(window, fundos, assets )
    while game:

        desenha(window, fundos, assets)


        game = recebe_eventos(window, fundos, assets )
    pygame.QUIT()



if __name__ == '__main__':
    w, f, a = inicializa()
    game_loop(w, f, a)

