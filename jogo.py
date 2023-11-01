import pygame
import random
import math


def inicializa():
    pygame.init()
    window = pygame.display.set_mode((400, 200), vsync=True, flags=pygame.SCALED)
    pygame.display.set_caption('233 CELSIUS')
    LARGURA, ALTURA = window.get_size() 

    fundos = {}

    for i in range(1, 16):  # Loop para carregar e redimensionar os fundos
        img = pygame.image.load(f'img/{i}.png')
        fundos[i] = pygame.transform.scale(img, (LARGURA, ALTURA))
    

    assets = {'valor': 1, 'rotação': 0 }
    assets['bruno'] = pygame.transform.scale(pygame.image.load('img/brunogrande.png'), (40, 40))
    assets['livro'] = pygame.transform.scale(pygame.image.load('img/livro.png'), (50, 50))
    assets['agua'] = pygame.transform.scale(pygame.image.load('img/agua.png'), (10, 10))
    assets['mangueira'] = pygame.transform.scale(pygame.image.load('img/mangueira.png'), (20, 20))
    assets['mira'] = pygame.transform.scale(pygame.image.load('img/mira.png'), (20, 20))
    assets['coracao'] = pygame.transform.scale(pygame.image.load('img/coracao.png'), (20, 20)) 

    state = {}
    bruno_largura, bruno_altura = assets['bruno'].get_size()
    state['bruno_pos'] = [(LARGURA - bruno_largura) / 2, (ALTURA - bruno_altura) / 2]
    state['bruno_vel'] = [0, 0]
    state['livros'] = []
    state['livros_vel'] = [0, 0]
    state['cima_baixo_esquerda_direita'] = 'nada'
    mangueira_largura, mangueira_altura = assets['mangueira'].get_size()
    state['mangueira_posicao'] = [(LARGURA - mangueira_largura) / 2, (ALTURA - mangueira_altura) / 2]
    state['agua'] = []
    state['espirra_agua'] = False  
    state['vidas'] = 5  # Inicializa o Bruno com 5 vidas

    return window, fundos, assets, state

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
    LARGURA, ALTURA = window.get_size()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
        if assets['valor'] == 15:
            if event.type == pygame.MOUSEBUTTONDOWN:
                state['espirra_agua'] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                state['espirra_agua'] = False
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if colisao_ponto_retangulo(x, y, 0, 0, LARGURA, ALTURA):
                    assets['valor'] += 1

    if assets['valor'] == 15:
        # Verifica colisão entre os livros e o Bruno
        bruno_rect = pygame.Rect(state['bruno_pos'][0], state['bruno_pos'][1], assets['bruno'].get_width(), assets['bruno'].get_height())
        for livro in state['livros']:
            livro_rect = pygame.Rect(livro['pos'][0], livro['pos'][1], assets['livro'].get_width(), assets['livro'].get_height())
            if bruno_rect.colliderect(livro_rect):
                state['vidas'] -= 1  # Remove uma vida se houver colisão
                state['livros'].remove(livro)  # Remove o livro que colidiu para não detectar a colisão novamente
        # Verifica se as vidas são 0 e emite um evento QUIT
        if state['vidas'] <= 0:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        # Chance de criar um novo livro
        if random.random() < 0.01:  # 2% de chance por quadro de adicionar um novo livro
            x, y = random.choice([(0, random.randint(0, ALTURA)), (LARGURA, random.randint(0, ALTURA)), (random.randint(0, LARGURA), 0), (random.randint(0, LARGURA), ALTURA)])
            dx, dy = state['bruno_pos'][0] - x, state['bruno_pos'][1] - y
            mag = math.sqrt(dx**2 + dy**2)
            dx /= mag
            dy /= mag
            speed = 1  # Velocidade do livro
            state['livros'].append({'pos': [x, y], 'vel': [dx * speed, dy * speed]})
            # Move cada livro
        for livro in state['livros']:
            livro['pos'][0] += livro['vel'][0]
            livro['pos'][1] += livro['vel'][1]

    mouse_x, mouse_y = pygame.mouse.get_pos()
    centro_x, centro_y = (state['bruno_pos'][0] + assets['bruno'].get_width() / 2, 
                          state['bruno_pos'][1] + assets['bruno'].get_height() / 2)
    rel_x, rel_y = mouse_x - centro_x, mouse_y - centro_y
    angulo = (180 / math.pi) * -math.atan2(rel_y, rel_x)
    assets['rotação'] = angulo

    distancia_centro = 25  # Distância entre Bruno e a mangueira
    state['mangueira_posicao'][0] = centro_x + distancia_centro * math.cos(math.radians(-angulo)) - assets['mangueira'].get_width()/2
    state['mangueira_posicao'][1] = centro_y + distancia_centro * math.sin(math.radians(-angulo)) - assets['mangueira'].get_height()/2

    if state.get('espirra_agua'):
        mouse_pos = pygame.mouse.get_pos()

        mangueira_ponta = (
            state['mangueira_posicao'][0] + assets['mangueira'].get_width() / 2,
            state['mangueira_posicao'][1] + assets['mangueira'].get_height() / 2
        )

        # Calcula o ângulo entre a ponta da mangueira e a posição do mouse ao clicar
        diff_x = mouse_pos[0] - mangueira_ponta[0]
        diff_y = mouse_pos[1] - mangueira_ponta[1]
        angulo = -math.degrees(math.atan2(diff_y, diff_x))

        assets['rotação'] = angulo
        
        state['agua'].append({
            'posicao': list(mangueira_ponta),
            'angulo': angulo
        })

    for part in state['agua']:
        speed = 5
        part['posicao'][0] += speed * math.cos(math.radians(-part['angulo']))
        part['posicao'][1] += speed * math.sin(math.radians(-part['angulo']))

        # Verifica colisões entre a água e os livros
        agua_rect = pygame.Rect(part['posicao'][0], part['posicao'][1], assets['agua'].get_width(), assets['agua'].get_height())
        livros_a_remover = []  # Lista para armazenar os livros que serão removidos
        for i, livro in enumerate(state['livros']):
            livro_rect = pygame.Rect(livro['pos'][0], livro['pos'][1], assets['livro'].get_width(), assets['livro'].get_height())
            if agua_rect.colliderect(livro_rect):  # Verifica se a água colide com o livro
                livros_a_remover.append(i)  # Adiciona o índice do livro à lista de remoção

        # Remove os livros que colidiram com a água
        for i in reversed(livros_a_remover):  # Use reversed para evitar problemas de índice durante a remoção
            del state['livros'][i]

    return True

def desenha(window, fundos, assets, state):
    window.fill((0, 0, 0))
    window.blit(fundos[assets['valor']], (0,0))

    for part in state['agua']:
        window.blit(assets['agua'], part['posicao'])

    if assets['valor'] == 15:
        window.blit(assets['bruno'], state['bruno_pos'])

        mangueira = assets['mangueira']
        mangueira_girada = pygame.transform.rotate(mangueira, assets['rotação'])

        # Calcula a nova posição para a mangueira rotacionada
        offset_x = state['mangueira_posicao'][0] - (mangueira_girada.get_width() - mangueira.get_width()) / 2
        offset_y = state['mangueira_posicao'][1] - (mangueira_girada.get_height() - mangueira.get_height()) / 2
        window.blit(mangueira_girada, (offset_x, offset_y))

        mira_pos = pygame.mouse.get_pos()  # Pega a posição do mouse
        window.blit(assets['mira'], (mira_pos[0]-assets['mira'].get_width()/2, mira_pos[1]-assets['mira'].get_height()/2))  # Centraliza a mira no mouse

        for livro in state['livros']:
            window.blit(assets['livro'], livro['pos'])

        for i in range(state['vidas']):
            window.blit(assets['coracao'], (10 + i * (assets['coracao'].get_width() + 5), 10))

    pygame.display.update()
    
    return window

def game_loop(window, fundos, assets, state):
    while recebe_eventos(window, fundos, assets, state):
        desenha(window, fundos, assets, state)

if __name__ == '__main__':
    w, f, a, s = inicializa()
    game_loop(w, f, a, s)

