from estados.partida import Partida
from fase import Fase
from jogo import Jogo

jogo = Jogo()
partida = Partida(jogo)
partida.registrar_fase(Fase(partida))

jogo.adicionar_estado("partida", partida)
jogo.mover_para_estado("partida")
jogo.iniciar()
