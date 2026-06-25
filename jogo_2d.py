from __future__ import annotations
import pygame, sys, random, textwrap, math
from dataclasses import dataclass, field
from typing import List, Optional, Callable


# ═══════════════════════════════════════════════════════════════════
#  INICIALIZAÇÃO
# ═══════════════════════════════════════════════════════════════════
pygame.init() # inicia o pygame
SW, SH = 1600, 1000 # tamanho da janela
tela = None # A tela começa vazia para não abrir antes da hora
relogio   = pygame.time.Clock() # normaliza fps
FPS     = 60

def iniciar_tela():
    global tela
    tela = pygame.display.set_mode((SW, SH)) # cria a janela 
    pygame.display.set_caption("Busca do Reino Antigo") # título da janela
    return tela

# ── Fontes ──────────────────────────────────────────────────────────
def _fonte(tamanho: int, negrito=False) -> pygame.font.Font:
    for nome in ("Courier New", "Courier", "Lucida Console"):
        try:
            return pygame.font.SysFont(nome, tamanho, bold=negrito)
        except Exception:
            pass
    return pygame.font.Font(None, tamanho + 2)

FONTE_MINUSCULA = _fonte(11)              # fonte minúscula / descrições
FONTE_PEQUENA = _fonte(13)              # fonte pequena
FONTE_MEDIA = _fonte(14)              # fonte média
FONTE_NEGRITO = _fonte(14, negrito=True)   # fonte média (botões)
FONTE_GRANDE = _fonte(17)              # fonte grande
FONTE_TITULO = _fonte(11, negrito=True)   # titulo

# ── Paleta ────────────────────────────────────────────────────────
AREA_DE_TRABALHO     = (  0, 128, 128)   # desktop
COR_JANELA = (192, 192, 192)   # cinza da janela
TITLE_ATIVA  = (  0,   0, 128)   # barra ativa
TITLE_INATIVA  = (128, 128, 128)   # barra desativada
BRANCO    = (255, 255, 255)
CINZA     = (128, 128, 128)
ESCURO     = ( 64,  64,  64)
PRETO    = (  0,   0,   0)
VERMELHO      = (200,   0,   0)
VERDE    = (  0, 180,   0)
AMARELO   = (220, 200,   0)
LARANJA   = (220, 120,   0)
AZUL     = (  0,   0, 200)
VIDA_OK    = (  0, 180,   0)
VIDA_MEDIA   = (220, 200,   0)
VIDA_BAIXA    = (200,   0,   0)
COR_MANA   = ( 50,  50, 220)
COR_XP   = (180, 160,   0)
FUNDO_SELECAO   = (  0,   0, 128)
FONTE_SELECAO   = (255, 255, 255)

# ═══════════════════════════════════════════════════════════════════
#  UTILITÁRIOS DE DESENHO
# ═══════════════════════════════════════════════════════════════════
def relevo(surf: pygame.Surface, rect, fill=COR_JANELA): # desenha um retângulo com bordas claras e escuras para dar efeito de relevo
    r = pygame.Rect(rect)
    pygame.draw.rect(surf, fill, r)
    pygame.draw.line(surf, BRANCO,  (r.x,     r.y),       (r.right-1, r.y))
    pygame.draw.line(surf, BRANCO,  (r.x,     r.y),       (r.x,       r.bottom-1))
    pygame.draw.line(surf, PRETO,  (r.x,     r.bottom-1),(r.right-1, r.bottom-1))
    pygame.draw.line(surf, PRETO,  (r.right-1, r.y),     (r.right-1, r.bottom-1))
    pygame.draw.line(surf, BRANCO,  (r.x+1,   r.y+1),     (r.right-2, r.y+1))
    pygame.draw.line(surf, BRANCO,  (r.x+1,   r.y+1),     (r.x+1,     r.bottom-2))
    pygame.draw.line(surf, CINZA,   (r.x+1,   r.bottom-2),(r.right-2, r.bottom-2))
    pygame.draw.line(surf, CINZA,   (r.right-2, r.y+1),   (r.right-2, r.bottom-2))

def relevo_baixo(surf: pygame.Surface, rect, fill=BRANCO):# desenha um retângulo com bordas escuras e claras para dar efeito de rebaixo
    r = pygame.Rect(rect)
    pygame.draw.rect(surf, fill, r)
    pygame.draw.line(surf, ESCURO,   (r.x,     r.y),       (r.right-1, r.y))
    pygame.draw.line(surf, ESCURO,   (r.x,     r.y),       (r.x,       r.bottom-1))
    pygame.draw.line(surf, BRANCO,  (r.x,     r.bottom-1),(r.right-1, r.bottom-1))
    pygame.draw.line(surf, BRANCO,  (r.right-1, r.y),     (r.right-1, r.bottom-1))
    pygame.draw.line(surf, PRETO,  (r.x+1,   r.y+1),     (r.right-2, r.y+1))
    pygame.draw.line(surf, PRETO,  (r.x+1,   r.y+1),     (r.x+1,     r.bottom-2))
    pygame.draw.line(surf, CINZA,   (r.x+1,   r.bottom-2),(r.right-2, r.bottom-2))
    pygame.draw.line(surf, CINZA,   (r.right-2, r.y+1),   (r.right-2, r.bottom-2))

def botao_janela(surf, rect, rotulo: str, apertado=False, ligado=True, fonte=None):
    f = fonte or FONTE_NEGRITO
    r = pygame.Rect(rect)
    ox = oy = 1 if apertado else 0 # deslocamento do texto para simular o botão sendo pressionado
    (relevo_baixo if apertado else relevo)(surf, r, COR_JANELA)
    cor = CINZA if not ligado else PRETO
    lbl = f.render(rotulo, True, cor)
    surf.blit(lbl, (r.x + (r.w - lbl.get_width())  // 2 + ox,
                    r.y + (r.h - lbl.get_height()) // 2 + oy))

def barra_horizontal(surf, rect, val, vida_max, col_hi=VIDA_OK, col_lo=VIDA_BAIXA):
    r = pygame.Rect(rect)
    pygame.draw.rect(surf, PRETO, r)
    if vida_max > 0:
        frac = max(0.0, min(1.0, val / vida_max))
        cor  = col_hi if frac > 0.4 else (VIDA_MEDIA if frac > 0.2 else col_lo)
        fw   = max(0, int((r.w - 2) * frac))
        pygame.draw.rect(surf, cor, (r.x + 1, r.y + 1, fw, r.h - 2))
    pygame.draw.rect(surf, CINZA, r, 1)

def escrever(surf, fonte, texto, x, y, cor=PRETO): # desenha um texto na posição (x, y) usando a fonte e cor especificadas, e retorna a largura do texto desenhado
    lbl = fonte.render(str(texto), True, cor)
    surf.blit(lbl, (x, y))
    return lbl.get_width()

def escrever_centralizado(surf, fonte, texto, cx, y, cor=PRETO): # desenha um texto centralizado na posição (cx, y) usando a fonte e cor especificadas
    lbl = fonte.render(str(texto), True, cor)
    surf.blit(lbl, (cx - lbl.get_width() // 2, y))

# ═══════════════════════════════════════════════════════════════════
#  JANELA BASE
# ═══════════════════════════════════════════════════════════════════
ALTURA_JANELA = 20
BORDA  = 2

class JanelaBase:
    _next_id = 0

    def __init__(self, x, y, w, h, titulo: str,
                 fechavel=True, cor_icone=(200, 200, 0)):
        JanelaBase._next_id += 1
        self.id         = JanelaBase._next_id
        self.rect       = pygame.Rect(x, y, w, h)
        self.titulo      = titulo
        self.fechavel  = fechavel
        self.cor_icone   = cor_icone
        self.ativa     = False
        self.visivel    = True
        self._arrastando      = False
        self._deslocamento_arrasto  = (0, 0)
        self._largura_interna        = w - BORDA * 2
        self._altura_interna        = h - BORDA * 2 - ALTURA_JANELA
        self.surf       = pygame.Surface((self._largura_interna, self._altura_interna))

    # ── Geometria ──────────────────────────────────────────────────
    # @propety serve para acessar valores como se fossem atributos, mas na verdade são métodos
    # serve para proteger o acesso a esses valores que não devem ser mudados (começam com _)
    @property
    def rect_interno(self) -> pygame.Rect:
        return pygame.Rect(self.rect.x + BORDA,
                           self.rect.y + BORDA + ALTURA_JANELA,
                           self._largura_interna, self._altura_interna)

    @property
    def titulo_rect(self) -> pygame.Rect:
        close_space = 16 if self.fechavel else 0# espaço para o botão de fechar, se a janela for fechável
        return pygame.Rect(self.rect.x + BORDA,
                           self.rect.y + BORDA,
                           self._largura_interna - close_space, ALTURA_JANELA)

    @property
    def fechar_rect(self) -> pygame.Rect:
        return pygame.Rect(self.rect.right - BORDA - 16,
                           self.rect.y + BORDA, 16, ALTURA_JANELA)

    # ── Eventos ────────────────────────────────────────────────────
    def apertar_mouse(self, pos, btn) -> bool:
        if not self.rect.collidepoint(pos): # se não clicar dentro da janela, ignora
            return False
        if btn == 1: # botão esquerdo
            # clicar no botão de fechar
            if self.fechavel and self.fechar_rect.collidepoint(pos): 
                self.visivel = False # fecha a janela
                return True # intercepta o clique para não passar para outras janelas
            if self.titulo_rect.collidepoint(pos): # clicar na barra de título
                self._arrastando     = True # arrasta a janela
                self._deslocamento_arrasto = (pos[0] - self.rect.x, pos[1] - self.rect.y) # calcula o offset do clique para manter a posição relativa
                return True# intercepta o clique para não passar para outras janelas
            lx = pos[0] - self.rect_interno.x # calcula a posição relativa do clique dentro da área interna da janela
            ly = pos[1] - self.rect_interno.y
            self._on_click(lx, ly)
        return True

    def soltar_mouse(self, pos, btn):
        self._arrastando = False

    def mover_mouse(self, pos):
        if self._arrastando:
            nx = max(0, min(SW - self.rect.w, pos[0] - self._deslocamento_arrasto[0]))
            ny = max(0, min(SH - self.rect.h, pos[1] - self._deslocamento_arrasto[1]))
            self.rect.topleft = (nx, ny)

    # metodo abstrato serve para indicar que esses métodos devem ser implementados pelas classes filhas,sem especificar nada na classe mãe
    def tecla_pressionada(self, key, uni): pass
    def rolar(self, pos, dy):   pass
    def _on_click(self, lx, ly):    pass
    def atualizar(self, dt):           pass

    # ── Desenho ──────────────────────────────────────────────────────
    def desenhar(self, tela: pygame.Surface):
        if not self.visivel:
            return
        relevo(tela, self.rect)
        # barra
        tr = pygame.Rect(self.rect.x + BORDA, self.rect.y + BORDA,
                         self.rect.w - BORDA * 2, ALTURA_JANELA)
        pygame.draw.rect(tela, TITLE_ATIVA if self.ativa else TITLE_INATIVA, tr)
        # icone
        ic = pygame.Rect(tr.x + 2, tr.y + (ALTURA_JANELA - 12) // 2, 12, 12)
        pygame.draw.rect(tela, self.cor_icone, ic)
        pygame.draw.rect(tela, PRETO, ic, 1)
        # texto do titulo
        lbl = FONTE_TITULO.render(self.titulo, True, BRANCO)
        tela.blit(lbl, (tr.x + 17, tr.y + (ALTURA_JANELA - lbl.get_height()) // 2))
        # botao de fechar
        if self.fechavel:
            cr = self.fechar_rect
            relevo(tela, cr)
            x_s = FONTE_TITULO.render("x", True, PRETO)
            tela.blit(x_s, (cr.x + (cr.w - x_s.get_width())  // 2,
                               cr.y + (cr.h - x_s.get_height()) // 2))
        # area interna
        pygame.draw.rect(tela, COR_JANELA, self.rect_interno)
        self.surf.fill(COR_JANELA)
        self._desenhar(self.surf)
        tela.blit(self.surf, self.rect_interno.topleft)

    def _desenhar(self, surf: pygame.Surface): pass


# ═══════════════════════════════════════════════════════════════════
#  GERENCIADOR DE JANELAS
# ═══════════════════════════════════════════════════════════════════
class GerenciadorJanelas:
    def __init__(self):
        self._wins: List[JanelaBase] = []   # last = top (focused)

    def adicionar(self, win: JanelaBase) -> JanelaBase:
        self._wins.append(win)
        self._focar(win)
        return win

    def obter(self, cls):
        for w in self._wins:
            if isinstance(w, cls): return w
        return None

    def _focar(self, win: JanelaBase):
        for w in self._wins: w.ativa = False
        win.ativa = True
        if win in self._wins:
            self._wins.remove(win)
        self._wins.append(win)

    def trazer_para_frente(self, win: JanelaBase): self._focar(win)

    def apertar_mouse(self, pos, btn):
        for win in reversed(self._wins):
            if win.visivel and win.rect.collidepoint(pos):
                self._focar(win)
                win.apertar_mouse(pos, btn)
                return

    def soltar_mouse(self, pos, btn):
        for w in self._wins: w.soltar_mouse(pos, btn)

    def mover_mouse(self, pos):
        for w in self._wins: w.mover_mouse(pos)

    def rolar(self, pos, dy):
        for win in reversed(self._wins):
            if win.visivel and win.rect.collidepoint(pos):
                win.rolar(pos, dy)
                return

    def tecla_pressionada(self, key, uni):
        if self._wins: self._wins[-1].tecla_pressionada(key, uni)

    def atualizar(self, dt):
        for w in self._wins: w.atualizar(dt)

    def desenhar(self, surf):
        for w in self._wins:
            if w.visivel: w.desenhar(surf)


gerenciador_janelas = GerenciadorJanelas()

# ═══════════════════════════════════════════════════════════════════
#  DEFINIÇÕES DE DADOS
# ═══════════════════════════════════════════════════════════════════

# @dataclass serve para criar classes com atributos e métodos de forma simplificada
# ele já cria o método __init__ automaticamente, e outros métodos como __repr__, __eq__, etc.

@dataclass
class ObjetoJogo:
    nome:  str
    tipo:  str       # arma / armadura / accessório / poção
    ouro:  int       # preço de compra
    ataque:   int = 0
    defesa:  int = 0
    vida:    int = 0   # HP que restora
    mana:    int = 0   # MP que restora
    descricao:  str = ''
    icone:  tuple = field(default=(200, 200, 0))

@dataclass
class FichaInimigo:
    nome:    str
    vida:      int
    ataque:     int
    defesa:    int
    exp:      int
    ouro:    int
    cor_corpo:    tuple          # cor do corpo
    cor_destaque:  tuple          # cor de destaque
    chefe:    bool   = False
    saque:    str    = ''    # chave do item, pode ser dropada ao morrer

@dataclass
class NoMapa:
    id:       int
    nome:     str
    x_mapa: int;  y_mapa: int       # posição nas coordenadas da superfície do mapa
    lista_inimigos:     List[str]     # chaves dos inimigos para encontros aleatórios
    eventos:   List[str]     # chaves dos eventos
    loja:     bool  = False
    descanso:     bool  = False # cura grátis ao chegar
    chefe:     str   = ''    # chave do chefe
    cor:      tuple = (180, 160, 120)
    visitado:  bool  = False
    derrotado:  bool  = False # chefe derrotado

@dataclass
class EventoHistoria:
    titulo:   str
    texto:    str
    escolhas: List[tuple]    # [(label, Callable)]


# ── ITENS ──────────────────────────────────────────────────────────
ITENS: dict[str, ObjetoJogo] = {
    # poções
    'poc_m':  ObjetoJogo("Poção Menor",   'poção',  8,  vida=25,  descricao="+25 HP",          icone=(255, 80, 80)),
    'poc_md':  ObjetoJogo("Poção Média",  'poção', 20,  vida=60,  descricao="+60 HP",          icone=(220,  0,  0)),
    'poc_gd':  ObjetoJogo("Poção Superior", 'poção', 40,  vida=120, descricao="+120 HP",         icone=(180,  0,  0)),
    'elixir': ObjetoJogo("Elixir",         'poção', 50,  vida=150, descricao="+150 HP",         icone=(255, 50,150)),
    'mana':   ObjetoJogo("Cristal de Mana",   'poção', 15,  mana=20,  descricao="+20 PM",          icone=( 80, 80,220)),
    'erva':   ObjetoJogo("Erva Curativa", 'poção',  5,  vida=20,  descricao="+20 HP",          icone=( 50,200, 50)),
    # armas
    'adaga':  ObjetoJogo("Adaga",         'arma', 12,  ataque=3,  descricao="ATQ +3",          icone=(200,200,210)),
    'espada':  ObjetoJogo("Espada de Ferro",     'arma', 30,  ataque=7,  descricao="ATQ +7",          icone=(170,170,210)),
    'espada_grande': ObjetoJogo("Espada Grande",     'arma', 80,  ataque=14, descricao="ATQ +14",         icone=(140,140,255)),
    'cajado':  ObjetoJogo("Cajado Mágico",    'arma', 45,  ataque=6,  descricao="ATQ +6  (magia)", icone=(180, 80,255)),
    'cimitarra': ObjetoJogo("Cimitarra", 'arma', 10, ataque=10, descricao="ATQ +10", icone=(200,180,150)),
    # armaduras
    'armadura_couro':  ObjetoJogo("Armadura de Couro", 'armadura',  20,  defesa=4, descricao="DEF +4",          icone=(140,100, 60)),
    'malha':  ObjetoJogo("Malha de Ferro",     'armadura',  60,  defesa=8, descricao="DEF +8",          icone=(160,160,180)),
    'placas':  ObjetoJogo("Armadura de Placas",   'armadura', 120,  defesa=14,descricao="DEF +14",         icone=(200,200,220)),
    'escudo': ObjetoJogo("Escudo de Madeira",  'armadura',  18,  defesa=3, descricao="DEF +3",          icone=(160,120, 60)),
    # acessórios
    'anel':   ObjetoJogo("Anel Mágico",     'acessório', 35, ataque=2, defesa=2, descricao="ATQ/DEF +2", icone=(255,200,  0)),
    'amuleto': ObjetoJogo("Amuleto Antigo", 'acessório', 80, ataque=4, defesa=4, descricao="ATQ/DEF +4", icone=(255,150,  0)),
}

ITENS_LOJA = ['poc_m', 'poc_md', 'poc_gd', 'mana', 'elixir', 'espada', 'espada_grande', 'cajado', 'armadura_couro', 'malha', 'placas', 'escudo']
# ── INIMIGOS ────────────────────────────────────────────────────────
INIMIGOS: dict[str, FichaInimigo] = {
    # nome, vida, ataque, defesa, exp, ouro, cor do corpo, cor de destaque, chefe=False, saque=''
    'gosma':  FichaInimigo("Gosma Verde",    20,  14,  1,  15,  3,  ( 60,180, 60), ( 40,220, 40), saque='poc_m'),
    'goblin': FichaInimigo("Goblin",         35,  15,  2, 25,  6,  ( 80,160, 60), ( 60,200, 50), saque='poc_md'),
    'lobo':   FichaInimigo("Lobo Terrível",      55, 14,  5, 30, 10,  (130, 90, 60), (190,150, 80), saque='poc_gd'),
    'esqueleto':   FichaInimigo("Esqueleto",       60, 22,  8, 50, 12,  (220,210,190), (180,170,150), saque='anel'),
    'orc':    FichaInimigo("Guerreiro Orc",    90, 26,  8, 55, 20,  ( 90,150, 60), ( 60,200, 40), saque='poc_md'),
    'espectro': FichaInimigo("Espectro Sombrio",  80, 28,  8, 70, 18,  ( 80, 40,120), (140, 60,200), saque='amuleto'),
    'troll':  FichaInimigo("Troll da Montanha",120, 30, 10, 90, 30,  (100,120, 80), ( 80,160, 80), saque='poc_gd'),
    'cavaleiro_sombrio':FichaInimigo("Cavaleiro Sombrio",   140, 34, 10, 200, 40,  ( 40, 40, 60), (100,100,160), saque='elixir'),
    'zeus': FichaInimigo("Dragão Zeus",300, 40, 15,200,100,  (180, 40, 40), (220, 80,  0),
                       chefe=True, saque='amuleto'),
}

# ── MAPA ────────────────────────────────────────────────────────────
# (mx, my) são posições dentro da superfície interna da JanelaMapa
NODES: dict[int, NoMapa] = {
    # id, nome, x_mapa, y_mapa, lista_inimigos, eventos, loja=False, descanso=False, chefe=''
    0: NoMapa(0, "Entrada da Floresta",      95, 220, [],                    ['viajante', 'erva'],
               loja=True, descanso=True, visitado=True, cor=(220,200,120)),
    1: NoMapa(1, "Floresta Sombria",  220, 120, ['gosma','goblin','lobo'],  ['acampamento','bau', 'viajante'],    cor=( 40,100, 40)),
    2: NoMapa(2, "Ruínas Antigas",400,  70, ['esqueleto','espectro'],          ['reliquario','armaria'],cor=(150,130,100)),
    3: NoMapa(3, "Pântano Sombrio", 195, 310, ['gosma','esqueleto'],         ['erva', 'bau'],            cor=( 60,100, 60)),
    4: NoMapa(4, "Estrada de Pedra",   360, 220, ['orc','esqueleto'],             ['altar', 'reliquario'],          cor=(130,120,110)),
    5: NoMapa(5, "Montanha",530, 140, ['orc','troll'],            ['viajante', 'armaria'],        cor=(150,140,130)),
    6: NoMapa(6, "Torre Sombria",   520, 310, ['cavaleiro_sombrio','espectro'],       ['altar'],                  cor=( 60, 50, 80)),
    7: NoMapa(7, "Covil do Dragão",680, 215, [],                        [],
               chefe='zeus', cor=(140, 40, 40)),
}
EDGES = [(0,1),(0,3),(1,2),(1,4),(3,4),(3,6),(2,5),(4,5),(5,7),(6,7)]

def vizinhos(nid: int) -> List[int]:
    return [b for a,b in EDGES if a==nid] + [a for a,b in EDGES if b==nid]

# ═══════════════════════════════════════════════════════════════════
#  JOGADOR + ESTADO DO JOGO
# ═══════════════════════════════════════════════════════════════════
class Jogador:
    def __init__(self):
        self.nome    = "Herói"
        self.vida      = 100;  self.vida_maxima = 100
        self.mana      = 40;   self.mana_maxima = 40
        self.ataque     = 8
        self.defesa    = 3
        self.exp      = 0;    self.exp_proximo = 25
        self.nivel   = 1
        self.ouro    = 30
        self.inventario:  List[str] = ['adaga', 'poc_m', 'poc_md', 'poc_gd']
        self.equipado = {'arma': None, 'armadura': None, 'acessório': None}

    def ataque_total(self):
        b = self.ataque
        for s in ('arma', 'acessório'):
            if self.equipado[s]: b += ITENS[self.equipado[s]].ataque
        return b

    def defesa_total(self):
        b = self.defesa
        for s in ('armadura', 'acessório'):
            if self.equipado[s]: b += ITENS[self.equipado[s]].defesa
        return b

    def curar(self, n):
        gained = min(n, self.vida_maxima - self.vida)
        self.vida += gained
        return gained

    def restaurar_mana(self, n):
        gained = min(n, self.mana_maxima - self.mana)
        self.mana += gained
        return gained

    def ganhar_experiencia(self, n) -> List[str]:
        self.exp += n
        mensagens = []
        while self.exp >= self.exp_proximo:
            self.exp      -= self.exp_proximo
            self.nivel   += 1
            self.exp_proximo  = int(self.exp_proximo * 1.6)
            self.vida_maxima  += 15;  self.vida  = self.vida_maxima
            self.mana_maxima  += 10;  self.mana  = self.mana_maxima
            self.ataque     += 2
            self.defesa    += 2
            mensagens.append(f"Subiu de nível! Agora seu nível é {self.nivel}")
        return mensagens

    def pocoes(self) -> List[str]:
        return [k for k in self.inventario if ITENS[k].tipo == 'poção']


class EstadoJogo:
    def __init__(self):
        self.jogador       = Jogador()
        self.no         = 0       # id do nó de mapa atual
        self.registro: List[str] = [
            "Bem-vindo à Busca do Reino Antigo!",
            "Abra o Mapa e viaje para um local.",
            "Derrote o Dragão Antigo no Covil do Dragão para vencer!"
        ]
        self.em_combate    = False
        self.fim_de_jogo    = False
        self.vitoria      = False
        self.evento_pendente = None

    def mensagem(self, texto: str):
        self.registro.append(texto)
        lw = gerenciador_janelas.obter(JanelaRegistro)
        if lw: lw.rolar_ate_fim()

estado_jogo = EstadoJogo()

# ═══════════════════════════════════════════════════════════════════
#  EVENTOS DA HISTÓRIA
# ═══════════════════════════════════════════════════════════════════
EVENTOS: dict[str, EventoHistoria] = {}

def _evento_possivel(nome_variavel_evento, titulo_evento, texto, escolhas):
    EVENTOS[nome_variavel_evento] = EventoHistoria(titulo_evento, texto, escolhas)

def _recompensar_item(k):
    estado_jogo.jogador.inventario.append(k)
    estado_jogo.mensagem(f"Você encontrou: {ITENS[k].nome}!")

def _recompensar_ouro(n):
    estado_jogo.jogador.ouro += n
    estado_jogo.mensagem(f"Você encontrou {n} ouro!")

_evento_possivel('bau',    "Baú de Tesouro",
    "Você encontra um baú antigo meio enterrado na lama. Um cadeado enferrujado o mantem fechado. Tentar abri-lo?",
    [("Abrir",  lambda: _recompensar_item(random.choice(['poc_md','mana','malha']))),
     ("Deixar", lambda: estado_jogo.mensagem("Você deixa o baú intacto."))])

_evento_possivel('acampamento',     "Acampamento Abandonado",
    "Um acampamento de viajante — as brasas ainda brilham. Descansar aqui para recuperar HP?",
    [("Descansar (+40 HP)", lambda: estado_jogo.mensagem(f"Você descansa. +{estado_jogo.jogador.curar(40)} HP recuperados.")),
     ("Continuar",       lambda: None)])

_evento_possivel('reliquario',"Relíquário Antigo",
    "Um baú de pedra zumbe com mágia residual. Estátuas estranhas cobrem sua superfície. Abrir?",
    [("Abrir",  lambda: _recompensar_item(random.choice(['poc_gd','elixir','espada_grande','placas']))),
     ("Deixar", lambda: None)])

_evento_possivel('altar',    "Altar Misterioso",
    "Um altar brilhante pulsa com energia arcána. Sua inscrição lê: 'Poder para os dignos.' Tocar?",
    [("Tocar",  lambda: (estado_jogo.jogador.restaurar_mana(estado_jogo.jogador.mana_maxima), estado_jogo.mensagem("Seu PM foi totalmente restaurado!"))),
     ("Deixar",     lambda: None)])

_evento_possivel('erva',     "Ervas de Cura",
    "Você encontra aglomerados de ervas luminosas na margem do pântano. Você pega elas?",
    [("Colher",  lambda: estado_jogo.mensagem(f"Você come as ervas. +{estado_jogo.jogador.curar(20)} HP.")),
     ("Deixar",    lambda: None)])

_evento_possivel('armaria',   "Armém Oculta",
    "Atrás de uma parede em runa você avista um suporte de armas. Uma espada ainda brilha na poeira. Pegar?",
    [("Pegar Espada",  lambda: _recompensar_item('espada')),
     ("Deixar",       lambda: None)])

_evento_possivel('viajante', "Viajante Caído",
    "Você encontra um viajante ferido no caminho. Ele coloca sua bolsa de moedas em suas mãos antes de perder a consciência.",
    [("Pegar o Ouro", lambda: _recompensar_ouro(100)),
     ("Deixar",      lambda: estado_jogo.mensagem("Você deixa o ouro com ele."))])


# ═══════════════════════════════════════════════════════════════════
#  JANELA DE REGISTRO
# ═══════════════════════════════════════════════════════════════════
class JanelaRegistro(JanelaBase):
    def __init__(self):
        super().__init__(0, SH - 182, 710, 157,
                         "Registro de Mensagens", fechavel=False, cor_icone=(0,180,180))
        self._rolar = 0
        self._LH     = 16

    def rolar_ate_fim(self):
        vis = (self._altura_interna - 8) // self._LH
        self._rolar = max(0, len(estado_jogo.registro) - vis)

    def rolar(self, pos, dy):
        vis = (self._altura_interna - 8) // self._LH
        self._rolar = max(0, min(max(0, len(estado_jogo.registro) - vis), self._rolar - dy))

    def _desenhar(self, surf):
        relevo_baixo(surf, surf.get_rect().inflate(-4, -4), (18, 22, 18))
        vis   = (self._altura_interna - 8) // self._LH
        lines = estado_jogo.registro[self._rolar: self._rolar + vis]
        for i, line in enumerate(lines):
            cor = BRANCO if i == len(lines) - 1 else (160, 195, 160)
            escrever(surf, FONTE_PEQUENA, line, 8, 6 + i * self._LH, cor)


# ═══════════════════════════════════════════════════════════════════
#  JANELA DE PERSONAGEM
# ═══════════════════════════════════════════════════════════════════
class JanelaEstatisticas(JanelaBase):
    def __init__(self):
        super().__init__(SW - 215, 5, 210, 300,
                         "Personagem", fechavel=False, cor_icone=LARANJA)

    def _desenhar(self, surf):
        p  = estado_jogo.jogador
        y  = 8

        escrever_centralizado(surf, FONTE_NEGRITO, p.nome, self._largura_interna // 2, y, TITLE_ATIVA);        y += 20
        escrever_centralizado(surf, FONTE_PEQUENA, f"Level {p.nivel}   XP {p.exp}/{p.exp_proximo}",
              self._largura_interna // 2, y, ESCURO);                               y += 16
        barra_horizontal(surf, (8, y, self._largura_interna - 16, 7), p.exp, p.exp_proximo,
             COR_XP, (30,30, 0));                                     y += 13

        escrever(surf, FONTE_PEQUENA, f"HP  {p.vida}/{p.vida_maxima}", 8, y);               y += 16
        barra_horizontal(surf, (8, y, self._largura_interna - 16, 12), p.vida, p.vida_maxima);       y += 18
        escrever(surf, FONTE_PEQUENA, f"PM  {p.mana}/{p.mana_maxima}", 8, y);               y += 16
        barra_horizontal(surf, (8, y, self._largura_interna - 16, 12), p.mana, p.mana_maxima,
             COR_MANA, (0, 0, 60));                                     y += 18

        pygame.draw.line(surf, CINZA, (8, y), (self._largura_interna - 8, y));     y += 8
        atk_bonus = p.ataque_total() - p.ataque
        def_bonus = p.defesa_total() - p.defesa
        escrever(surf, FONTE_MEDIA, f"ATQ  {p.ataque_total():>3}  (+{atk_bonus})", 8, y); y += 18
        escrever(surf, FONTE_MEDIA, f"DEF  {p.defesa_total():>3}  (+{def_bonus})", 8, y); y += 18
        escrever(surf, FONTE_MEDIA, f"Ouro {p.ouro:>4}", 8, y, (180,150,0));         y += 20

        pygame.draw.line(surf, CINZA, (8, y), (self._largura_interna - 8, y));     y += 6
        escrever(surf, FONTE_MINUSCULA, "Equipado:", 8, y, ESCURO);                       y += 14
        for slot in ('arma', 'armadura', 'acessório'):
            eq  = p.equipado[slot]
            nm  = ITENS[eq].nome if eq else "—"
            cor = PRETO if eq else CINZA
            escrever(surf, FONTE_MINUSCULA, f"  {slot[:3].upper()}: {nm}", 8, y, cor); y += 13


# ═══════════════════════════════════════════════════════════════════
#  JANELA DE MAPA
# ═══════════════════════════════════════════════════════════════════
class JanelaMapa(JanelaBase):
    _R = 22   # raio do círculo do nó

    def __init__(self):
        super().__init__(205, 5, 840, 500,
                         "Mapa Mundo  —  clique em um nó adjacente (brilhante) para viajar",
                         fechavel=False, cor_icone=(0,120,220))
        self._hover = -1

    # ── interaction ───────────────────────────────────────────────
    def _on_click(self, lx, ly):
        if estado_jogo.em_combate or estado_jogo.fim_de_jogo or estado_jogo.vitoria:
            return
        for nid, no in NODES.items():
            if (lx - no.x_mapa) ** 2 + (ly - no.y_mapa) ** 2 <= self._R ** 2:
                if nid != estado_jogo.no and nid in vizinhos(estado_jogo.no):
                    self.viajar_para(nid)
                    return

    def mover_mouse(self, pos):
        super().mover_mouse(pos)
        lx = pos[0] - self.rect_interno.x
        ly = pos[1] - self.rect_interno.y
        self._hover = -1
        for nid, no in NODES.items():
            if (lx - no.x_mapa) ** 2 + (ly - no.y_mapa) ** 2 <= self._R ** 2:
                self._hover = nid
                break

    def viajar_para(self, nid: int):
        no = NODES[nid]

        # --- BLOQUEIO DO DRAGÃO ---
        if no.chefe == 'zeus':
            # Verifica se os nós de 0 a 6 já foram visitados
            todas_visitadas = all(NODES[i].visitado for i in range(7))
            if estado_jogo.jogador.nivel < 5 or not todas_visitadas:
                estado_jogo.mensagem("Acesso Negado! O Covil do Dragão exige Nível 5 e explorar todo o mapa.")
                return
        # --------------------------

        no.visitado = True
        estado_jogo.no = nid
        estado_jogo.mensagem(f"Você viaja para {no.nome}.")

        if no.descanso:
            curared = estado_jogo.jogador.curar(estado_jogo.jogador.vida_maxima)
            estado_jogo.jogador.mana = estado_jogo.jogador.mana_maxima
            if curared: estado_jogo.mensagem("Você descansa na cidade. HP e PM totalmente restaurados.")

        if no.chefe and not no.derrotado:
            self.iniciar_combate(no.chefe, chefe=True)
            return

        teve_combate = False
        if no.lista_inimigos:
            if random.random() < 0.8:  # 80% chance de combate
                self.iniciar_combate(random.choice(no.lista_inimigos))
                teve_combate = True
            
        if no.eventos:
            evento_sorteado = EVENTOS.get(random.choice(no.eventos))
            if evento_sorteado:
                if teve_combate:
                    estado_jogo.evento_pendente = evento_sorteado 
                else:
                    gerenciador_janelas.adicionar(JanelaEvento(evento_sorteado))

        if no.loja:
            gerenciador_janelas.adicionar(JanelaLoja())

    def iniciar_combate(self, key: str, chefe=False):
        estado_jogo.em_combate = True
        gerenciador_janelas.adicionar(JanelaCombate(key, chefe))

    # ── desenho ────────────────────────────────────────────────────
    def _desenhar(self, surf):
        surf.fill((28, 22, 16))

        # arestas
        for a, b in EDGES:
            na, nb_ = NODES[a], NODES[b]
            reach = (a == estado_jogo.no or b == estado_jogo.no)
            cor   = (180,155, 95) if reach else (75, 65, 50)
            w_    = 3 if reach else 1
            pygame.draw.line(surf, cor, (na.x_mapa, na.y_mapa), (nb_.x_mapa, nb_.y_mapa), w_)

        # nodes
        adj = vizinhos(estado_jogo.no)
        for nid, no in NODES.items():
            r = self._R
            if nid == estado_jogo.no:
                cor    = (255, 210, 60)
                border = 3
            elif no.derrotado:
                cor    = (80, 80, 80)
                border = 1
            elif nid in adj:
                cor    = no.cor
                border = 2
                pygame.draw.circle(surf, (200,200,100), (no.x_mapa, no.y_mapa), r + 5, 1)
            else:
                cor    = tuple(max(0, c // 3) for c in no.cor)
                border = 1

            if nid == self._hover and nid in adj and nid != estado_jogo.no:
                pygame.draw.circle(surf, BRANCO, (no.x_mapa, no.y_mapa), r + 3, 2)

            pygame.draw.circle(surf, cor,   (no.x_mapa, no.y_mapa), r)
            pygame.draw.circle(surf, PRETO, (no.x_mapa, no.y_mapa), r, border)

            # indicador de chefe
            if no.chefe and not no.derrotado:
                pygame.draw.circle(surf, VERMELHO, (no.x_mapa + r - 7, no.y_mapa - r + 7), 7)
                lbl = FONTE_MINUSCULA.render("!", True, BRANCO)
                surf.blit(lbl, (no.x_mapa + r - 7 - lbl.get_width()  // 2,
                                no.y_mapa - r + 7 - lbl.get_height() // 2))

            name_col = (255,230, 90) if nid == estado_jogo.no else BRANCO
            if nid not in adj and nid != estado_jogo.no and not no.visitado:
                name_col = CINZA
            lbl = FONTE_PEQUENA.render(no.nome, True, name_col)
            surf.blit(lbl, (no.x_mapa - lbl.get_width() // 2, no.y_mapa + r + 4))

        if not estado_jogo.em_combate:
            escrever(surf, FONTE_MINUSCULA, "Clique em um nó brilhante para viajar", 8, self._altura_interna - 18, (140,140,100))


# ═══════════════════════════════════════════════════════════════════
#  JANELA DE COMBATE
# ═══════════════════════════════════════════════════════════════════
class JanelaCombate(JanelaBase):
    _ACOES = [("Atacar",'atq'), ("Magia",'magia'), ("Objeto",'item'), ("Fugir",'fugir')]

    def __init__(self, enemy_key: str, chefe=False):
        inimigo = INIMIGOS[enemy_key]
        titulo = ("⚔ CHEFE — " if chefe else "⚔ ") + inimigo.nome
        super().__init__(SW//2 - 250, SH//2 - 210, 500, 420,
                         titulo, fechavel=False, cor_icone=VERMELHO)
        self.chave_inimiga    = enemy_key
        self.ficha_inimiga    = inimigo
        self.chefe    = chefe
        self.vida_inimigo     = inimigo.vida
        self.fase   = 'jogador'   # 'jogador' | 'fim'
        self.mensagens: List[str] = [f"Um {inimigo.nome} aparece!"]
        self.tempo_flash = 0.0
        self.cor_flash = None
        self.tremor   = 0.0
        self.mostra_itens = False
        self._botoes   = []         # preenchido no método de desenho
        self.botao_apertado = None

    # ── ajudantes ───────────────────────────────────────────────────
    def _mensagem(self, texto): self.mensagens = (self.mensagens + [texto])[-6:]

    # ── ações ───────────────────────────────────────────────────
    def _on_click(self, lx, ly):
        if self.fase != 'jogador':
            return
        if self.mostra_itens:
            # linhas de itens
            pots = estado_jogo.jogador.pocoes()
            for i, key in enumerate(pots):
                if pygame.Rect(18, 272 + i * 26, self._largura_interna - 36, 24).collidepoint(lx, ly):
                    self._usar_item(key); return
            # botão de voltar
            if pygame.Rect(18, self._altura_interna - 44, 80, 30).collidepoint(lx, ly):
                self.mostra_itens = False
            return
        for r, act in self._botoes:
            if r.collidepoint(lx, ly):
                self.botao_apertado = act
                self._acao(act)
                return

    def soltar_mouse(self, pos, btn):
        super().soltar_mouse(pos, btn)
        self.botao_apertado = None

    def _acao(self, action):
        p = estado_jogo.jogador
        if action == 'atq':
            dmg = max(1, p.ataque_total() - self.ficha_inimiga.defesa + random.randint(-2, 4))
            self.vida_inimigo = max(0, self.vida_inimigo - dmg)
            self._mensagem(f"Você golpeia por {dmg} de dano!")
            self.tremor   = 0.3
            self.cor_flash = VERMELHO;  self.tempo_flash = 0.3
            if self.vida_inimigo == 0: self._finalizar(True); return

        elif action == 'magia':
            if p.mana < 20: self._mensagem("PM insuficiente!"); return
            p.mana -= 20
            dmg = max(1, p.ataque_total() - self.ficha_inimiga.defesa // 2 + random.randint(0, 6))
            self.vida_inimigo = max(0, self.vida_inimigo - dmg)
            self._mensagem(f"Raio Mágico — {dmg} de dano!")
            self.cor_flash = (80,80,255); self.tempo_flash = 0.3
            if self.vida_inimigo == 0: self._finalizar(True); return

        elif action == 'item':
            if not estado_jogo.jogador.pocoes(): self._mensagem("Nenhum item usável!"); return
            self.mostra_itens = True;  return

        elif action == 'fugir':
            if self.chefe: self._mensagem("Não pode fugir de um chefe!"); return
            if random.random() < 0.25:
                estado_jogo.em_combate = False
                estado_jogo.mensagem("Você fugiu do combate!")
                self.visivel = False
                return
            else:
                self._mensagem("Não conseguiu escapar!")

        self._turno_inimigo()

    def _usar_item(self, key):
        p    = estado_jogo.jogador
        objeto = ITENS[key]
        if objeto.vida: self._mensagem(f"{objeto.nome}: +{p.curar(objeto.vida)} HP")
        if objeto.mana: self._mensagem(f"{objeto.nome}: +{p.restaurar_mana(objeto.mana)} PM")
        estado_jogo.jogador.inventario.remove(key)
        self.mostra_itens = False


    def _turno_inimigo(self):
        p    = estado_jogo.jogador
        inimigo    = self.ficha_inimiga
        # chefe especial: ocasionalmente causa o dobro de dano
        if self.chefe and random.random() < 0.30:
            dmg = max(1, inimigo.ataque * 2 - p.defesa_total() + random.randint(0, 8))
            if p.vida == 1:
                self._finalizar(False)
                return

            if (p.vida - dmg) <= 0:
                p.vida = 1
                self._mensagem("Você está com pouca vida! Mais uma pancada será fatal!")
                return

            p.vida -= dmg
            self._mensagem(f"Sopro de Fogo! Você recebe {dmg} de dano!")
        else:
            dmg = max(1, inimigo.ataque - p.defesa_total() + random.randint(-2, 4))
            if p.vida == 1: 
                self._finalizar(False)
                return
            if (p.vida - dmg) <= 0:
                p.vida = 1
                self._mensagem("Você está com pouca vida! Mais uma pancada será fatal!")
                return
            p.vida -= dmg
            self._mensagem(f"{inimigo.nome} acerta você por {dmg} de dano!")    

        

    def _finalizar(self, won: bool):
        self.fase   = 'fim'
        estado_jogo.em_combate = False
        if won:
            p = estado_jogo.jogador
            p.ouro += self.ficha_inimiga.ouro
            lvl_msgs = p.ganhar_experiencia(self.ficha_inimiga.exp)
            estado_jogo.mensagem(f"Vitória! +{self.ficha_inimiga.exp} PE, +{self.ficha_inimiga.ouro} ouro.")
            for m in lvl_msgs: estado_jogo.mensagem(m)
            if self.ficha_inimiga.saque and random.random() < 0.50:
                p.inventario.append(self.ficha_inimiga.saque)
                estado_jogo.mensagem(f"Recompensa obtida: {ITENS[self.ficha_inimiga.saque].nome}!")
            if self.chefe:
                NODES[estado_jogo.no].derrotado = True
                if estado_jogo.no == 7:
                    estado_jogo.vitoria = True
            self._mensagem("Pressione qualquer tecla para continuar...")
        else:
            estado_jogo.fim_de_jogo = True
            estado_jogo.mensagem("Você foi derrotado...")
            self._mensagem("FIM DE JOGO")

    # ── tecla: fechar janela após combate ──────────────────────
    def tecla_pressionada(self, key, uni):
        if self.fase == 'fim' and not estado_jogo.fim_de_jogo:
            self.visivel = False
            if estado_jogo.evento_pendente:
                gerenciador_janelas.adicionar(JanelaEvento(estado_jogo.evento_pendente))
                estado_jogo.evento_pendente = None # Limpa depois de usar

    # ── atualizar ────────────────────────────────────────────────────
    def atualizar(self, dt):
        if self.tempo_flash > 0: self.tempo_flash -= dt
        if self.tremor   > 0: self.tremor   -= dt

    # ── desenho ────────────────────────────────────────────────────
    def _draw_enemy(self, surf, ex, ey, dead=False):
        inimigo = self.ficha_inimiga
        sx = ex + (random.randint(-4, 4) if self.tremor > 0 else 0)
        sy = ey

        # corpo
        pygame.draw.rect(surf, inimigo.cor_corpo,   (sx,    sy,    88, 88))
        pygame.draw.rect(surf, inimigo.cor_destaque, (sx+10, sy+18, 68, 30))
        pygame.draw.rect(surf, PRETO,    (sx,    sy,    88, 88), 2)

        # olhos
        for ox in (24, 58):
            pygame.draw.circle(surf, PRETO, (sx + ox, sy + 28), 9)
            pygame.draw.circle(surf, BRANCO, (sx + ox, sy + 28), 6)
            if not dead:
                pygame.draw.circle(surf, PRETO, (sx + ox + 2, sy + 26), 3)

        # boca
        if dead:
            pygame.draw.arc(surf, PRETO, (sx+22, sy+56, 44, 18), 0, math.pi, 3)
        else:
            pygame.draw.arc(surf, PRETO, (sx+22, sy+58, 44, 14), math.pi, 2*math.pi, 3)

        # sobreposição de flash
        if self.tempo_flash > 0 and self.cor_flash:
            ov = pygame.Surface((88, 88), pygame.SRCALPHA)
            ov.fill((*self.cor_flash, int(170 * self.tempo_flash / 0.3)))
            surf.blit(ov, (sx, sy))

    def _desenhar(self, surf):
        p    = estado_jogo.jogador
        dead = (self.fase == 'fim' and estado_jogo.fim_de_jogo)

        # ── inimigo (painel esquerdo) ─────────────────────────────────
        self._draw_enemy(surf, 45, 35, dead=(self.vida_inimigo == 0))
        e_col = VERMELHO if self.chefe else ESCURO
        escrever_centralizado(surf, FONTE_NEGRITO, self.ficha_inimiga.nome, 89, 128, e_col)
        barra_horizontal(surf, (45, 144, 88, 10), self.vida_inimigo, self.ficha_inimiga.vida, VIDA_BAIXA, (60,0,0))
        escrever_centralizado(surf, FONTE_MINUSCULA, f"{self.vida_inimigo}/{self.ficha_inimiga.vida}", 89, 156, ESCURO)

        # ── estatísticas do jogador (painel direito) ─────────────────
        px = 220
        escrever(surf, FONTE_NEGRITO, p.nome, px, 35)
        escrever(surf, FONTE_PEQUENA, f"HP  {p.vida}/{p.vida_maxima}", px, 58)
        barra_horizontal(surf, (px, 76, 140, 13), p.vida, p.vida_maxima)
        escrever(surf, FONTE_PEQUENA, f"MP  {p.mana}/{p.mana_maxima}", px, 98)
        barra_horizontal(surf, (px, 116, 140, 13), p.mana, p.mana_maxima, COR_MANA, (0,0,60))
        escrever(surf, FONTE_PEQUENA, f"ATK {p.ataque_total()}  DEF {p.defesa_total()}", px, 140)

        # ── messages ─────────────────────────────────────────────
        relevo_baixo(surf, pygame.Rect(8, 168, self._largura_interna - 16, 90), (20,26,20))
        for i, m in enumerate(self.mensagens[-5:]):
            cor = BRANCO if i == len(self.mensagens[-5:]) - 1 else (150,180,150)
            escrever(surf, FONTE_PEQUENA, m, 14, 173 + i * 17, cor)

        # ── action buttons ───────────────────────────────────────
        self._botoes = []
        if self.fase == 'jogador' and not self.mostra_itens:
            bw, bh   = 104, 34
            n        = len(self._ACOES)
            total_w  = n * bw + (n - 1) * 8
            bx0      = (self._largura_interna - total_w) // 2
            by       = self._altura_interna - 50
            for i, (rotulo, act) in enumerate(self._ACOES):
                bx  = bx0 + i * (bw + 8)
                r   = pygame.Rect(bx, by, bw, bh)
                ok  = True
                if act == 'magia':  ok = p.mana >= 10
                if act == 'item': ok = bool(p.pocoes())
                botao_janela(surf, r, rotulo,
                           apertado=(self.botao_apertado == act), ligado=ok)
                self._botoes.append((r, act))

        elif self.fase == 'jogador' and self.mostra_itens:
            escrever(surf, FONTE_NEGRITO, 'Qual item usar?', 18, 262, ESCURO)
            pots = p.pocoes()
            if not pots:
                escrever(surf, FONTE_PEQUENA, '(nenhum)', 18, 284, CINZA)
            for i, key in enumerate(pots):
                ir = pygame.Rect(18, 272 + i * 26, self._largura_interna - 36, 24)
                relevo(surf, ir)
                escrever(surf, FONTE_MEDIA, f"{ITENS[key].nome}  —  {ITENS[key].descricao}", 24, 275 + i * 26)
            botao_janela(surf, pygame.Rect(18, self._altura_interna - 44, 80, 30), "Voltar")

        elif self.fase == 'fim' and not estado_jogo.fim_de_jogo:
            escrever_centralizado(surf, FONTE_NEGRITO, "Pressione qualquer tecla para continuar", self._largura_interna//2, self._altura_interna-36, VERDE)
        elif self.fase == 'fim' and estado_jogo.fim_de_jogo:
            escrever_centralizado(surf, FONTE_GRANDE, "FIM  DE  JOGO", self._largura_interna//2, self._altura_interna-36, VERMELHO)


# ═══════════════════════════════════════════════════════════════════
#  JANELA DE INVENTÁRIO
# ═══════════════════════════════════════════════════════════════════
class JanelaInventario(JanelaBase):
    _COLS = 4
    _CELL = 76

    def __init__(self):
        super().__init__(220, 130, 340, 390,
                         "Inventário  (I para fechar)", fechavel=True,
                         cor_icone=(160,120,60))
        self._sel = -1

    def _on_click(self, lx, ly):
        items = estado_jogo.jogador.inventario
        for i in range(len(items)):
            row, cor = divmod(i, self._COLS)
            if pygame.Rect(8 + cor * self._CELL, 8 + row * self._CELL,
                           self._CELL - 4, self._CELL - 4).collidepoint(lx, ly):
                self._sel = i; return

        if 0 <= self._sel < len(items):
            eq_r  = pygame.Rect(8,   self._altura_interna - 42, 100, 30)
            drp_r = pygame.Rect(116, self._altura_interna - 42,  80, 30)
            if eq_r.collidepoint(lx, ly):  self._equipar_ou_usar()
            if drp_r.collidepoint(lx, ly): self._largar()

    def _equipar_ou_usar(self):
        p = estado_jogo.jogador
        if not (0 <= self._sel < len(p.inventario)): return
        key  = p.inventario[self._sel]
        objeto = ITENS[key]
        if objeto.tipo == 'poção':
            if objeto.vida: estado_jogo.mensagem(f"Usou {objeto.nome}: +{p.curar(objeto.vida)} HP")
            if objeto.mana: estado_jogo.mensagem(f"Usou {objeto.nome}: +{p.restaurar_mana(objeto.mana)} PM")
        else:
            old = p.equipado.get(objeto.tipo)
            if old: p.inventario.append(old)
            p.equipado[objeto.tipo] = key
            estado_jogo.mensagem(f"Equipou {objeto.nome}.")
        p.inventario.pop(self._sel)
        self._sel = -1

    def _largar(self):
        p = estado_jogo.jogador
        if not (0 <= self._sel < len(p.inventario)): return
        key = p.inventario.pop(self._sel)
        estado_jogo.mensagem(f"Largou {ITENS[key].nome}.")
        self._sel = -1

    def _desenhar(self, surf):
        items = estado_jogo.jogador.inventario
        for i, key in enumerate(items):
            row, cor = divmod(i, self._COLS)
            r    = pygame.Rect(8 + cor * self._CELL, 8 + row * self._CELL,
                               self._CELL - 4, self._CELL - 4)
            objeto = ITENS[key]
            if i == self._sel:
                pygame.draw.rect(surf, FUNDO_SELECAO, r)
            else:
                relevo_baixo(surf, r, (230,228,220))
            ic = pygame.Rect(r.x + 18, r.y + 8, 32, 32)
            pygame.draw.rect(surf, objeto.icone, ic)
            pygame.draw.rect(surf, PRETO, ic, 1)
            escrever_centralizado(surf, FONTE_MINUSCULA, objeto.tipo[0].upper(), r.x + self._CELL//2 - 2, r.y + 14, PRETO)
            nm_col = FONTE_SELECAO if i == self._sel else PRETO
            nm = objeto.nome if len(objeto.nome) <= 10 else objeto.nome[:9] + "."
            escrever_centralizado(surf, FONTE_MINUSCULA, nm, r.centerx, r.y + 46, nm_col)

        # Painel de Informação
        info_y = self._altura_interna - 96
        pygame.draw.line(surf, CINZA, (4, info_y), (self._largura_interna - 4, info_y))
        if 0 <= self._sel < len(items):
            key  = items[self._sel]
            objeto = ITENS[key]
            escrever(surf, FONTE_MEDIA, objeto.nome, 8, info_y + 6, TITLE_ATIVA)
            escrever(surf, FONTE_PEQUENA, objeto.descricao, 8, info_y + 24, ESCURO)
            escrever(surf, FONTE_MINUSCULA, f"Valor: {objeto.ouro}", 8, info_y + 44, (160,140,0))
            lbl = "Usar" if objeto.tipo == 'poção' else "Equipar"
            y_botao = self._altura_interna - 36
            botao_janela(surf, pygame.Rect(8,   y_botao, 100, 30), lbl)
            botao_janela(surf, pygame.Rect(116, y_botao,  80, 30), "Largar")
        else:
            escrever(surf, FONTE_PEQUENA, "Clique em um item para selecioná-lo.", 8, info_y + 12, CINZA)


# ═══════════════════════════════════════════════════════════════════
#  JANELA DE LOJA
# ═══════════════════════════════════════════════════════════════════
class JanelaLoja(JanelaBase):
    def __init__(self):
        # calcula altura inicial baseada no número de itens disponíveis
        try:
            linhas_iniciais = len(ITENS_LOJA)
        except Exception:
            linhas_iniciais = 6
        # cada linha ocupa ~30px; adiciona margem e espaço para botões
        h = max(300, 120 + linhas_iniciais * 30)
        h = min(800, h)
        super().__init__(310, 80, 370, h,
                         "Mercador", fechavel=True, cor_icone=(200,180,0))
        self._sel      = 0
        self._sell     = False
        self._notice   = ""

    def itens(self): return ITENS_LOJA if not self._sell else estado_jogo.jogador.inventario

    def _on_click(self, lx, ly):
        p = estado_jogo.jogador
        # abas
        if pygame.Rect(8,  8, 80, 26).collidepoint(lx, ly):
            self._sell = False; self._sel = 0; return
        if pygame.Rect(96, 8, 80, 26).collidepoint(lx, ly):
            self._sell = True;  self._sel = 0; return

        items = self.itens()
        for i, key in enumerate(items):
            if pygame.Rect(8, 42 + i * 30, self._largura_interna - 16, 28).collidepoint(lx, ly):
                self._sel = i; return

        # botão de ação
        if pygame.Rect(8, self._altura_interna - 44, 130, 32).collidepoint(lx, ly):
            items = self.itens()
            if 0 <= self._sel < len(items):
                key  = items[self._sel]
                objeto = ITENS[key]
                if not self._sell:
                    cost = objeto.ouro
                    if p.ouro >= cost:
                        p.ouro -= cost
                        p.inventario.append(key)
                        self._notice = f"Comprou {objeto.nome}!"
                    else:
                        self._notice = "Ouro insuficiente!"
                else:
                    gain = max(1, objeto.ouro // 2)
                    p.ouro += gain
                    p.inventario.remove(key)
                    if self._sel >= len(p.inventario): self._sel = max(0, len(p.inventario)-1)
                    self._notice = f"Vendeu por {gain} po."

    def _desenhar(self, surf):
        # redimensiona a janela se o número de itens atual mudou
        p = estado_jogo.jogador
        itens_atuais = self.itens()
        try:
            linhas = len(itens_atuais)
        except Exception:
            linhas = 0
        altura_necessaria = max(300, 120 + linhas * 30)
        altura_necessaria = min(800, altura_necessaria)
        if altura_necessaria != self.rect.h:
            self.rect.h = altura_necessaria
            self._largura_interna = self.rect.w - BORDA * 2
            self._altura_interna = self.rect.h - BORDA * 2 - ALTURA_JANELA
            self.surf = pygame.Surface((self._largura_interna, self._altura_interna))
        # abas
        botao_janela(surf, pygame.Rect(8,  8, 80, 26), 'Comprar',
                   apertado=not self._sell, fonte=FONTE_MEDIA)
        botao_janela(surf, pygame.Rect(96, 8, 80, 26), 'Vender',
                   apertado=self._sell, fonte=FONTE_MEDIA)
        escrever(surf, FONTE_PEQUENA, f"Ouro: {p.ouro}", 200, 14, (180,150,0))

        items = self.itens()
        for i, key in enumerate(items):
            objeto  = ITENS[key]
            
            r     = pygame.Rect(8, 42 + i * 30, self._largura_interna - 16, 28)
            selecionado   = (i == self._sel)
            if selecionado:
                pygame.draw.rect(surf, FUNDO_SELECAO, r)
            else:
                relevo(surf, r)
            fg = FONTE_SELECAO if selecionado else PRETO
            sg = (180,180,200) if selecionado else CINZA
            preco = objeto.ouro if not self._sell else max(1, objeto.ouro // 2)
            escrever(surf, FONTE_MEDIA, objeto.nome, 16, 45 + i * 30, fg)
            escrever(surf, FONTE_MINUSCULA, objeto.descricao, 165, 48 + i * 30, sg)
            escrever(surf, FONTE_MEDIA, f"{preco}g", self._largura_interna - 48, 45 + i * 30, AMARELO if not selecionado else (255,230,80))

        pygame.draw.line(surf, CINZA, (8, self._altura_interna - 53), (self._largura_interna - 8, self._altura_interna - 53))
        lbl = 'Comprar' if not self._sell else 'Vender'
        botao_janela(surf, pygame.Rect(8, self._altura_interna - 44, 130, 32), lbl, fonte=FONTE_NEGRITO)
        if self._notice:
            escrever(surf, FONTE_PEQUENA, self._notice, 148, self._altura_interna - 36, ESCURO)


# ═══════════════════════════════════════════════════════════════════
#  JANELA DE EVENTO / HISTÓRIA
# ═══════════════════════════════════════════════════════════════════
class JanelaEvento(JanelaBase):
    def __init__(self, evt: EventoHistoria):
        super().__init__(SW//2 - 210, SH//2 - 140, 420, 280,
                         evt.titulo, fechavel=False, cor_icone=LARANJA)
        self.evt = evt

    def _on_click(self, lx, ly):
        for i, (rotulo, fn) in enumerate(self.evt.escolhas):
            r = pygame.Rect(18 + i * 160, self._altura_interna - 50, 140, 38)
            if r.collidepoint(lx, ly):
                fn()
                self.visivel = False
                return

    def _desenhar(self, surf):
        lines = textwrap.wrap(self.evt.texto, 52)
        for i, line in enumerate(lines):
            escrever(surf, FONTE_MEDIA, line, 14, 14 + i * 21, ESCURO)

        pygame.draw.line(surf, CINZA, (8, self._altura_interna - 60), (self._largura_interna - 8, self._altura_interna - 60))
        for i, (rotulo, fn) in enumerate(self.evt.escolhas):
            botao_janela(surf, pygame.Rect(18 + i * 160, self._altura_interna - 50, 140, 38), rotulo, fonte=FONTE_NEGRITO)


# ═══════════════════════════════════════════════════════════════════
#  BARRA DE TAREFAS
# ═══════════════════════════════════════════════════════════════════
ALTURA_BARRA_TAREFAS   = 28
LARGURA_BOTAO_TAREFA = 105
_ITENS_BARRA_TAREFAS = [
    ("Mapa",       JanelaMapa),
    ("Inventário", JanelaInventario),
    ("Personagem",     JanelaEstatisticas),
    ("Loja",      JanelaLoja),
    ("Registro",   JanelaRegistro),
]

def desenhar_barra_tarefas(surf):
    bar = pygame.Rect(0, SH - ALTURA_BARRA_TAREFAS, SW, ALTURA_BARRA_TAREFAS)
    relevo(surf, bar)
    escrever(surf, FONTE_NEGRITO, "⚔ MISSÃO", 8, SH - ALTURA_BARRA_TAREFAS + 6, TITLE_ATIVA)
    x = 120
    for rotulo, cls in _ITENS_BARRA_TAREFAS:
        win = gerenciador_janelas.obter(cls)
        ativa = bool(win and win.visivel)
        botao_janela(surf, pygame.Rect(x, SH - ALTURA_BARRA_TAREFAS + 3, LARGURA_BOTAO_TAREFA, 22),
                   rotulo, apertado=ativa, fonte=FONTE_PEQUENA)
        x += LARGURA_BOTAO_TAREFA + 5

def clicar_barra_tarefas(pos) -> bool:
    x = 120
    for rotulo, cls in _ITENS_BARRA_TAREFAS:
        r = pygame.Rect(x, SH - ALTURA_BARRA_TAREFAS + 3, LARGURA_BOTAO_TAREFA, 22)
        if r.collidepoint(pos):
            win = gerenciador_janelas.obter(cls)
            if win:
                if win.visivel: gerenciador_janelas.trazer_para_frente(win)
                else: win.visivel = True; gerenciador_janelas.trazer_para_frente(win)
            else:
                gerenciador_janelas.adicionar(cls())
            return True
        x += LARGURA_BOTAO_TAREFA + 5
    return False

def rect_barra_tarefas() -> pygame.Rect:
    return pygame.Rect(0, SH - ALTURA_BARRA_TAREFAS, SW, ALTURA_BARRA_TAREFAS)

# ═══════════════════════════════════════════════════════════════════
#  SOBREPOSIÇÕES: VITÓRIA / FIM DE JOGO
# ═══════════════════════════════════════════════════════════════════
def desenhar_overlay(surf):
    if not (estado_jogo.fim_de_jogo or estado_jogo.vitoria):
        return
    ov = pygame.Surface((SW, SH), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 170))
    surf.blit(ov, (0, 0))
    if estado_jogo.vitoria:
        escrever_centralizado(surf, FONTE_GRANDE, "★   V I T Ó R I A   ★",          SW//2, SH//2 - 70, AMARELO)
        escrever_centralizado(surf, FONTE_MEDIA, "Zeus, O Grande Dragão Ancião, foi derrotado!", SW//2, SH//2 - 30, BRANCO)
        escrever_centralizado(surf, FONTE_MEDIA, "Mas de repente você percebe que está em cima de um alçapão",  SW//2, SH//2 + 10, BRANCO)
        escrever_centralizado(surf, FONTE_PEQUENA, "De repente o alçapão se abre e você cai em outro mundo",          SW//2, SH//2 + 48, CINZA)
    else:
        escrever_centralizado(surf, FONTE_GRANDE, "☠   G A M E   O V E R   ☠", SW//2, SH//2 - 40, VERMELHO)
        escrever_centralizado(surf, FONTE_MEDIA, "Enquanto você dá seu último suspiro você percebe que está em cima de um alçapão",  SW//2, SH//2 + 10, BRANCO)
        escrever_centralizado(surf, FONTE_PEQUENA, "De repente o alçapão se abre e você cai em outro mundo",          SW//2, SH//2 + 48, CINZA)
    return 5


# ═══════════════════════════════════════════════════════════════════
#  FUNDO DO DESKTOP
# ═══════════════════════════════════════════════════════════════════
def desenhar_area_trabalho(surf):
    surf.fill(AREA_DE_TRABALHO)
    # textura de grade sutil
    for y in range(0, SH, 20):
        pygame.draw.line(surf, (0, 110, 110), (0, y), (SW, y), 1)
    for x in range(0, SW, 20):
        pygame.draw.line(surf, (0, 110, 110), (x, 0), (x, SH - ALTURA_BARRA_TAREFAS), 1)

# ═══════════════════════════════════════════════════════════════════
#  INÍCIO  —  cria janelas iniciais
# ═══════════════════════════════════════════════════════════════════
gerenciador_janelas.adicionar(JanelaRegistro())
gerenciador_janelas.adicionar(JanelaEstatisticas())
gerenciador_janelas.adicionar(JanelaMapa())

