import pygame
import random
import sys

# Sons
if sys.platform == "win32":
    import winsound

    def som_ponto():
        winsound.MessageBeep()

    def som_morte():
        winsound.MessageBeep(winsound.MB_ICONHAND)
else:
    def som_ponto():
        print("som de ponto")

    def som_morte():
        print("som de morte")

pygame.init()

# Tela
LARGURA = 400
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

# Cores
AZUL = (135, 206, 235)
VERDE = (0, 200, 0)
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
LARANJA = (255, 140, 0)
VERMELHO = (220, 0, 0)

# Pássaro
passaro = pygame.Rect(50, 300, 30, 30)
velocidade = 0
gravidade = 0.5
pulo = -8

# Canos
canos = []
ESPACO = 220
DISTANCIA_CANOS = 320
VELOCIDADE_CANO = 3

# Jogo
pontos = 0
vidas = 3
fonte = pygame.font.SysFont(None, 36)
fonte_game_over = pygame.font.SysFont(None, 52)

def criar_cano():
    altura = random.randint(80, 300)
    topo = pygame.Rect(LARGURA, 0, 60, altura)
    baixo = pygame.Rect(400, altura + ESPACO, 60, ALTURA - (altura + ESPACO))
    return {
        "topo": topo,
        "baixo": baixo,
        "pontuou": False
    }

def desenhar_passaro(rect):
    pygame.draw.ellipse(tela, AMARELO, rect)

    olho_x = rect.x + 20
    olho_y = rect.y + 8
    pygame.draw.circle(tela, BRANCO, (olho_x, olho_y), 5)
    pygame.draw.circle(tela, PRETO, (olho_x + 1, olho_y), 2)

    bico_ponta = (rect.x + rect.width + 8, rect.y + 15)
    bico_cima = (rect.x + rect.width - 2, rect.y + 10)
    bico_baixo = (rect.x + rect.width - 2, rect.y + 20)
    pygame.draw.polygon(tela, LARANJA, [bico_cima, bico_baixo, bico_ponta])

canos.append(criar_cano())
game_over = False

while True:
    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not game_over:
                velocidade = pulo

            if evento.key == pygame.K_r and game_over:
                passaro = pygame.Rect(50, 300, 30, 30)
                velocidade = 0
                canos = [criar_cano()]
                pontos = 0
                vidas = 3
                game_over = False

    if not game_over:
        velocidade += gravidade
        passaro.y += int(velocidade)

        novos_canos = []
        for cano in canos:
            cano["topo"].x -= VELOCIDADE_CANO
            cano["baixo"].x -= VELOCIDADE_CANO

            if not cano["pontuou"] and cano["topo"].right < passaro.left:
                pontos += 1
                cano["pontuou"] = True
                som_ponto()

            if cano["topo"].right > 0:
                novos_canos.append(cano)

        canos = novos_canos

        if len(canos) == 0 or canos[-1]["topo"].x < LARGURA - DISTANCIA_CANOS:
            canos.append(criar_cano())

        for cano in canos:
            if passaro.colliderect(cano["topo"]) or passaro.colliderect(cano["baixo"]):
                vidas -= 1
                som_morte()

                if vidas <= 0:
                    game_over = True
                else:
                    passaro = pygame.Rect(50, 300, 30, 30)
                    velocidade = 0
                    canos = [criar_cano()]
                break

        if not game_over and (passaro.top <= 0 or passaro.bottom >= ALTURA):
            vidas -= 1
            som_morte()

            if vidas <= 0:
                game_over = True
            else:
                passaro = pygame.Rect(50, 300, 30, 30)
                velocidade = 0
                canos = [criar_cano()]

    tela.fill(AZUL)

    desenhar_passaro(passaro)

    for cano in canos:
        pygame.draw.rect(tela, VERDE, cano["topo"])
        pygame.draw.rect(tela, VERDE, cano["baixo"])

    texto_pontos = fonte.render(f"Pontos: {pontos}", True, PRETO)
    texto_vidas = fonte.render(f"Vidas: {vidas}", True, VERMELHO)

    tela.blit(texto_pontos, (10, 10))
    tela.blit(texto_vidas, (10, 45))

    if game_over:
        texto_final = fonte_game_over.render("GAME OVER", True, PRETO)
        texto_reiniciar = fonte.render("Aperte R para reiniciar", True, PRETO)

        tela.blit(texto_final, (100, 250))
        tela.blit(texto_reiniciar, (85, 300))

    pygame.display.flip()