import pygame
import random



def inicializa():
    pygame.init()
    window = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('233 CELSIUS')
    fundos = {}
    personagens = {}
    
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
    fundos[15] = pygame.image.load('img/15.png')
    assets ={'valor' : 1, 'rotação': 0 }
    assets['bruno'] = pygame.image.load('img/brunogrande.png')
    assets['livro'] = pygame.image.load('img/livro.png')
    state = {}
    state['player_posicao'] = [850, 400]
    state['player_velocidade'] = [0, 0]
    state['livros'] = []
    state['livrosvelocidade'] = [0, 0]
    state['cima_baixo_esquerda_direita'] = 'nada'



    return window, fundos, assets, personagens, state

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


def recebe_eventos(window, fundos, assets, state):
    game = True
    e = 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.MOUSEBUTTONDOWN:

                x, y = pygame.mouse.get_pos()
                if assets['valor'] == 15:
                    assets['valor'] = 15
                else:
                    if colisao_ponto_retangulo(x, y, 0, 0, 1920, 1080) == True:
                        assets['valor']+=1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                state['player_velocidade'][0] -= 2
                assets['rotação'] = 270
                state['cima_baixo_esquerda_direita'] = 'esquerda'
            elif event.key == pygame.K_RIGHT:
                state['player_velocidade'][0] += 2
                assets['rotação'] = 90
                state['cima_baixo_esquerda_direita'] = 'direita'
            elif event.key == pygame.K_UP:
                state['player_velocidade'][1] -= 2
                assets['rotação'] = 180
                state['cima_baixo_esquerda_direita'] = 'cima'
            elif event.key == pygame.K_DOWN:
                state['player_velocidade'][1] += 2
                assets['rotação'] = 0
                state['cima_baixo_esquerda_direita'] = 'baixo'
            elif event.key == pygame.K_SPACE:
                livro_x = state['player_posicao'][0] + 45
                livro_y = state['player_posicao'][1] - 20
                state['livros'].append([livro_x, livro_y])
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                state['player_velocidade'][0] += 2
                assets['rotação'] = 270
                state['cima_baixo_esquerda_direita'] = 'esquerda'
            elif event.key == pygame.K_RIGHT:
                state['player_velocidade'][0] -= 2
                assets['rotação'] = 90
                state['cima_baixo_esquerda_direita'] = 'direita'
            elif event.key == pygame.K_UP:
                state['player_velocidade'][1] += 2
                assets['rotação'] = 180
                state['cima_baixo_esquerda_direita'] = 'cima'
            elif event.key == pygame.K_DOWN:
                state['player_velocidade'][1] -= 2
                assets['rotação'] = 0
                state['cima_baixo_esquerda_direita'] = 'baixo'






        
    return game


def desenha(window, fundos, assets, state):
    window.fill((0, 0, 0))
    window.blit(fundos[assets['valor']], (0,0))
    if fundos[assets['valor']] == fundos[15]:
        player =pygame.transform.scale(assets['bruno'], (200, 200))
        player = pygame.transform.rotate(player, assets['rotação'])
        window.blit(player, state['player_posicao'])
        for livro in state['livros']:
            livropequeno = pygame.transform.scale(assets['livro'], (50, 50))
            livropequeno = pygame.transform.rotate(livropequeno, assets['rotação'])
            window.blit(livropequeno, (livro[0], livro[1]))

    pygame.display.update()
    
    return window

def game_loop(window, fundos, assets, state):
    game = recebe_eventos(window, fundos, assets, state )
    while game:


        state['player_posicao'][0] += state['player_velocidade'][0]
        state['player_posicao'][1] += state['player_velocidade'][1]

        for livro in state['livros']:
            if state['cima_baixo_esquerda_direita'] == 'cima':
                livro[1] -= 2
            elif state['cima_baixo_esquerda_direita'] == 'baixo':
                livro[1] += 2
            elif state['cima_baixo_esquerda_direita'] == 'esquerda':
                livro[0] -= 2
            elif state['cima_baixo_esquerda_direita'] == 'direita':
                livro[0] += 2

            if livro[0] < 0 or livro[0] > 1920 or livro[1] < 0 or livro[1] > 1080:
                state['livros'].remove(livro)

        desenha(window, fundos, assets, state)


        game = recebe_eventos(window, fundos, assets, state )
    pygame.QUIT()



if __name__ == '__main__':
    w, f, a, p, s = inicializa()
    game_loop(w, f, a, s)

