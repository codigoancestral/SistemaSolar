import pygame
import math
import locale

pygame.init()

LARGURA, ALTURA = 750, 650
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
AZUL = (100, 149, 237)
VERMELHO = (188, 39, 50)
CINZA_ESCURO = (80, 78, 81)

FONTE = pygame.font.SysFont("comicsans", 26)

janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Sistema Planetário Solar')
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class Planeta:
  UA = 149.6e6 * 1000
  G = 6.67428e-11
  ESCALA = 200 / UA            # 1 UA = 100 pixels
  PASSAGEMTEMPO = 3600 * 24    # 1 dia

  def __init__(self, x, y, raio, cor, massa):
      self.x = x
      self.y = y
      self.raio = raio
      self.cor = cor
      self.massa = massa

      self.orbita = []
      self.sol = False
      self.distanciaSol = 0

      self.velocidadeX = 0
      self.velocidadeY = 0

  def desenho(self, janela):
    x = self.x * self.ESCALA + LARGURA / 2
    y = self.y * self.ESCALA + ALTURA / 2

    if len(self.orbita) > 2:
      pontosAtualizados = []
      for ponto in self.orbita:
        x, y = ponto
        x = x * self.ESCALA + LARGURA / 2
        y = y * self.ESCALA + ALTURA / 2
        pontosAtualizados.append((x, y))
    
      pygame.draw.lines(janela, self.cor, False, pontosAtualizados, 2)  # desenha as órbitas
    pygame.draw.circle(janela, self.cor, (x,y), self.raio)              # desenha os planetas e o sol

    if not self.sol:
      textoDistancia = FONTE.render(f'{locale.currency(round(self.distanciaSol/1000, 1), symbol=False, grouping=True)}km', 1, BRANCO)
      janela.blit(textoDistancia, (x - textoDistancia.get_width()/2, y - textoDistancia.get_width()/2))
  
  def atracao(self, outroObjeto):
     outroObjetoX, outroObjetoY = outroObjeto.x, outroObjeto.y
     distanciaX = outroObjetoX - self.x
     distanciaY = outroObjetoY - self.y
     distancia = math.sqrt(distanciaX ** 2 + distanciaY ** 2)                 # distância entre dois objetos
     if outroObjeto.sol:
       self.distanciaSol = distancia
      
     forcaAtracao = self.G * self.massa * outroObjeto.massa / distancia**2    # força de atração entre dois objetos
     anguloTheta = math.atan2(distanciaY, distanciaX)                         # ângulo entre dois objetos

     forcaX = math.cos(anguloTheta) * forcaAtracao                            # componente X da força de atração
     forcaY = math.sin(anguloTheta) * forcaAtracao                            # componente Y da força de atração

     return forcaX, forcaY

  def atualizaPosicao(self, planetas):
    totalFX = totalFY = 0
    for planeta in planetas:
      if self == planeta:
        continue

      fx, fy = self.atracao(planeta)
      totalFX += fx                                               # Atualiza a força de atração X
      totalFY += fy                                               # Atualiza a força de atração Y

    self.velocidadeX += totalFX / self.massa * self.PASSAGEMTEMPO  # Atualiza a velocidade X
    self.velocidadeY += totalFY / self.massa * self.PASSAGEMTEMPO  # Atualiza a velocidade Y

    self.x += self.velocidadeX * self.PASSAGEMTEMPO               # Atualiza a posição X
    self.y += self.velocidadeY * self.PASSAGEMTEMPO               # Atualiza a posição Y

    self.orbita.append((self.x, self.y))                          # Atualiza a órbita do objeto

def main():
  run = True
  clock = pygame.time.Clock()

  sol       = Planeta(0, 0, 30, AMARELO, 1.98882 * 10**30)
  sol.sol = True

  mercurio  = Planeta(0.387 * Planeta.UA, 0, 8, CINZA_ESCURO, 3.30 * 10**23)
  mercurio.velocidadeY = -47.4 * 1000

  venus     = Planeta(0.723 * Planeta.UA, 0, 14, BRANCO, 4.8685 * 10**24)
  venus.velocidadeY = -35.2 * 1000

  terra     = Planeta(-1 * Planeta.UA, 0, 16, AZUL, 5.9742 * 10**24)
  terra.velocidadeY = 29.783 * 1000

  marte     = Planeta(-1.524 * Planeta.UA, 0, 12, VERMELHO, 6.39 * 10**23)
  marte.velocidadeY = 24.077 * 1000

  planetas = [sol, mercurio, venus, terra, marte]

  while run:
    clock.tick(60)
    janela.fill((0,0,0))
    pygame.display.update()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

    for planeta in planetas:
      planeta.atualizaPosicao(planetas)
      planeta.desenho(janela)

    pygame.display.update()
  
  pygame.quit()

main()