import pygame
import constants as c 

from states import GameState
from entities import BarraVida, Coracao, Mangueira, Livro, Agua, BarraAgua

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

class TelaGameOver(TelaBase):
    def executa(self):
        self.desenha()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                self.jogo.muda_tela(TelaJogo(self.jogo))
        return True

    def desenha(self):
        self.jogo.window.fill((0, 0, 0))
        fundo = self.jogo.fundos[16]
        self.jogo.window.blit(fundo, (0, 0))

        pygame.display.update()


class TelaJogo(TelaBase):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.fundo = self.jogo.fundos[15]
        self.mangueira = Mangueira(jogo)
        self.livro = Livro(jogo, c.LIVRO_CHANCE_GERACAO_1, c.LIVRO_VEL1)
        self.barra_vida = BarraVida(jogo, 0, 5, TelaNivel2)
        self.agua = Agua(jogo)
        self.bruno = self.jogo.assets['bruno']
        self.game_state = GameState(jogo)
        self.barra_agua = BarraAgua(jogo)
        self.coracao = Coracao(jogo, 5, False)
        self.mira = self.jogo.assets['mira']

    def executa(self):
        self.coracao.atualiza()
        if self.coracao.vida_esgotada:
            self.jogo.muda_tela(TelaGameOver(self.jogo))        
        if not self.game_state.atualiza_estado():
            return False
        self.atualiza()
        self.desenha()

        return True
    
    def atualiza(self):
        self.mangueira.atualiza()
        self.livro.atualiza()
        self.barra_vida.atualiza()
        self.agua.atualiza()
        self.barra_agua.atualiza()
        self.coracao.atualiza()

    def desenha(self):
        self.jogo.window.fill((0, 0, 0))
        self.jogo.window.blit(self.fundo, (0,0))
        self.jogo.window.blit(self.bruno, self.jogo.state['bruno_pos'])
        self.mangueira.desenha()
        self.livro.desenha()
        self.barra_vida.desenha()
        self.agua.desenha()
        self.barra_agua.desenha()
        self.coracao.desenha()

        mira_pos = pygame.mouse.get_pos()
        self.jogo.window.blit(self.mira, (mira_pos[0]-c.MIRA_LARGURA/2, mira_pos[1]-c.MIRA_ALTURA/2))

        pygame.display.update()

class TelaNivel2(TelaJogo):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.fundo = self.jogo.fundos[17]
        
        self.livro = Livro(jogo, c.LIVRO_CHANCE_GERACAO_2, c.LIVRO_VEL2)

        self.barra_vida = BarraVida(jogo, self.jogo.state['livros_atingidos'], 10, TelaNivel3)
     
        self.coracao = Coracao(jogo, self.jogo.state['vidas'], False)

class TelaNivel3(TelaJogo):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.fundo = self.jogo.fundos[18]

        self.livro = Livro(jogo, c.LIVRO_CHANCE_GERACAO_3, c.LIVRO_VEL3)

        self.barra_vida = BarraVida(jogo, self.jogo.state['livros_atingidos'], 15, TelaJogo)
     
        self.coracao = Coracao(jogo, self.jogo.state['vidas'], False)