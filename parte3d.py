from funcoes import *

app = Ursina()
window.fullscreen = True

# ───────────────────────────────────────────────────────────────
#  FOTOS
# ───────────────────────────────────────────────────────────────
MEMORIAS = [
    (('nossa_foto1.jpg'), 'Nossa 1a Foto Juntos'),
    (('sanca1.jpg'), 'Primeira vez em São Carlos'),
    (('show1.jpg'), 'Primeiro Show Juntos'),
    (('especial1.jpg'), 'Momento Especial'),
]

ADICIONAIS = [
    ('sanca2.jpg'),
    ('sanca3.jpg'),
    ('show2.jpg'),
    ('especial2.jpg'),
    ('especial3.jpg'),
    ('tinder.png')
]

# ───────────────────────────────────────────────────────────────
#  CONSTANTES DE LAYOUT
# ───────────────────────────────────────────────────────────────
H     = 4.5      # altura dos ambientes
D     = 10      # metade do tamanho da dungeon
MEIA_LARGURA_CORREDOR    = 4       # meia-largura do corredor (8u total)
SALA_LARGURA    = 7       # meia-largura das salinhas laterais
SALA_PROFUNDIDADE    = 5       # meia-profundidade das salinhas
GAP   = 3       # meia-abertura das portas (buraco de 6u)
PASSO = 22      # distância entre salas no eixo Z


NUMERO_MEMORIAS     = len(MEMORIAS)
LADO  = ([-1, 1] * (NUMERO_MEMORIAS // 2 + 1))[:NUMERO_MEMORIAS]               # alternando esq/dir
# ═══════════════════════════════════════
# POSICIONAMENTO GLOBAL
# ═══════════════════════════════════════

# fim da dungeon 1
Z_DUNGEON1_FIM = D

# começo da dungeon 2
Z_DUNGEON2_INICIO = Z_DUNGEON1_FIM

# fim da dungeon 2
Z_DUNGEON2_FIM = Z_DUNGEON2_INICIO + 110

# corredor começa DEPOIS da dungeon 2
Z_CORREDOR_INICIO = Z_DUNGEON2_FIM

# posições das salas
Z_SALAS = [Z_CORREDOR_INICIO + 15 + i * PASSO for i in range(NUMERO_MEMORIAS)]

# fim do corredor
Z_CORREDOR_FIM = Z_SALAS[-1] + 18


# ═══════════════════════════════════════════════════════════════
#  PARTE 1 — DUNGEON
# ═══════════════════════════════════════════════════════════════

# a orientação do jogo é: Z para frente, X para os lados (direita positivo) e Y para cima
# na função piso a ordem é X, Y, Z, 
# então o scale é (largura, altura, profundidade)

piso((0, 0, 0),  (D * 2, 1, D * 2), color.dark_gray) #chao
piso((0, H, 0),  (D * 2, 1, D * 2), color.gray, teto=True, textura=('parede.jpg')) #teto

parede(( 0,   H/2, -D),  (D * 2, H, 1), color.dark_gray, textura=('parede1.png'))       # sul
parede((-D,   H/2,  0),  (1, H, D * 2), color.dark_gray, textura=('parede1.png'))       # oeste
parede(( D,   H/2,  0),  (1, H, D * 2), color.dark_gray, textura=('parede1.png'))       # leste
parede((-6,   H/2,  D),  (D - 2, H, 1), color.dark_gray, textura=('parede1.png'))       # norte-esq ↘ buraco de 4u no centro
parede(( 6,   H/2,  D),  (D - 2, H, 1), color.dark_gray, textura=('parede1.png'))       # norte-dir ↙


# Textos finais na parede (usando Label3D)
Label3D('Chegue até o final da Dungeon', pos=(0, H - 0.5, D - 0.6), esc=9, cor=color.white)
Text(parent=scene, text="Próxima fase", position=(0, 3, 9), scale=15, color=color.red, origin=(0,0))

# Porta visual para a fase 2
porta_fase2 = Entity(
    model='cube',
    position=(0, H/2, D - 0.2),
    scale=(4, H, 0.3),
    color=color.brown,
    collider='box',
    texture=('porta.jpg'),
)



# ── Inimigos simples ────────────────────────────────────────────
class Inimigo(Entity):
    def __init__(self, pos):
        super().__init__(model=('esque.obj'), position=pos,
                         scale=0.03,
                         color=color.white, 
                         collider='box',)
        self.vida = 3
        self.vivo = True
        self.rotation_y = 90 # o modelo ta de lado, então precisa girar ele

    def update(self):
        if not self.vivo:
            return
        d = distance(self, player)
        if 1.5 < d < 12: #faz o inimigo andar
            dir_ = (player.position - self.position).normalized()
            dir_.y = 0
            self.position += dir_ * 3.5 * time.dt
            self.look_at_2d(player.position, 'y')
            self.rotation_y -= 90 # esqueleto tem o .obj virado pro lado


inimigos = []
for _ in range(5): # cria inimigos em posições aleatórias
    inimigos.append(Inimigo(Vec3(
        random.uniform(-D + 2, D - 2),
        -1,
        random.uniform(-D + 2, D - 5),
    )))

# ═══════════════════════════════════════
# PARTE 1.2 — SEGUNDA DUNGEON
# ═══════════════════════════════════════

# chão
piso((0, 0, Z_DUNGEON2_INICIO + 55),
   (20, 1, 110),
   color.dark_gray, textura=('chao2.jpg'))

# teto
piso((0, H, Z_DUNGEON2_INICIO + 55),
   (20, 1, 110),
   color.dark_gray,
   teto=True)

# paredes laterais
parede((-10, H/2, Z_DUNGEON2_INICIO + 60),
   (1, H, 120),
   color.dark_gray,
   textura=('parede.jpg'))

parede((10, H/2, Z_DUNGEON2_INICIO + 60),
   (1, H, 120),
   color.dark_gray,
   textura=('parede.jpg'))

# parede do fundo COM PORTA
parede((-6, H/2, Z_DUNGEON2_FIM),
   (8, H, 1),
   color.gray)
parede((6, H/2, Z_DUNGEON2_FIM),
   (8, H, 1),
   color.gray)


# porta pro corredor de memórias
porta_corredor = Entity(
    model='cube',
    position=(0, H/2, Z_DUNGEON2_FIM),
    scale=(4, H, 0.5),
    color=color.orange,
    collider='box',
    texture=('porta.jpg'),
)

# mensagens da segunda porta
Text(parent=scene, text="info pessoal", position=(0, 3, Z_DUNGEON2_FIM + 1.8), scale=15, color=color.red, origin=(0,0))
texto_amor = "info pessoal"
Label3D(texto_amor, pos=(0, 1, Z_DUNGEON2_FIM + 1.8), esc=8, cor=color.white)


Label3D(
    'Corredor de Memorias',
    pos=(0, H - 0.5, Z_DUNGEON2_FIM),
    esc=8,
    cor=color.orange
)
for _ in range(8): # mais inimigos
    inimigos.append(
        Inimigo(Vec3(
            random.uniform(-7, 7),
            -1,
            random.uniform(Z_DUNGEON2_INICIO + 10, Z_DUNGEON2_FIM - 10)
        ))
    )
# ═══════════════════════════════════════════════════════════════
#  PARTE 2 — CORREDOR DE MEMÓRIAS
# ═══════════════════════════════════════════════════════════════
LARGURA_CORREDOR  = Z_CORREDOR_FIM - Z_CORREDOR_INICIO # largura total do corredor (para calcular o centro)
Z_CENTRO_CORREDOR = Z_CORREDOR_INICIO + LARGURA_CORREDOR / 2 # centro do corredor (para posicionar o chão e teto)

piso((0, 0,  Z_CENTRO_CORREDOR), (MEIA_LARGURA_CORREDOR * 2, 1, LARGURA_CORREDOR), color.dark_gray) #chao
piso((0, H,  Z_CENTRO_CORREDOR), (MEIA_LARGURA_CORREDOR * 2, 1, LARGURA_CORREDOR), color.gray, teto=True, textura=('estrelas.png')) #teto

# Paredes do corredor, com buracos para as salas
def segs_parede(x_muro, zs_buracos):
    """Paredes com buracos nos z das salas."""
    # lista de (inicio, fim) dos buracos, ordenada
    cortes = sorted([(z - GAP, z + GAP) for z in zs_buracos])     
    # zc significa "z corrente", começa no início do corredor 
    zc = Z_CORREDOR_INICIO 
    for za, zb in cortes:
        # za é o início do buraco, zb é o fim do buraco
        # s é o tamanho da parede antes do buraco
        s = za - zc
        if s > 0.05:
            parede((x_muro, H/2, zc + s / 2), (1, H, s), color.gray, textura=('parede1.png'))
        zc = zb
    s = Z_CORREDOR_FIM - zc # parede depois do último buraco
    if s > 0.05:
        parede((x_muro, H/2, zc + s / 2), (1, H, s), color.gray, textura=('parede1.png'))


segs_parede(-MEIA_LARGURA_CORREDOR, [Z_SALAS[i] for i in range(NUMERO_MEMORIAS) if LADO[i] == -1])
segs_parede( MEIA_LARGURA_CORREDOR, [Z_SALAS[i] for i in range(NUMERO_MEMORIAS) if LADO[i] ==  1])

#cria salas na lageral do corredor
def criar_sala(z, lado, txt, arq, arq2 = None, arq3 = None):
    """
    Cria uma salinha lateral com um quadro e uma foto na parede do fundo.
      lado = -1 → esquerda do corredor
      lado = +1 → direita do corredor
    """
    
    X_PORTA = MEIA_LARGURA_CORREDOR * lado # x da abertura (borda do corredor)
    X_CENTRO_SALA = (MEIA_LARGURA_CORREDOR + SALA_LARGURA) * lado # x do centro da sala
    X_PAREDE_DO_FUNDO_SALA = (MEIA_LARGURA_CORREDOR + SALA_LARGURA * 2) * lado  # x da parede do fundo

    #── Foto na parede do fundo ──────────────────────────────
    foto3d(
        pos=((abs(X_PAREDE_DO_FUNDO_SALA) - 0.60) * lado, H/2, z),
        esc=(0.34, 0.255),
        ry= 90 * lado,
        arquivo=arq,
    )
    # foto parede esquerda da sala
    if arq2:
        foto3d(
            pos=(X_CENTRO_SALA, H/2, z + SALA_PROFUNDIDADE - 0.6),
            esc=(0.34, 0.255),
            ry= 0 * lado,
            arquivo=arq2,
        )
    # foto parede direita da sala
    if arq3:
        foto3d(
            pos=(X_CENTRO_SALA, H/2, z - SALA_PROFUNDIDADE + 0.6),
            esc=(0.34, 0.255),
            ry= 180 * lado,
            arquivo=arq3,
        )

    # quadro que fica no fundo, atrás da foto
    quadro = Entity(
        model='quad',
        texture= ("quadro.png"),
        position=((abs(X_PAREDE_DO_FUNDO_SALA) - 0.55) * lado, H/2, z),
        scale=(5.5, 4.725),
        rotation=(0, 90 * lado, 0), # Giramos a foto para alinhar com a parede
        # -90 de direita, 90 se esquerda
        double_sided=True
    )


    # Paredes em U, abertura para o corredor
    parede((X_PAREDE_DO_FUNDO_SALA, H/2, z),        (1,  H, SALA_PROFUNDIDADE * 2), color.gray, textura=('parede1.png'))  # parede do fundo
    parede((X_CENTRO_SALA, H/2, z - SALA_PROFUNDIDADE),   (SALA_LARGURA * 2,  H, 1), color.gray, textura=('parede1.png'))
    parede((X_CENTRO_SALA, H/2, z + SALA_PROFUNDIDADE),   (SALA_LARGURA * 2,  H, 1), color.gray, textura=('parede1.png'))

    # Chão e teto da sala
    piso((X_CENTRO_SALA, 0, z),  (SALA_LARGURA * 2, 1, SALA_PROFUNDIDADE * 2), color.dark_gray)
    piso((X_CENTRO_SALA, H, z),  (SALA_LARGURA * 2, 1, SALA_PROFUNDIDADE * 2), color.gray, teto=True, textura=('estrelas.png'))


    # ── PORTA na abertura da sala ──────────────────────────────
    porta_sala = Entity(
        model='cube',
        position=(X_PORTA, H/2, z),
        scale=(0.2, H, 2*GAP),
        color=color.brown,
        collider='box',
        texture=('porta.jpg'),
    )
    porta_sala.aberta = False  # Marca se a porta está aberta
    
    # Letreiro da porta (nome da memória)
    Label3D(txt, pos=(X_PORTA, H, z), esc=8, cor=color.white)
    

    return porta_sala  # Retorna a porta para ser controlada


portas_salas = []
for i, (arq, txt) in enumerate(MEMORIAS): #cria as salas laterais do corredor com as fotos e os textos
    """
    Aqui era para ficar tudo dentro da função "criar_sala". Mas tava com dificuldade de fazer
    os textos ficarem nos lugares certos, já que em cada sala eles ficariam em lugares diferentes.
    Então resolvi colocar a parte do texto explicitamente em cada if para facilitar
    """
    if i == 0:
        texto = "info pessoal"
        x_centro = (MEIA_LARGURA_CORREDOR + SALA_LARGURA) * LADO[i]
        painel = Entity(
            position=(
                x_centro,
                H/2,
                Z_SALAS[i] - SALA_PROFUNDIDADE + 0.6
            ),
            rotation_y=180 * LADO[i]
        )
        Text(
            text=texto,
            scale=8, color=color.white, parent=painel, origin=(0,0)
        )
        arq2 = ADICIONAIS[5] # foto da parede esquerda
        porta = criar_sala(Z_SALAS[i], LADO[i], txt, arq, arq2)
    elif i == 1:
        texto = "info pessoal"
        x_centro = (MEIA_LARGURA_CORREDOR + 3*SALA_LARGURA/2 + 0.2) * LADO[i]
        painel = Entity(
            position=(
                x_centro,
                H/2,
                Z_SALAS[i] - SALA_PROFUNDIDADE + 0.6
            ),
            rotation_y=180 * LADO[i]
        )
        Text(
            text=texto,
            scale=8, color=color.white, parent=painel, origin=(0,0)
        )
        texto = "info pessoal"
        x_centro = (MEIA_LARGURA_CORREDOR + SALA_LARGURA/2 - 0.3) * LADO[i]
        painel = Entity(
            position=(
                x_centro,
                H/2,
                Z_SALAS[i] - SALA_PROFUNDIDADE + 0.6
            ),
            rotation_y=180 * LADO[i]
        )
        Text(
            text=texto,
            scale=8, color=color.white, parent=painel, origin=(0,0)
        )
        arq2 = ADICIONAIS[0] # foto da parede esquerda
        arq3 = ADICIONAIS[1]  # foto da parede direita
        porta = criar_sala(Z_SALAS[i], LADO[i], txt, arq, arq2, arq3)
    elif i == 2:
        texto = "info pessoal"
        x_centro = (MEIA_LARGURA_CORREDOR + SALA_LARGURA) * LADO[i]
        painel = Entity(
            position=(
                x_centro,
                H/2,
                Z_SALAS[i] - SALA_PROFUNDIDADE + 0.6
            ),
            rotation_y=180 * LADO[i]
        )
        Text(
            text=texto,
            scale=8, color=color.white, parent=painel, origin=(0,0)
        )
        arq2 = ADICIONAIS[2]  # foto da parede esquerda
        porta = criar_sala(Z_SALAS[i], LADO[i], txt, arq, arq2)
    elif i == 3:
        arq2 = ADICIONAIS[3]  # foto da parede esquerda
        arq3 = ADICIONAIS[4]  # foto da parede direita
        porta = criar_sala(Z_SALAS[i], LADO[i], txt, arq, arq2, arq3)
    else:
        porta = criar_sala(Z_SALAS[i], LADO[i], txt, arq)
    portas_salas.append(porta)



# ═══════════════════════════════════════════════════════════════
#  PARTE 3 — SALA FINAL
# ═══════════════════════════════════════════════════════════════

# sala final
LARGURA_FINAL = 22 # tamanho da sala final 
Z_FINAL = Z_CORREDOR_FIM # posição da sala final
Z_FINAL_CENTRO = Z_FINAL + LARGURA_FINAL / 2 #posição do centro da sala final (para chão e teto)

piso((0, 0,  Z_FINAL_CENTRO), (LARGURA_FINAL, 1, LARGURA_FINAL), color.dark_gray) #chao
piso((0, H,  Z_FINAL_CENTRO), (LARGURA_FINAL, 1, LARGURA_FINAL), color.white, teto=True, textura=('estrelas.png')) #teto

parede((0,      H/2, Z_FINAL + LARGURA_FINAL),  (LARGURA_FINAL, H, 1), color.white, textura=('arcade.png'))          # fundo
parede((-LARGURA_FINAL/2,  H/2, Z_FINAL_CENTRO),      (1, H, LARGURA_FINAL), color.gray, textura=('arcade.png'))           # esquerda
parede(( LARGURA_FINAL/2,  H/2, Z_FINAL_CENTRO),      (1, H, LARGURA_FINAL), color.gray, textura=('arcade.png'))           # direita
parede((-6,     H/2, Z_FINAL),       (LARGURA_FINAL/2 - 1.9, H, 1), color.gray, textura=('arcade.png'))     # frente-esq ↘ abertura de 12u
parede(( 6,     H/2, Z_FINAL),       (LARGURA_FINAL/2 - 1.9, H, 1), color.gray, textura=('arcade.png'))     # frente-dir ↙

# ── Fotos nas paredes da sala final ─────────────────────────
"""Cria uma salinha lateral com um quadro e uma foto na parede do fundo.
      lado = -1 → esquerda do corredor
      lado = +1 → direita do corredor
"""
j = 4
for i, (arq, txt) in enumerate(MEMORIAS):
    if i >= 2:
        j = -4
    if i % 2 == 0:
        lado = -1
    else:
        lado = 1
    foto3d(
        pos=((abs(LARGURA_FINAL/2) - 0.60) * lado, H/2, Z_FINAL_CENTRO + j),
        esc=(0.34, 0.255),
        ry= 90 * lado,
        arquivo=arq,
    )

    quadro = Entity(
        model='quad',
        texture= ("quadro.png"),
        position=((abs(LARGURA_FINAL/2) - 0.55) * lado, H/2, Z_FINAL_CENTRO + j),
        scale=(5.5, 4.725),
        rotation=(0, 90 * lado, 0),      # Giramos a foto para alinhar com a parede
        # -90 de direita, 90 se esquerda
        double_sided=True
    )

# Texto de amor na parede da sala final
texto = "info pessoal"
Text(
    text=texto,
    origin=(0, 0), scale=10, color=color.white, parent=scene,
    position=(0, H/2, Z_FINAL + LARGURA_FINAL - 0.6),
)

# ── Pedestal + botão ────────────────────────────────────────
parede((0, 1, Z_FINAL_CENTRO - 4), (1, 2, 1), color.gray)            # pedestal
botao_3d = Entity(
    model='cube',
    position=(0, 2.7, Z_FINAL_CENTRO - 4),
    scale=(0.8, 0.8, 0.8),
    color=color.red,
    collider='box',
)
Label3D('[E] Apertar', pos=(0, 3.6, Z_FINAL_CENTRO - 4 - 0.5), esc=7, cor=color.white)

mensagem_surp = Text(
    text='fimmmm',
    origin=(0, 0), scale=5, color=color.red,
    enabled=False, background=True,
)
surp_ativada = False


def ativar_surpresa():
    global surp_ativada
    if not surp_ativada:
        surp_ativada = True
        mensagem_surp.enabled = True
        botao_3d.color = color.lime


# ═══════════════════════════════════════════════════════════════
#  JOGADOR
# ═══════════════════════════════════════════════════════════════
player = FirstPersonController(position=(0, 2, -D + 3), origin_y=-0.5, speed=10)
Entity(parent=camera.ui, model='quad', scale=0.01, color=color.white)   # mira


# ═══════════════════════════════════════════════════════════════
#  INPUT
# ═══════════════════════════════════════════════════════════════
def input(key):
    if key == 'escape':
        application.quit()

    # Ataque — clique esquerdo, raio de 3u
    if key == 'left mouse down':
        hit = raycast(camera.world_position, 
                      camera.forward,
                      distance=3, 
                      ignore=(player,)
        )
        if hit.hit:
            for ini in inimigos:
                if ini.vivo and hit.entity == ini: 
                    # se acertar o inimigo tira vida e vai mudando de cor
                    ini.vida -= 1
                    cores = {2: color.orange, 1: color.yellow} 
                    ini.color = cores.get(ini.vida, color.red)
                    if ini.vida <= 0:
                        ini.vivo = False
                        ini.disable()
                    break

    # Interação — tecla E, raio de 3u
    if key == 'e':

        hit = raycast(
            camera.world_position,
            camera.forward,
            distance=3,
            ignore=(player,)
        )


        if hit.hit:
            # Abrir portas das salas laterais
            for porta in portas_salas:
                if hit.entity == porta and not porta.aberta:
                    porta.aberta = True
                    porta.animate_position(
                        porta.position + Vec3(0, H + 1, 0),
                        duration=1
                    )
                    porta.collider = None
                    break
            
            # Abrir porta pro corredor de memórias
            if hit.entity == porta_corredor:
                #começa a tocar zoe_jane
                zoe_jane = Audio(
                    'zoe_jane.mp3',
                    loop=True,
                    autoplay=False)
                zoe_jane.play()
                porta_corredor.animate_position(
                    porta_corredor.position + Vec3(0, H + 1, 0),
                    duration=1
                )
                porta_corredor.collider = None

            # Abrir a primeir aporta
            elif hit.entity == porta_fase2:
                porta_fase2.animate_position(
                    porta_fase2.position + Vec3(0, H + 1, 0),
                    duration=1
                )
                porta_fase2.collider = None


            # Botão final
            elif hit.entity == botao_3d:
                ativar_surpresa()


# ═══════════════════════════════════════════════════════════════
#  HUD
# ═══════════════════════════════════════════════════════════════
Text(
    '[Clique Esq] Atacar    [E] Interagir    [ESC] Sair',
    origin=(0, -0.5), position=(0, -0.46),
    scale=0.75, color=color.white,
)

app.run()