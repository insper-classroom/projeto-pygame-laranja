import pygame
import constants as c 

class GameState:
    def __init__(self, jogo):
        self.jogo = jogo

    def atualiza_estado(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if self.jogo.assets['valor'] == c.TELA_JOGO:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.jogo.state['espirra_agua'] = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.jogo.state['espirra_agua'] = False
                
        return True