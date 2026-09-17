import Utilidades

# ============================================================================
# POLICULTURA paralela (multi-drone): um drone por linha. Cada drone anda a sua
# linha por posicao ABSOLUTA (move_to), pra poder pular ate a casa do acompanhante
# e voltar sem se perder. Em cada casa: colhe se pronto, planta a cultura e planta
# o acompanhante que ela pede (get_companion) na posicao pedida -> bonus de rendimento.
#
# Obs: como o acompanhante cai numa casa vizinha (ate 3), drones de linhas vizinhas
# podem escrever na mesma casa (condicao de corrida) e um bonus ou outro se perde.
# Nao trava nem quebra; so nao fica 100% perfeito nas bordas entre linhas.
# Culturas que ganham bonus: Grass, Bush, Tree e Carrot.
# ============================================================================

def preparar_solo(tipo):
	if tipo == Entities.Carrot:
		if get_ground_type() != Grounds.Soil:
			till()
	else:                                   # grama, arbusto, arvore -> grama
		if get_ground_type() != Grounds.Grassland:
			till()


def _linha(tipo, y):
	# processa a linha y inteira (posicao absoluta pra sobreviver aos pulos do acompanhante)
	size = get_world_size()
	for x in range(size):
		Utilidades.move_to(x, y)
		if can_harvest():
			harvest()
		preparar_solo(tipo)
		if get_entity_type() == None:
			plant(tipo)
		comp = get_companion()
		if comp != None:
			tc, (cx, cy) = comp
			Utilidades.move_to(cx, cy)
			preparar_solo(tc)
			if get_entity_type() != tc:
				plant(tc)


def policultura(tipo):
	# 1 drone por linha (todos partindo de (0,0); cada um navega ate a sua linha)
	size = get_world_size()
	Utilidades.move_to(0, 0)
	drones = []
	for y in range(size):
		d = spawn_drone(_linha, tipo, y)
		if d:
			drones.append(d)
		else:
			_linha(tipo, y)              # sem drone livre: faz voce mesmo
	for d in drones:
		wait_for(d)
