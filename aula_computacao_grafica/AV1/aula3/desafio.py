from vpython import sphere, box, vector, color, cylinder, rate, scene, curve

# Definição da aceleração da gravidade (m/s^2)
gravidade = 9.8  
# Intervalo de tempo da simulação (passo de tempo para atualização da posição da bola)
dt = 0.01  

# Criar o chão (plano verde onde a bola quicará)
chao = box(pos=vector(0, -0.5, 0), size=vector(10, 1, 10), color=color.green)

# Criar a mesa com um cilindro como base e um tampo superior
mesa_base = cylinder(pos=vector(0, 0, 0), axis=vector(0, 2, 0), radius=0.3, color=color.red)
tampo_mesa = cylinder(pos=vector(0, 2, 0), axis=vector(0, 0.1, 0), radius=1.5, color=color.red)

# Criar a bola (posicionada acima da mesa, com uma cor azul)
bola = sphere(pos=vector(0, 2.3, 0), radius=0.2, color=color.blue)
# Definir a velocidade inicial da bola no eixo X
bola.velocity = vector(1, 0, 0)  

# Criar um objeto para armazenar a trajetória da bola (linha amarela)
trajetoria = curve(color=color.yellow)

# Variável de controle para iniciar a simulação
simulando = False

# Função para iniciar a simulação ao pressionar a tecla espaço
def iniciar_simulacao(evt):
    global simulando
    if evt.key == ' ':  # Se a tecla pressionada for espaço
        simulando = True

# Vincular a função ao evento de pressionamento de tecla
scene.bind('keydown', iniciar_simulacao)

# Loop de simulação
while True:
    rate(100)  # Controla a taxa de atualização da simulação (100 iterações por segundo)

    if simulando:
        # Atualizar a posição da bola com base na sua velocidade
        bola.pos += bola.velocity * dt

        # Registrar a posição da bola na trajetória
        trajetoria.append(pos=bola.pos)

        # Se a bola ainda estiver sobre a mesa, não há gravidade atuando sobre ela
        if bola.pos.x < tampo_mesa.radius - bola.radius:
            bola.velocity.y = 0 
        else:
            # Aplicar a aceleração da gravidade na velocidade vertical da bola
            bola.velocity.y -= gravidade * dt

        # Verificar colisão com o chão
        if bola.pos.y - bola.radius <= chao.pos.y + chao.size.y / 2:
            # Inverter a direção da velocidade vertical e aplicar um coeficiente de restituição (0.5 para perda de energia)
            bola.velocity.y = -bola.velocity.y * 0.5
            # Reduzir a velocidade no eixo X para simular atrito (0.8)
            bola.velocity.x *= 0.8