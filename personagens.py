import os
import random
from time import sleep
from rich import print
from rich.panel import Panel
from pygame import mixer
 

class Arma:
    """
    É a arma do personagem ou inimigo
    """
    def __init__(self, nome = "", dano = int, durabilidade = int):
        self.nome = nome
        self.dano = dano
        self.durabilidade = durabilidade




class Heroi:
    """
    É o personagem do jogador, tem nome, arma, vida, itens e pontos.
    """
    cimitarra = Arma(nome = "cimitarra", dano = 5, durabilidade = 50)
    maos = Arma(nome = "mãos", dano = 1, durabilidade = 10000)
 
    def __init__(self, nome = "", arma = maos, vida = 100, cor = "green"):
        self.nome = nome
        self.arma = arma
        self.vida = vida
        self.vida_maxima = vida
        self.vivo = True
        self.cor = cor
        self.estrada_atual = 0
        self.estrada = 30
        self.itens = []
        self.pontos = 0
        self.upgrade1 = False
        self.upgrade2 = False
        self.upgrade3 = False

    def mostrar_vida(self):
        tamanho = 20
        vida_atual = max(0, self.vida) # Evita que a barra desenhe negativo se tomar muito dano
        cheios = round((vida_atual / self.vida_maxima) * tamanho)
        vazios = tamanho - cheios
        
        barra = f"[{self.cor}]{'█' * cheios}[/{self.cor}][grey37]{'_' * vazios}[/grey37]"
        print(f"Vida de {self.nome}: {vida_atual}/{self.vida_maxima}\n|{barra}|")

    def _morrer(self):
        print("Você [red]morreu[/red]")
        sleep(3)
        print("Mas espera")
        sleep(1)
        print("Você sente algo estranho acontecendo...")
        sleep(3)
        self.vida = self.vida_maxima
        self.vivo = False

    def criar(self):
        print("Seja bem vindo ao jogo! Vamos criar seu personagem:")
        self.nome = f"[yellow]{input('Digite o seu nome: ')}[/yellow]"
        os.system("cls")
        sleep(3)
        print("Que belo nome! *wink*")
        sleep(1)
        os.system("cls")
        print("\nPronto! Personagem criado, vamos lá!\nVocê tem que chegar ao castelo e em cada passo podem surgir inimigos!")
        dificul = input("Escolher dificuldade, isso vai decidir quanta vida você tem e quão longe está o castelo:\nFácil(f)\nMédio(m)\nDifícil(d) \n").strip().lower()
        if dificul == "f":
            self.vida = 150
            self.vida_maxima = 150
            self.estrada = 25
        elif dificul == "d":
            self.vida = 80
            self.vida_maxima = 80
            self.estrada = 40
        self.mostrar_vida()
        os.system("cls")

    def equipar(self, weapon):
        self.arma = weapon
        return print(f"Você equipou a arma {weapon.nome}")
    
    def bater(self):
        self.arma.durabilidade -= 2
        if self.arma.durabilidade <= 0:
            print("Sua arma quebrou!")
            self.arma = self.maos

    def ver_itens(self):
        if self.upgrade2 == True:
            print(f"""
                Você tem {len(self.itens)} itens
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠉⠉⠉⠉⠉⠉⠉⠉⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⣾⠀⣿⣿⡿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⢿⣿⣿⠀⢷⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⢰⡏⠀⣿⣿⠀⣴⣶⣶⣶⣶⣶⣶⣶⣶⣦⠀⣿⣿⡀⢸⡆⠀⠀⠀⠀
            ⠀⠀⠀⠀⢸⡇⠀⣿⣿⣆⠘⠻⠇⢠⣤⣤⡄⠸⠟⠋⣠⣿⣿⡇⢸⡇⠀⠀⠀⠀
            ⠀⠀⠀⠀⢸⣇⠀⣿⣿⣿⣿⣶⣆⣈⣉⣉⣁⣰⣶⣿⣿⣿⣿⠃⢸⡇⠀⠀⠀⠀
            ⠀⠀⠀⠀⠈⣿⣀⣉⣉⠉⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠉⣉⣉⣀⣿⠀⠀⠀⠀⠀
            ⠀⠀⢀⡴⠀⣉⣉⠉⠉⠉⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠉⠉⠉⣉⣉⠀⢦⡀⠀⠀
            ⠀⠀⠈⣀⠀⣿⣿⠀⣿⣿⠀⠛⠛⠉⠉⠉⠉⠛⠛⠀⣿⣿⠀⣿⣿⠀⣀⠁⠀⠀
            ⠀⠀⢸⡇⢀⣿⣿⠀⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⠀⣿⣿⡀⢸⡇⠀⠀
            ⠀⠀⢸⡇⢸⣿⠀⣤⡤⢤⣄⠘⠻⠿⠿⠿⠿⠟⠃⣠⡤⢤⣤⠀⣿⡇⢸⡇⠀⠀
            ⠀⠀⢠⡄⢸⣿⠀⠛⠃⠘⠋⢸⣶⣶⣆⣰⣶⣶⡇⠙⠃⠘⠛⠀⣿⡇⢠⡄⠀⠀
            ⠀⠀⢠⡄⠸⣿⣿⠀⠷⠞⠀⠛⠛⠿⠿⠿⠿⠛⠛⠀⠳⠾⠀⣿⣿⠇⢠⡄⠀⠀
            ⠀⠀⠘⠗⠀⣿⣿⠀⣶⣶⠀⣿⣷⣶⣶⣶⣶⣾⣿⠀⣶⣶⠀⣿⣿⠀⠺⠃⠀⠀
            ⠀⠀⠀⠀⠀⠉⠉⠀⠉⠉⠀⠉⠉⠉⠉⠉⠉⠉⠉⠀⠉⠉⠀⠉⠉⠀⠀⠀⠀⠀
                """)
        print("Seus itens são:")
        for itens in self.itens:
            print(itens)
        char = input("Qual você quer usar? (digite qualquer outra tecla para sair)").lower()
        if char == "cimitarra" and "cimitarra" in self.itens:
            self.equipar(self.cimitarra)
            self.itens.remove("cimitarra")
            return
        elif char == "erva" and "erva" in self.itens:
            self.itens.remove("erva")
            self.vida += 20
            print(f"Sua vida aumentou em 20! Vida atual: {self.vida}")
            return

    def ver_personagem(self):
        print(f"O nome do seu personagem é [yellow]{self.nome}[/yellow]\nVocê tem {self.vida} de [dark_red]vida[/dark_red] \nVocê está no {self.estrada_atual} passo de {self.estrada} para o [grey37]castelo[/grey37]\nVocê está usando a arma {self.arma.nome} que da {self.arma.dano} de dano e tem {self.arma.durabilidade} de durabilidade")
        print(f"Você tem [bright_yellow]{self.pontos}[/bright_yellow] pontos")
        input()
        return
    
    def loja(self):
        msg1 = msg2 = ""
        if self.upgrade2 == True:
            msg2 = "[Comprado]"
            print(r"""
                                                                        ___
                                                                ___..--'  .`.
                                                        ___...--'     -  .` `.`.
                                            ___...--' _      -  _   .` -   `.`.
                                    ___...--'  -       _   -       .`  `. - _ `.`.
                            __..--'_______________ -         _  .`  _   `.   - `.`.
                            .`    _ /\    -        .`      _     .`__________`. _  -`.`.
                        .` -   _ /  \_     -   .`  _         .` |  Lojinha  |`.   - `.`.
                        .`-    _  /   /\   -   .`        _   .`   |___________|  `. _   `.`.
                    .`________ /__ /_ \____.`____________.`     ___       ___  - `._____`|
                        |   -  __  -|    | - |  ____  |   | | _  |   |  _  |   |  _ |
                        | _   |  |  | -  |   | |.--.| |___| |    |___|     |___|    |
                        |     |--|  |    | _ | |'--'| |---| |   _|---|     |---|_   |
                        |   - |__| _|  - |   | |.--.| |   | |    |   |_  _ |   |    |
                    ---``--._      |    |   |=|'--'|=|___|=|====|___|=====|___|====|
                    -- . ''  ``--._| _  |  -|_|.--.|_______|_______________________|
                    `--._           '--- |_  |:|'--'|:::::::|:::::::::::::::::::::::|
                    _____`--._ ''      . '---'``--._|:::::::|:::::::::::::::::::::::|
                    ----------`--._          ''      ``--.._|:::::::::::::::::::::::|
                    `--._ _________`--._'        --     .   ''-----.................|'
                        `--._----------`--._.  _           -- . :''           -    ''
                            `--._ _________`--._ :'              -- . :''      -- . ''
                    -- . ''       `--._ ---------`--._   -- . :''
                            :'        `--._ _________`--._:'  -- . ''      -- . ''
                    -- . ''     -- . ''    `--._----------`--._      -- . ''     -- . ''
                                                `--._ _________`--._
                    -- . ''           :'              `--._ ---------`--._-- . ''    -- . ''
                            -- . ''       -- . ''         `--._ _________`--._   -- . ''
                    :'                 -- . ''          -- . ''  `--._----------`--._
                """)
        if self.upgrade1 == True: msg1 = "[Comprado]"
        lojinha = Panel(f"Bem vindo a loja! Aqui você consegue fazer [italic]upgrades[/italic] no jogo\nEscolha o upgrade que quer fazer:\n\t1 - Música no jogo (preço [yellow]25[/yellow]) {msg1}\n\t2 - Gráficos (preço [yellow]50[/yellow]) {msg2}\n\t3 - Misterioso? (preço [yellow]100[/yellow])\n", subtitle=f"Você tem [yellow]{self.pontos}[/yellow] pontos", title="Loja", width= 60)
        print(lojinha)
        char = input("Em qual número você quer dar upgrade?: ")
        if char == "1":
            if self.pontos >= 25 and self.upgrade1 == False:
                self.pontos -= 25
                self.upgrade1 = True
                mixer.music.load("fog.mp3")
                mixer.music.play()
                return
            elif self.upgrade1 == True:
                print("Upgrade já comprado!")
            elif self.pontos < 100:
                print("Pontos insuficientes!")
                return
        elif char == "2":
            if self.pontos >= 50 and self.upgrade2 == False:
                self.pontos -= 50
                self.upgrade2 = True
                return
            elif self.upgrade2 == True:
                print("Upgrade já comprado!")
                return
            elif self.pontos < 100:
                print("Pontos insuficientes!")
                return
        elif char == "3":
            if self.pontos >= 100:
                self.pontos -= 100
                self.upgrade3 = True
                os.system("cls")
                print("Parabéns! Você conseguiu o último upgrade, achou um atalho para o castelo e venceu o jogo!")
                sleep(3)
                print("Mas espera")
                sleep(1)
                print("Você chegando no castelo se perde na floresta e sente algo estranho acontecendo...")
                sleep(3)
                if self.upgrade1 == True:
                    mixer.music.stop()
                self.vivo = False
                return
            elif self.pontos < 100:
                print("Pontos insuficientes!")
                return
        else:
            return
    
    def andar(self):
        os.system("cls")
        dado = random.randint(1, 3)
        if dado == 1 or dado == 3:
            if self.upgrade2 == True:
                print(r"""
                            .         .      /\      .:  *       .          .              .
                                        *    .'  `.      .     .     *      .                  .
                        :             .    /      \  _ .________________  .                    .
                            |            `.+-~~-+.'/.' `.^^^^^^^^\~~~~~\.                      .
                        .    -*-   . .       |u--.|  /     \~~~~~~~|~~~~~|
                            |              |   u|.'       `." "  |" " "|                        .
                            :            .    |.u-./ _..---.._ \" " | " " |
                        -*-            *   |    ~-|U U U U|-~____L_____L_                      .
                            :         .   .   |.-u.| |..---..|"//// ////// /\       .            .
                                .  *        |u   | |       |// /// // ///==\     / \          .
                        .          :         |.--u| |..---..|//////~\////====\   /   \       .
                            .               | u  | |       |~~~~/\u |~~|++++| .`+~~~+'  .
                                            |.-|~U~U~|---..|u u|u | |u ||||||   |  U|
                                        /~~~~/-\---.'     |===|  |u|==|++++|   |   |
                                aaa      |===| _ | ||.---..|u u|u | |u ||HH||U~U~U~U~|        aa@@
                            aaa@@@@@@aa   |===|||||_||      |===|_.|u|_.|+HH+|_/_/_/_/aa    a@@@@@@
                        aa@@@@@@@@@@@@@@a |~~|~~~~\---/~-.._|--.---------.~~~`.__ _.@@@@@@a    ~~~~
                        ~~~~~~    ~~~    \_\\ \  \/~ //\  ~,~|  __   | |`.   :||  ~~~~
                                            a\`| `   _//  | / _| || |  | `.'  ,''|     aa@@@@@@@a
                        aaa   aaaa       a@@@@\| \  //'   |  // \`| |  `.'  .' | |  aa@@@@@@@@@@@@@
                        @@@@@a@@@@@@a      ~~~~~ \\`//| | \ \//   \`  .-'  .' | '/      ~~~~~~~  ~~
                        @S.C.E.S.W.@@@@a          \// |.`  ` ' /~  :-'   .'|  '/~aa
                        ~~~~~~ ~~~~~~         a@@@|   \\ |   // .'    .'| |  |@@@@@@a
                                            a@@@@@@@\   | `| ''.'     .' | ' /@@@@@@@@@a
                                            ~~~~~~  \  |  \  /      .'|  |  ~~~~~~~
                                                    \ |   \ /      .' |  |    ~~~~
                                                    `|    \      .'  |  |
                                                        |     \   .'    |  |
                                                        |      \.'
                      """)
            print("Você avança no caminho para o [white]castelo...[/white]")
            self.estrada_atual += 1
            print(f"{self.estrada_atual} de {self.estrada}")
            if self.estrada == self.estrada_atual:
                print("Parabéns! Você chegou no castelo e venceu o jogo!")
                sleep(3)
                print("Mas espera")
                sleep(1)
                print("Você chegando no castelo se perde na floresta e sente algo estranho acontecendo...")
                sleep(3)
                if self.upgrade1 == True:
                    mixer.music.stop()
                self.vivo = False
        elif dado == 2:
            print("Um inimigo apareceu! Derrote-o!")
            inimigo = Heroi(cor = "red", nome = random.choice(["[red]inimigo[/red]","[red]eis que leto[/red]"]) ,arma = random.choice([self.maos, self.cimitarra]), vida = random.randint(5,15))
            self.lutar(inimigo)

    def lutar(self, inimigo):
        while (self.vivo == True) and (inimigo.vivo == True):
            char = input("Escolha o que você quer fazer:\nBater(b)\nTentar fugir(f)\n")
            os.system("cls")
            if self.upgrade2 == True:
                print(r"""                              _.--""-._
    .                         ."         ".
    / \    ,^.         /(     Y             |      )\
    /   `---. |--'\    (  \__..'--   -   -- -'""-.-'  )
    |        :|    `>   '.     l_..-------.._l      .'
    |      __l;__ .'      "-.__.||_.-'v'-._||`"----"
    \  .-' | |  `              l._       _.'
    \/    | |                   l`^^'^^'j
            | |                _   \_____/     _
            j |               l `--__)-'(__.--' |
            | |               | /`---``-----'"1 |  ,-----.
            | |               )/  `--' '---'   \'-'  ___  `-.
            | |              //  `-'  '`----'  /  ,-'   I`.  \
        _ L |_            //  `-.-.'`-----' /  /  |   |  `. \
        '._' / \         _/(   `/   )- ---' ;  /__.J   L.__.\ :
        `._;/7(-.......'  /        ) (     |  |            | |
        `._;l _'--------_/        )-'/     :  |___.    _._./ ;
            | |                 .__ )-'\  __  \  \  I   1   / /
            `-'                /   `-\-(-'   \ \  `.|   | ,' /
                            \__  `-'    __/  `-. `---'',-'
                                )-._.-- (        `-----'
                                )(  l\ o ('..-.
                        _..--' _'-' '--'.-. |
                    __,,-'' _,,-''            \ \
                f'. _,,-'                   \ \
                ()--  |                       \ \
                    \.  |                       /  \
                    \ \                      |._  |
                    \ \                     |  ()|
                        \ \                     \  /
                        ) `-.                   | |
                        // .__)                  | |
                    _.//7'                      | |
                '---'                         j_| `
                                                (| |
                                                |  \
                                                |lllj
                                                ||||| 

                                                ||||| """)
            dado = random.randint(1,4)
            if char == "f":
                if dado == 4:
                    print("Você conseguiu fugir")
                    return
                else:
                    print("Você não conseguiu fugir")
                    self.vida -= inimigo.arma.dano
                    print(f"O {inimigo.nome} te bateu com uma {inimigo.arma.nome} e tirou {inimigo.arma.dano} de vida!\n")
                    self.mostrar_vida()
                    if self.vida <= 0:
                        if self.upgrade1 == True:
                            mixer.music.stop()
                        self._morrer()
            elif char == "b":
                inimigo.vida -= self.arma.dano
                print(f"Você bateu no {inimigo.nome} com {self.arma.nome} e tirou {self.arma.dano} de vida")
                inimigo.mostrar_vida()
                
                self.bater()
                if inimigo.vida <= 0:
                    print(f"Você derrotou o {inimigo.nome}!")
                    print("Você ganhou 25 pontos, use-os na loja")
                    self.pontos += 25
                    if dado == 2 or dado == 4:
                        loot = random.choice(["cimitarra", "erva"])
                        print(f"O {inimigo.nome} dropou o seguinte item: {loot}")
                        self.itens.append(loot)
                    inimigo.vivo = False
                    return
                if dado == 2:
                    self.vida -= inimigo.arma.dano
                    print(f"O {inimigo.nome} te bateu com uma {inimigo.arma.nome} e tirou {inimigo.arma.dano} de vida!\n")
                    self.mostrar_vida()
                    if self.vida <= 0:
                        if self.upgrade1 == True:
                            mixer.music.stop()
                        self._morrer()
                elif dado == 3:
                    print(f"O {inimigo.nome} tentou te bater mas errou")
                elif dado == 1:
                    print(f"O {inimigo.nome} tentou te bater e quase acertou")
                else:
                    print(f"O {inimigo.nome} ficou te olhando de um jeito curioso")


            