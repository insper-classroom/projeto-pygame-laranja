#imports
import pygame, sys
from pygame.locals import *
import random

#Define valores de cor (R,G,B)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL_CLARO = (0, 200, 255)
AMARELO = (255, 255, 0)
ROXO = (170, 0, 225)
cores = [VERDE, VERMELHO, AZUL_CLARO, AMARELO, ROXO]

#declarando variáveis ​​globais
leaderboard = {}

pontuacao = 0
maior_pontuacao = 0
nivel_num = 0
dificuldade = 0

replay = True
pressionado = False
escalar_feito = False
intro_feito = False
start_feito = False
start_output = False
jogo_start = False
lancar_barril = False
pula_esquerda = False
pula_direita = False
pula_parado = False
bater = False
cena_morte = False
jogo_feito = False
vitoria_jogo = False
vitoria_nivel = False
pontuacao_vitoria = False
vitoria_cena_output = False
vitoria_cena_feito = False

opcao = "topo"
direcao = "direita"

plataformasX = [55, 55, 51, 60, 56, 56, 56]
plataformasY = [9, 10, 8, 9, 11, 9, 9, 11]
plataforma_num = 0

PC_escalar = 0
escalar_cont = 15
plataforma_num = 0
PC_pulaX = 378
PC_pulaY = 172
PC_pulaYnum = 0

brunoX = 150
brunoY = 720
add_pula = -7
pula_cont = 0
ponto_salto = 0
cont_mortes = 0
vidas = 2

barrilX = []
barrilY = []
lancar_cont_regressiva = 0
barril_direcao = []
queda = []
queda_cont = []
barril_esquerda = []
barril_direita = []

plataforma_inclinaX = [100, 140, 190, 240, 280, 330, 380, 430, 480, 530, 570, 620, 670, 720]
inclina_cont = 0

escadaX1 = [295, 605, 295, 345, 345, 150, 245, 385, 600, 600, 245, 150, 265, 265, 315, 555, 555, 600, 440, 320]
escadaX2 = [305, 610, 310, 350, 350, 160, 255, 400, 610, 610, 255, 160, 280, 280, 325, 565, 565, 610, 450, 335]
escadaY1 = [710, 635, 617, 610, 526, 538, 522, 423, 506, 435, 414, 338, 409, 332, 309, 314, 417, 241, 154, 232]
escadaY2 = [720, 705, 657, 620, 571, 608, 532, 523, 511, 475, 464, 408, 414, 382, 329, 369, 432, 311, 232, 272]
escada_cima = [False, True, True, False, True, True, False, True, False, True, True, True, False, True, False, True, False, True, True, True]
escada_baixo = [True, True, False, True, False, True, True, True, True, False, False, True, True, False, True, False, True, True, True, False]

limites_esqueraY = [541, 341]
limites_direitaY = [638, 438, 244]

escada_barrilX = [320, 610, 560, 280, 160, 250, 400, 610, 350, 160, 300, 610]
escada_barrilY1 = [243, 252, 326, 270, 350, 428, 437, 449, 535, 547, 627, 645]
escada_barrilY2 = [343, 322, 446, 344, 420, 538, 527, 519, 625, 617, 727, 715]
barril_ajustar = [-2, 1, -1, 4, 2, 3, 5, 1, 5, 1, 4, 1]

confeteX = []
confeteY = []
confete_raio = []
confete_vel = []
confete_cor = []

#Define Imagens
titulo = pygame.image.load("title-screen.png")
start = pygame.image.load("start.png")
tela_vitoria = pygame.image.load("win-screen.png")
tela_gameover = pygame.image.load("game-over-screen.png")

seleciona_icone = pygame.image.load("select-icon.png")
vida = pygame.image.load("mario-life.png")

com_escada = pygame.image.load("withLadder.png")
plataforma0 = pygame.image.load("platform0.png")
plataforma1 = pygame.image.load("platform1.png")
plataforma2 = pygame.image.load("platform2.png")
plataforma3 = pygame.image.load("platform3.png")
plataforma4 = pygame.image.load("platform4.png")
plataforma5 = pygame.image.load("platform5.png")
plataforma6 = pygame.image.load("platform6.png")
plataformas = [plataforma0, plataforma1, plataforma2, plataforma3, plataforma4, plataforma5, plataforma6]
nivel = pygame.image.load("level.png")

azul0 = pygame.image.load("blue0.png")
azul1 = pygame.image.load("blue1.png")
azul2 = pygame.image.load("blue2.png")
azul3 = pygame.image.load("blue3.png")
azul4 = pygame.image.load("blue4.png")
azul5 = pygame.image.load("blue5.png")
azul_nums = [azul0, azul1, azul2, azul3, azul4, azul5]
branco0 = pygame.image.load("white0.png")
branco1 = pygame.image.load("white1.png")
branco2 = pygame.image.load("white2.png")
branco3 = pygame.image.load("white3.png")
branco4 = pygame.image.load("white4.png")
branco5 = pygame.image.load("white5.png")
branco6 = pygame.image.load("white6.png")
branco7 = pygame.image.load("white7.png")
branco8 = pygame.image.load("white8.png")
branco9 = pygame.image.load("white9.png")
branco_nums = [branco0, branco1, branco2, branco3, branco4, branco5, branco6, branco7, branco8, branco9]

bruno_esquerda = pygame.image.load("mario-left.png")
bruno_direita = pygame.image.load("mario-right.png")
correr_esquerda = pygame.image.load("run-left.png")
correr_direita = pygame.image.load("run-right.png")
bruno_pula_esquerda = pygame.image.load("jump-left.png")
bruno_pula_direita = pygame.image.load("jump-right.png")
bruno_escala1 = pygame.image.load("marioClimb1.png")
bruno_escala2 = pygame.image.load("marioClimb2.png")
morto = pygame.image.load("dead.png")
bruno_img = bruno_direita

livro_ajuda = pygame.image.load("pauline-help.png")
livro_parado = pygame.image.load("pauline-still.png")

PC_up1 = pygame.image.load("DK_up1.png")
PC_up2 = pygame.image.load("DK_up2.png")
PC_escala_vazio1 = pygame.image.load("dkClimbEmpty1.png")
PC_escala_vazio2 = pygame.image.load("dkClimbEmpty2.png")
PC_avancar = pygame.image.load("dkForward.png")
PC_esquerda = pygame.image.load("dkLeft.png")
PC_direita = pygame.image.load("dkRight.png")
PC_derrota = pygame.image.load("DK-defeat.png")
PC_img = PC_avancar

barril_pilha = pygame.image.load("barrel-stack.png")
barril_baixo = pygame.image.load("barrel-down.png")
barril1 = pygame.image.load("barrel1.png")
barril2 = pygame.image.load("barrel2.png")
barril3 = pygame.image.load("barrel3.png")
barril4 = pygame.image.load("barrel4.png")
barril_sequencia = [barril1, barril2, barril3, barril4]
barril_foto = []

coracao_quebrado = pygame.image.load("broken-heart.png")
coracao_int = pygame.image.load("full-heart.png")
relogio = pygame.time.Clock()
#declara valores de 400 pedaços de confete
for i in range(0, 400):
    #escolhe um valor aleatório de x e o anexa à lista
    x = random.randint(0, 800)
    confeteX.append(x)
    
    #escolhe valor aleatório de y e o anexa à lista
    y = random.randint(-500, -100)
    confeteY.append(y)
    
    #escolhe um raio aleatório e o anexa à lista
    r = random.randint(1, 4)
    confete_raio.append(r)
    
    #escolhe velocidade aleatória e a anexa à lista
    s = random.randint(5, 20)
    confete_vel.append(s)
    
    #escolhe uma cor aleatória e a anexa à lista
    cor = random.randint(0,4)
    confete_cor.append(cores[cor])