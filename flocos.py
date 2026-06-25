#No programa da flocos colocar um mp3 r fotos nossas. Fazer tipo um game de dungeon?
#pegar primeira mensagem nossa
#colocar sistema de upgrades e o jogo ir mudando
from personagens import *
from jogo_2d import *
import subprocess





os.system("cls")
print("Oi info pessoal, fiz esse joguinho pra vc")
sleep(5)
os.system("cls")
sleep(2)
print("espero que goste :)")
sleep(3)
os.system("cls")


def main():
    #parte 1
    heroi = Heroi()
    heroi.criar()
    while heroi.vivo:
        char = input("O que você quer fazer?\nAndar(a)\nVer inventário(i)\nVer seu personagem(p)\nVer a loja(l)")
        os.system("cls")
        if char == "a":
            heroi.andar()
        elif char == "i":
            heroi.ver_itens()
        elif char == "p":
            heroi.ver_personagem()
        elif char == "l":
            heroi.loja()
        elif char == "morrer":
            heroi._morrer()

    #parte 2
    tela = iniciar_tela()
    # --- TRANSFERÊNCIA DE DADOS) ---
    estado_jogo.jogador.nome = heroi.nome.replace("[yellow]", "").replace("[/yellow]", "")
    estado_jogo.jogador.vida = heroi.vida
    estado_jogo.jogador.vida_maxima = heroi.vida_maxima
    estado_jogo.jogador.ouro = heroi.pontos

    estado_jogo.jogador.inventario += [x for x in heroi.itens if x != 'cimitarra']

    if heroi.arma.nome == 'cimitarra':
        estado_jogo.jogador.equipado['arma'] = 'cimitarra'
    else:
        estado_jogo.jogador.equipado['arma'] = None
    # --------------------------------------------------------------------

    while True:
        dt = relogio.tick(FPS) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i and not estado_jogo.em_combate:
                    iw = gerenciador_janelas.get(JanelaInventario)
                    if iw:
                        iw.visivel = not iw.visivel
                        if iw.visivel: gerenciador_janelas.trazer_para_frente(iw)
                    else:
                        gerenciador_janelas.add(JanelaInventario())
                else:
                    gerenciador_janelas.tecla_pressionada(event.key, event.unicode)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect_barra_tarefas().collidepoint(event.pos):
                    clicar_barra_tarefas(event.pos)
                else:
                    gerenciador_janelas.apertar_mouse(event.pos, event.button)

            elif event.type == pygame.MOUSEBUTTONUP:
                gerenciador_janelas.soltar_mouse(event.pos, event.button)

            elif event.type == pygame.MOUSEMOTION:
                gerenciador_janelas.mover_mouse(event.pos)

            elif event.type == pygame.MOUSEWHEEL:
                gerenciador_janelas.rolar(pygame.mouse.get_pos(), event.y)

        gerenciador_janelas.atualizar(dt)

        desenhar_area_trabalho(tela)  # Desenha o fundo da tela
        gerenciador_janelas.desenhar(tela)       # Desenha as janelas abertas (mapa, inventário, etc.)
        desenhar_barra_tarefas(tela)  # Desenha a barra de tarefas
        
        a = desenhar_overlay(tela)

        pygame.display.flip()

        # parte 3
        if a == 5:
            sleep(10)
            pygame.quit()

            # começa um subprocesso e inicia a parte 3
            subprocess.run([sys.executable, "parte3d.py"])
            sys.exit() # Encerra o script atual



if __name__ == '__main__':
    main()
    