import pygame
import constants as c 

from states import GameState
from entities import BarraVida, Coracao, Mangueira, Livro, Agua
from screens import TelaBase, TelaInicial, TelaJogo, TelaGameOver, TelaNivel2, TelaNivel3

class Jogo:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((c.LARGURA, c.ALTURA), vsync=True, flags=pygame.SCALED)
        pygame.display.set_caption('233 CELSIUS')
        self.carrega_recursos()
        self.tela_atual = TelaInicial(self)

    def carrega_recursos(self):
        self.assets = self.carregar_assets()
        self.fundos = self.carregar_fundos()
        self.state = self.criar_estado_inicial()

    def carregar_assets(self):
        assets = {
            'bruno': pygame.transform.scale(pygame.image.load('img/brunogrande.png'), (c.BRUNO_LARGURA, c.BRUNO_ALTURA)),
            'livro': pygame.transform.scale(pygame.image.load('img/livro.png'), (c.LIVRO_LARGURA, c.LIVRO_ALTURA)),
            'agua': pygame.transform.scale(pygame.image.load('img/agua.png'), (c.AGUA_LARGURA, c.AGUA_ALTURA)),
            'mangueira': pygame.transform.scale(pygame.image.load('img/mangueira.png'), (c.MANGUEIRA_LARGURA, c.MANGUEIRA_ALTURA)),
            'mira': pygame.transform.scale(pygame.image.load('img/mira.png'), (c.MIRA_LARGURA, c.MANGUEIRA_ALTURA)),
            'coracao': pygame.transform.scale(pygame.image.load('img/coracao.png'), (c.CORACAO_LARGURA, c.CORACAO_ALTURA)),
            'valor': 1, 
            'rotacao': 0,
            'fonte': pygame.font.Font(pygame.font.get_default_font(), 20),
            'som': pygame.mixer.music.load('musica.mp3'),
            'play': pygame.mixer.music.play(loops=-1)
        }

        return assets


    def carregar_fundos(self):    
        fundos = {}
        for i in range(1, 21):
            img = pygame.image.load(f'img/{i}.png')
            fundos[i] = pygame.transform.scale(img, (c.LARGURA, c.ALTURA))
        return fundos
    
    def criar_estado_inicial(self):
        state = {
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
            'vidas': 5,
            'livro_chance_geracao': c.LIVRO_CHANCE_GERACAO_1
        }
    
        return state
    

    def muda_tela(self, tela):
        self.tela_atual = tela
    
    def run(self):
        while self.tela_atual.executa():
            pass
        pygame.quit()


if __name__ == '__main__':
    jogo = Jogo()
    jogo.run() 