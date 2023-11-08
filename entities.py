import pygame
import constants as c 
import math
import random


class Mangueira(pygame.sprite.Sprite):
    def __init__(self, jogo):
        super().__init__()
        self.jogo = jogo
        self.image = self.jogo.assets['mangueira']
        self.rect = self.image.get_rect()
        self.angulo = self.jogo.assets['rotacao']

    def atualiza(self):
        centro_x, centro_y = (self.jogo.state['bruno_pos'][0] + c.BRUNO_LARGURA / 2, 
                              self.jogo.state['bruno_pos'][1] + c.BRUNO_ALTURA / 2)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - centro_x, mouse_y - centro_y
        self.angulo = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        self.jogo.state['mangueira_posicao'][0] = centro_x + c.DISTANCIA_CENTRO_MANGUEIRA * math.cos(math.radians(-self.angulo)) - c.MANGUEIRA_LARGURA/2
        self.jogo.state['mangueira_posicao'][1] = centro_y + c.DISTANCIA_CENTRO_MANGUEIRA * math.sin(math.radians(-self.angulo)) - c.MANGUEIRA_ALTURA/2

    def desenha(self):
        mangueira_girada = pygame.transform.rotate(self.image, self.angulo)
        offset_x = self.jogo.state['mangueira_posicao'][0] - (mangueira_girada.get_width() - c.MANGUEIRA_LARGURA) / 2
        offset_y = self.jogo.state['mangueira_posicao'][1] - (mangueira_girada.get_height() - c.MANGUEIRA_ALTURA) / 2
        self.jogo.window.blit(mangueira_girada, (offset_x, offset_y))


class Livro(pygame.sprite.Sprite):
    def __init__(self, jogo, chance_geracao, livro_vel):
        super().__init__()
        self.jogo = jogo
        self.image = jogo.assets['livro']
        self.vel = livro_vel
        self.vida = self.jogo.state['livro_vida']
        self.livros = self.jogo.state['livros']
        self.bruno_pos = self.jogo.state['bruno_pos']
        self.livro_chance_geracao = chance_geracao

    def chance_geracao(self):
        if random.random() < self.livro_chance_geracao:
            x, y = random.choice([(0, random.randint(0, c.ALTURA)), (c.LARGURA, random.randint(0, c.ALTURA)), (random.randint(0, c.LARGURA), 0), (random.randint(0, c.LARGURA), c.ALTURA)])
            dx, dy = self.bruno_pos[0] - x, self.bruno_pos[1] - y
            mag = math.sqrt(dx**2 + dy**2)
            dx /= mag
            dy /= mag
            self.livros.append({'pos': [x, y], 'vel': [dx * self.vel, dy * self.vel], 'vida': self.vida})

    def atualiza(self):
        self.chance_geracao()
        for livro in self.livros:
            livro['pos'][0] += livro['vel'][0]
            livro['pos'][1] += livro['vel'][1]


    def desenha(self):
        for livro in self.livros:
            self.jogo.window.blit(self.image, livro['pos'])

class BarraVida(pygame.sprite.Sprite):
    def __init__(self, jogo, livros_atingidos, muda_nivel, tela):
        super().__init__()
        self.jogo = jogo
        self.livro = self.jogo.state['livros']
        self.livro_vida_total =  self.jogo.state['livro_vida']
        self.agua = self.jogo.state['agua']
        self.livros_atingidos = livros_atingidos
        self.muda_nivel = muda_nivel
        self.tela = tela

    def atualiza(self):
        for part in self.agua:
            agua_rect = pygame.Rect(part['posicao'][0], part['posicao'][1], c.AGUA_LARGURA, c.AGUA_ALTURA)
            livros_a_remover = [] 
            aguas_a_remover = []  
            for i, livro in enumerate(self.livro):
                livro_rect = pygame.Rect(livro['pos'][0], livro['pos'][1], c.LIVRO_LARGURA, c.LIVRO_ALTURA)
                if agua_rect.colliderect(livro_rect): 
                    livro['vida'] -= c.LIVRO_DANO  
                    aguas_a_remover.append(part) 
                    if livro['vida'] <= 0:  
                        self.livros_atingidos += 1 
                        self.jogo.state['livros_atingidos'] = self.livros_atingidos 
                        livros_a_remover.append(i)

            for i in reversed(livros_a_remover): 
                del self.livro[i]

            for agua in aguas_a_remover:
                self.agua.remove(agua)

        if self.livros_atingidos == self.muda_nivel:
            self.jogo.muda_tela(self.tela(self.jogo))

    def desenha(self):
        for livro in self.livro:
            posicao_barra_vida = (livro['pos'][0], livro['pos'][1] - 10)  
            vida_atual = livro['vida'] / self.livro_vida_total
            pygame.draw.rect(self.jogo.window, c.VERMELHO, (posicao_barra_vida[0], posicao_barra_vida[1], c.BARRA_VIDA_LARGURA, c.BARRA_VIDA_ALTURA))
            pygame.draw.rect(self.jogo.window, c.VERDE, (posicao_barra_vida[0], posicao_barra_vida[1], c.BARRA_VIDA_LARGURA * vida_atual, c.BARRA_VIDA_ALTURA))
        
        font = pygame.font.SysFont(None, 36)
        text = font.render(f":{self.livros_atingidos}", True, (c.BRANCO))
        text_width = text.get_width()
        self.jogo.window.blit(text, (c.LARGURA - text_width - 10, 10))
        self.jogo.window.blit(self.jogo.assets['livro'], (c.LARGURA - c.LIVRO_LARGURA - text_width, 0))


class Agua(pygame.sprite.Sprite):
    def __init__(self, jogo):
        super().__init__()
        self.jogo = jogo
        self.espirra_agua = self.jogo.state['espirra_agua']
        self.agua_atual = self.jogo.state['agua_atual']
        self.mangueira_pos = self.jogo.state['mangueira_posicao']
        self.angulo =  self.jogo.assets['rotacao']
        self.agua = self.jogo.state['agua']
        self.image = self.jogo.assets['agua']

    def atualiza(self):

        if self.jogo.state.get('espirra_agua') and self.jogo.state['agua_atual'] > 0:
            mouse_pos = pygame.mouse.get_pos()

            mangueira_ponta = (
                self.mangueira_pos[0] + c.MANGUEIRA_LARGURA / 2,
                self.mangueira_pos[1] + c.MANGUEIRA_ALTURA / 2
            )

            diff_x = mouse_pos[0] - mangueira_ponta[0]
            diff_y = mouse_pos[1] - mangueira_ponta[1]
            angulo = -math.degrees(math.atan2(diff_y, diff_x))

            self.angulo = angulo
         
            self.agua.append({
                'posicao': list(mangueira_ponta),
                'angulo': angulo
            }) 

            self.jogo.state['agua_atual'] -= c.AGUA_CONSUMO

        for part in self.agua:
            part['posicao'][0] += c.AGUA_VEL * math.cos(math.radians(-part['angulo']))
            part['posicao'][1] += c.AGUA_VEL * math.sin(math.radians(-part['angulo']))

    def desenha(self):
        for part in self.agua:
            self.jogo.window.blit(self.image, part['posicao'])

class BarraAgua(pygame.sprite.Sprite):
    def __init__(self, jogo):
        super().__init__()
        self.jogo = jogo
        self.agua_atual = self.jogo.state['agua_atual']
        self.agua_max = self.jogo.state['agua_max']
    
    def atualiza(self):

        if not self.jogo.state.get('espirra_agua') and self.jogo.state['agua_atual'] < self.agua_max:
            self.jogo.state['agua_atual'] += 0.5
            if self.jogo.state['agua_atual'] > self.agua_max:
                self.jogo.state['agua_atual'] = self.agua_max
        

    def desenha(self):
        posicao_barra_agua = ((c.LARGURA - c.BARRA_AGUA_LARGURA) / 2, c.ALTURA - c.BARRA_AGUA_ALTURA - 3)
        agua_atual = self.jogo.state['agua_atual']/ self.agua_max
        pygame.draw.rect(self.jogo.window, c.CINZA, (posicao_barra_agua[0], posicao_barra_agua[1], c.BARRA_AGUA_LARGURA, c.BARRA_AGUA_ALTURA))
        pygame.draw.rect(self.jogo.window, c.AZUL, (posicao_barra_agua[0], posicao_barra_agua[1], c.BARRA_AGUA_LARGURA * agua_atual, c.BARRA_AGUA_ALTURA))

class Coracao(pygame.sprite.Sprite):
    def __init__(self, jogo, vidas, vida_esgotada):
        super().__init__()
        self.jogo = jogo
        self.vidas = vidas
        self.vida_esgotada = vida_esgotada

    def atualiza(self):
        bruno_rect = pygame.Rect(self.jogo.state['bruno_pos'][0], self.jogo.state['bruno_pos'][1], c.BRUNO_LARGURA, c.BRUNO_LARGURA)
        for livro in self.jogo.state['livros']:
            livro_rect = pygame.Rect(livro['pos'][0], livro['pos'][1], c.LIVRO_LARGURA, c.LIVRO_ALTURA)
            if bruno_rect.colliderect(livro_rect):
                self.vidas -= 1 
                self.jogo.state['vidas'] = self.vidas
                self.jogo.state['livros'].remove(livro) 
        if self.vidas <= 0:
            self.vida_esgotada = True

    def desenha(self):
        for i in range(self.vidas):
            self.jogo.window.blit(self.jogo.assets['coracao'], (10 + i * (c.CORACAO_LARGURA + 5), 10))
