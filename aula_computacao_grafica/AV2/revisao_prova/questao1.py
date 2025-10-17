import pygame, random, math

pygame.init()

WIDTH, HEIGHT = 800,600
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Questão 1")

VERDE = (0,255,0)
VERMELHO = (255,0,0)

def gerar_poligon_convexo(num_pontos,raio_base=50,centro=(50,50)):
    angulos = sorted([random.uniform(0,2 * math.pi) for _ in range(num_pontos)])
    pontos = []
    for angulo in angulos:
        raio = random.uniform(raio_base * 0.5,raio_base * 1.2)
        x = centro[0] + raio * math.cos(angulo)
        y = centro[1] + raio * math.sin(angulo)
        pontos.append((x,y))
    return pontos

def gerar_formas_termicas(qtd_formas=5):
    gradientes_cores = [
        (255, 0, 0), # vermelho
        (255, 165, 0), #laranja
        (255, 255, 0), #amarelo 
        (0, 0, 255) #azul 
    ]

    formas = []

    for _ in range(qtd_formas):
        num_pontos = random.randit(4,6)
        pontos_2d = gerar_poligon_convexo(num_pontos)

        z_profundidade = random.randint(0,100)
        pontos_3ds =[(x,y,z_profundidade) for (x,y) in pontos_2d]


# def gerar_formas_termicas(qtd_formas=5):
#     gradientes_cores = [
#         (255, 0, 0), # vermelho
#         (255, 165, 0), #laranja
#         (255, 255, 0), #amarelo 
#         (0, 0, 255) #azul 
#     ]



# def gerando_formas_geometricas(quantidade):
#     formas_geometricas = []

#     for _ in range(quantidade):
#         cor = (
#             random.choice(range(0,256,3)),
#             random.choice(range(0,256,3)),
#             random.choice(range(0,256,3))
#         )
#         pontos = [
#             (
#                 random.randint(0,100),
#                 random.randint(0,100),
#                 random.randint(0,100)
#             ) for _ in range(4)
#         ]
#         z_buffer = sum(p[2] for p in pontos) / len(pontos)

#         formas_geometricas.append({
#             "cor": cor,
#             "pontos": pontos,
#             "z_buffer": z_buffer
#         })



rodando = True
while rodando:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
pygame.quit()