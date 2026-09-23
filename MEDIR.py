import segundoMAZE
import mapaMAZE

# ============================================================================
# MEDIR: corrida entre segundoMAZE (labirinto novo a cada tesouro) e mapaMAZE
# (mesmo labirinto + mapa). Os dois pegam TESOUROS tesouros e comparamos:
#   ticks    -> custo do jogo (nao muda com velocidade/energia): a medida justa
#   segundos -> tempo real
#   ouro ganho e substancia gasta
# get_tick_count(), get_time() e quick_print() sao gratis: nao atrapalham a medicao.
# O resultado sai no output.txt.
# ============================================================================

TESOUROS = 30                               # quantos tesouros cada algoritmo pega
COMPARAR_COM_SEGUNDO = False                # a corrida do segundoMAZE leva ~33 min e ja
											# temos os numeros dele: so liga se quiser refazer


def _medir(nome, corrida):
	ouro = num_items(Items.Gold)
	subst = num_items(Items.Weird_Substance)
	t0 = get_tick_count()
	s0 = get_time()
	corrida()
	ticks = get_tick_count() - t0
	segundos = get_time() - s0
	quick_print(nome, "|", ticks, "ticks |", ticks // TESOUROS, "ticks/tesouro |",
		segundos, "s | ouro +", num_items(Items.Gold) - ouro,
		"| substancia -", subst - num_items(Items.Weird_Substance))
	return ticks


def _corrida_segundo():
	for i in range(TESOUROS):
		segundoMAZE.Maze()


tempos_mapa = []                            # ticks ate cada tesouro no mapaMAZE

def _corrida_mapa():
	mapaMAZE.rodar(TESOUROS, tempos_mapa)


clear()
substancia = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
precisa = TESOUROS * substancia
if COMPARAR_COM_SEGUNDO:
	precisa = 2 * precisa
if num_items(Items.Weird_Substance) < precisa:
	quick_print("Substancia insuficiente pra medir: precisa de", precisa)
else:
	quick_print("=== corrida:", TESOUROS, "tesouros cada | campo", get_world_size(), "x", get_world_size(), "===")
	t_segundo = 0
	if COMPARAR_COM_SEGUNDO:
		t_segundo = _medir("segundoMAZE (labirinto novo)     ", _corrida_segundo)
	t_mapa = _medir("mapaMAZE (mesmo labirinto + mapa)", _corrida_mapa)

	# curva de aprendizado: o 1o tesouro explora, os seguintes usam o mapa
	n = len(tempos_mapa)
	if n > 1:
		resto = 0
		for i in range(1, n):
			resto = resto + tempos_mapa[i]
		quick_print("mapa aprendendo: 1o tesouro", tempos_mapa[0],
			"ticks | media dos seguintes", resto // (n - 1),
			"ticks | ultimo", tempos_mapa[n - 1], "ticks")
	if COMPARAR_COM_SEGUNDO and t_mapa > 0:
		quick_print("RESULTADO: mapaMAZE foi", t_segundo / t_mapa, "x mais rapido")
	# numeros das corridas anteriores (30 tesouros, campo 32x32), pra comparar
	quick_print("referencia segundoMAZE: 201874 ticks/tesouro")
	quick_print("referencia mapaMAZE antes de otimizar: 103299 ticks/tesouro | 1o 45557 | media dos seguintes 105036")
