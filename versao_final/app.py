from jogo import Jogo
from estados.partida import Partida
from estados.menu_principal import MenuPrincipal
from estados.menu_creditos import MenuCreditos
from estados.menu_opcoes import MenuOpcoes
from estados.fim_de_jogo import FimDeJogo
from estados.menu_ranking import MenuRanking
from estados.menu_registro import MenuRegistro
# from fase import Fase


jogo = Jogo()

partida = Partida(jogo.maquina_de_estado)
menu_principal = MenuPrincipal(jogo.maquina_de_estado, jogo.tela)
menu_ranking = MenuRanking(jogo.maquina_de_estado, jogo.tela)
menu_registro = MenuRegistro(jogo.maquina_de_estado, jogo.tela)
menu_creditos = MenuCreditos(jogo.maquina_de_estado, jogo.tela)
menu_opcoes = MenuOpcoes(jogo.maquina_de_estado, jogo.tela)
fim_de_jogo = FimDeJogo(jogo.maquina_de_estado, jogo.tela)

# partida.registrar_fase(Fase(partida))

jogo.maquina_de_estado.adicionar_estado("partida", partida)
jogo.maquina_de_estado.adicionar_estado("menu_principal", menu_principal)
jogo.maquina_de_estado.adicionar_estado("menu_ranking", menu_ranking)
jogo.maquina_de_estado.adicionar_estado("menu_registro", menu_registro)
jogo.maquina_de_estado.adicionar_estado("menu_creditos",menu_creditos)
jogo.maquina_de_estado.adicionar_estado("menu_opcoes", menu_opcoes)
jogo.maquina_de_estado.adicionar_estado("fim_de_jogo", fim_de_jogo)

jogo.iniciar()
