import pygame
import constants as c
import math
import random

class Jogo:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((c.LARGURA, c.ALTURA), vsync=True, flags=pygame.SCALED)
        pygame.display.set_caption('233 CELSIUS')
        self.carrega_recursos()
        self.tela_atual = TelaInicial(self)

    def carrega_recursos(self):
        self.assets = {
            'bruno': pygame.transform.scale(pygame.image.load('img/brunogrande.png'), (c.BRUNO_LARGURA, c.BRUNO_ALTURA)),
            'livro': pygame.transform.scale(pygame.image.load('img/livro.png'), (c.LIVRO_LARGURA, c.LIVRO_ALTURA)),
            'agua': pygame.transform.scale(pygame.image.load('img/agua.png'), (c.AGUA_LARGURA, c.AGUA_ALTURA)),
            'mangueira': pygame.transform.scale(pygame.image.load('img/mangueira.png'), (c.MANGUEIRA_LARGURA, c.MANGUEIRA_ALTURA)),
            'mira': pygame.transform.scale(pygame.image.load('img/mira.png'), (c.MIRA_LARGURA, c.MANGUEIRA_ALTURA)),
            'coracao': pygame.transform.scale(pygame.image.load('img/coracao.png'), (c.CORACAO_LARGURA, c.CORACAO_ALTURA)),
            'valor': 1, 
            'rotacao': 0,
            'fonte': pygame.font.Font(pygame.font.get_default_font(), 20)
        }

def inicializa():
    pygame.init()
    window = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('233 CELSIUS')
    fundos = {}
    personagens = {}
    pygame.mixer.music.load('musica.mp3')
    pygame.mixer.music.play(loops=-1)
    
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

        self.state = {
            'bruno_pos': [(c.LARGURA - c.BRUNO_LARGURA) / 2, (c.ALTURA - c.BRUNO_ALTURA) / 2],
            'livros': [],
            'livro_vida': 100,
            'livros_atingidos': 0,
            'cima_baixo_esquerda_direita': 'nada',
            'mangueira_posicao': [(c.LARGURA - c.MANGUEIRA_LARGURA) / 2, (c.ALTURA - c.MANGUEIRA_ALTURA) / 2],
            'agua': [],
            'espirra_agua': False,
            'agua_atual': 100,
            'agua_max': 100,
            'vidas': 5
        }

    def muda_tela(self, tela):
        self.tela_atual = tela

    def run(self):
        while self.tela_atual.executa():
            pass
        pygame.quit()

class TelaBase:
    def __init__(self, jogo):
        self.jogo = jogo

    def executa(self):
        pass

    def desenha(self):
        pass

    def atualiza(self):
        pass

class TelaInicial(TelaBase):
    def colisao_ponto_retangulo(self, ponto_x, ponto_y, rect_x, rect_y, rect_w, rect_h):
        if (
        rect_x <= ponto_x and 
        ponto_x <= rect_x + rect_w and 
        rect_y <= ponto_y and 
        ponto_y <= rect_y + rect_h
    ):
            return True
        else:
            return False

    def executa(self):
        self.desenha()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if self.colisao_ponto_retangulo(x, y, 0, 0, c.LARGURA, c.ALTURA):
                    self.jogo.assets['valor'] += 1
            if self.jogo.assets['valor'] == c.TELA_JOGO:
                self.jogo.muda_tela(TelaJogo(self.jogo))
        return True

    def desenha(self):
        self.jogo.window.fill((0, 0, 0))
        fundo = self.jogo.fundos[self.jogo.assets['valor']]
        self.jogo.window.blit(fundo, (0, 0))
        pygame.display.update()

class TelaJogo(TelaBase):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.fundo = self.jogo.fundos[15]
        self.mangueira = Mangueira(jogo)
        self.livro = Livro(jogo)
        self.barra_vida = BarraVida(jogo)
        self.agua = Agua(jogo)
        self.bruno = self.jogo.assets['bruno']

    def executa(self):
        self.atualiza()
        self.desenha()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False 
        return True
    
    def atualiza(self):
        self.mangueira.atualiza()
        self.livro.atualiza()
        self.barra_vida.atualiza()
        self.agua.atualiza()

    def desenha(self):
        self.jogo.window.fill((0, 0, 0))
        self.jogo.window.blit(self.fundo, (0,0))
        self.jogo.window.blit(self.bruno, self.jogo.state['bruno_pos'])
        self.mangueira.desenha()
        self.livro.desenha()
        self.barra_vida.desenha()
        self.agua.desenha()

        pygame.display.update()


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
    def __init__(self, jogo):
        super().__init__()
        self.jogo = jogo
        self.image = jogo.assets['livro']
        self.vel = c.LIVRO_VEL
        self.vida = self.jogo.state['livro_vida']
        self.livros = self.jogo.state['livros']
        self.bruno_pos = self.jogo.state['bruno_pos']

    def chance_geracao(self):
        if random.random() < c.LIVRO_CHANCE_GERACAO:
            x, y = random.choice([(0, random.randint(0, c.ALTURA)), (c.LARGURA, random.randint(0, c.ALTURA)), (random.randint(0, c.LARGURA), 0), (random.randint(0, c.LARGURA), c.ALTURA)])
            dx, dy = self.bruno_pos[0] - x, self.bruno_pos[1] - y
            mag = math.sqrt(dx**2 + dy**2)
            dx /= mag
            dy /= mag
            self.livros.append({'pos': [x, y], 'vel': [dx * c.LIVRO_VEL, dy * c.LIVRO_VEL], 'vida': self.vida})

    def atualiza(self):
        self.chance_geracao()
        for livro in self.livros:
            livro['pos'][0] += livro['vel'][0]
            livro['pos'][1] += livro['vel'][1]


    def desenha(self):
        for livro in self.livros:
            self.jogo.window.blit(self.image, livro['pos'])

class BarraVida(pygame.sprite.Sprite):
    def __init__(self, jogo):
        super().__init__()
        self.jogo = jogo
        self.livro = self.jogo.state['livros']
        self.livro_vida_total =  self.jogo.state['livro_vida']
        self.agua = self.jogo.state['agua']
        self.livros_atingidos = self.jogo.state['livros_atingidos']

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
                        livros_a_remover.append(i)  

            for i in reversed(livros_a_remover):  
                del self.livro[i]

            for agua in aguas_a_remover:
                self.agua.remove(agua)


    def desenha(self):
        for livro in self.livro:
            posicao_barra_vida = (livro['pos'][0], livro['pos'][1] - 10) 
            vida_atual = livro['vida'] / self.livro_vida_total
            pygame.draw.rect(self.jogo.window, c.VERMELHO, (posicao_barra_vida[0], posicao_barra_vida[1], c.BARRA_VIDA_LARGURA, c.BARRA_VIDA_ALTURA))
            pygame.draw.rect(self.jogo.window, c.VERDE, (posicao_barra_vida[0], posicao_barra_vida[1], c.BARRA_VIDA_LARGURA * vida_atual, c.BARRA_VIDA_ALTURA))
    
if __name__ == '__main__':
    jogo = Jogo()
    jogo.run() 

