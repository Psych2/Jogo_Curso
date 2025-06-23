import pygame
import sys

pygame.init()

# Tela
tdt = (1920, 1080)
tela = pygame.display.set_mode(tdt, pygame.FULLSCREEN)
pygame.display.set_caption("Meu Jogo")

# Sons
som_colisao = pygame.mixer.Sound("som_colisao.wav")
som_vitoria = pygame.mixer.Sound("som_vitoria.wav")
som_derrota = pygame.mixer.Sound("som_derrota.wav")
pygame.mixer.music.load("musica_fundo.mp3")
pygame.mixer.music.play(-1)

# Cores
cores = {
    "branca": [255, 255, 255],
    "preta": [0, 0, 0],
    "amarela": [255, 255, 0],
    "azul": [0, 0, 255],
    "verde": [0, 255, 0]
}

# Jogador
tam_jogador = 100
jogador = pygame.Rect(0, 1050, tam_jogador, 15)

# Classe da Bola com imagem e hitbox
class Bola:
    def __init__(self, imagem_path, x, y, velocidade):
        imagem_original = pygame.image.load(imagem_path).convert_alpha()
        self.imagem = pygame.transform.scale(imagem_original, (30, 30))  # Ajuste o tamanho aqui
        self.rect = self.imagem.get_rect(center=(x, y))
        self.vel = velocidade

    def mover(self):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]

        if self.rect.left <= 0 or self.rect.right >= tdt[0]:
            self.vel[0] = -self.vel[0]
        if self.rect.top <= 0:
            self.vel[1] = -self.vel[1]
        if self.rect.bottom >= tdt[1]:
            return False  # Saiu da tela
        return True

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect.topleft)

    def colide_com(self, outro):
        return self.rect.colliderect(outro)

# Criar blocos
def criar_blocos(cols, rows):
    blocos = []
    largura = tdt[0] // cols - 5
    altura = 15
    for j in range(rows):
        for i in range(cols):
            x = i * (largura + 5)
            y = j * (altura + 10)
            blocos.append(pygame.Rect(x, y, largura, altura))
    return blocos

# Movimento jogador
def mov_jogador_tecla():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and jogador.right < tdt[0]:
        jogador.x += 7
    if keys[pygame.K_LEFT] and jogador.left > 0:
        jogador.x -= 7

# Atualizar pontos
def atualizar_pontos(pontos):
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f"Pontos: {pontos}", True, cores["azul"])
    tela.blit(texto, (0, 780))

# Desenhar jogo
def desenhar_inicio_jogo(fundo_frame, bola):
    tela.blit(fundo_frame, (0, 0))
    pygame.draw.rect(tela, cores["azul"], jogador)
    bola.desenhar(tela)

# Blocos
qntd_blocos_linhas = 5
qntd_linhas_blocos = 4
blocos = criar_blocos(qntd_blocos_linhas, qntd_linhas_blocos)

# Fundo animado (2 frames)
fundo_frames = [
    pygame.transform.scale(pygame.image.load("fundo_0.png").convert(), tdt),
    pygame.transform.scale(pygame.image.load("fundo_1.png").convert(), tdt)
]
frame_atual = 0
tempo_frame = 300
ultimo_tempo = pygame.time.get_ticks()

# Bola
bola = Bola("bola.png", 100, 500, [4, -4])
pontos = 0
fim = False

# Loop principal
while not fim:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim = True

    # Atualiza fundo animado
    agora = pygame.time.get_ticks()
    if agora - ultimo_tempo > tempo_frame:
        frame_atual = (frame_atual + 1) % 2
        ultimo_tempo = agora

    mov_jogador_tecla()

    # Movimento e colisão da bola
    if not bola.mover():
        fim = True
        som_derrota.play()
        mensagem = "Game Over"

    if bola.colide_com(jogador):
        bola.vel[1] = -bola.vel[1]
        som_colisao.play()

    for bloco in blocos[:]:
        if bola.colide_com(bloco):
            blocos.remove(bloco)
            bola.vel[1] = -bola.vel[1]
            pontos += 1
            som_colisao.play()

    # Vitória
    if len(blocos) == 0:
        som_vitoria.play()
        fim = True
        mensagem = "Você venceu!"

    # Desenho
    desenhar_inicio_jogo(fundo_frames[frame_atual], bola)
    for bloco in blocos:
        pygame.draw.rect(tela, cores["verde"], bloco)
    atualizar_pontos(pontos)

    pygame.display.flip()
    pygame.time.delay(10)

# Tela final
pygame.mixer.music.stop()
fonte = pygame.font.Font(None, 80)
texto = fonte.render(mensagem, True, cores["amarela"])
tela.blit(texto, (tdt[0] // 2 - 200, tdt[1] // 2))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
