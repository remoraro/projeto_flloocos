from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math
import sys
import os

# ───────────────────────────────────────────────────────────────
#  FUNÇÕES AUXILIARES
# ───────────────────────────────────────────────────────────────

# ───────────────────────────────────────────────────────────────
#  CRIA PAREDES (cubo com colisão)
# ───────────────────────────────────────────────────────────────

def parede(pos, esc, cor=color.azure, textura=None):
    """Cria um cubo com colisão."""
    return Entity(model='cube', position=pos, scale=esc,
                  color=cor, collider='box', texture=textura)

# ───────────────────────────────────────────────────────────────
#  CRIAÇÃO DE PLANOS (chão, teto)
# ───────────────────────────────────────────────────────────────

def piso(pos, esc, cor, teto=False, textura=None):
    """Cria um plano (chão com colisão, teto sem)."""
    e = Entity(model='plane', position=pos, scale=esc, color=cor,
               collider=None if teto else 'box', texture=textura)
    if teto:
        e.rotation_x = 180
    return e

# ───────────────────────────────────────────────────────────────
#  FOTO 3D 
# ───────────────────────────────────────────────────────────────

def foto3d(pos, esc, ry, arquivo):
    """Coloca uma foto numa parede usando Sprite."""
    img = load_texture(arquivo)
    sprite = Sprite(
            texture=img,
            position=pos,
            scale=esc,
            rotation_y=ry,
        )
    return sprite

# ───────────────────────────────────────────────────────────────
#  TEXTO 3D BILLBOARD (sempre vira para o jogador — sem espelho)
# ───────────────────────────────────────────────────────────────

class Label3D(Entity):
    """Texto em 3D que sempre fica de frente para o jogador."""

    def __init__(self, txt, pos, esc=8, cor=color.yellow):
        # O parâmetro billboard=True faz toda a mágica automaticamente!
        super().__init__(position=pos, billboard=True)
        
        self.text_entity = Text(
            text=txt, 
            scale=esc,
            color=cor, 
            origin=(0, 0),
            parent=self
        )
    