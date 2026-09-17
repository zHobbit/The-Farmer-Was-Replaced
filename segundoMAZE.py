import Utilidades

# ============================================================================
# Solucao eficiente do labirinto: DFS guiada pelo alvo (best-first + backtrack)
#
# Ideia: measure() da a posicao do tesouro. Em cada celula, olhamos as saidas
# com can_move() (custa ~1 tick, de graca) e andamos para a vizinha ainda nao
# visitada que mais aproxima do tesouro. Se cair num beco, volta um passo.
# Como o labirinto e uma arvore (sem loops), isso nunca e pior que a mao-esquerda
# e quase sempre gasta bem menos movimentos (cada move que anda custa 200 ticks).
# ============================================================================

def Maze():
	# limpa o tile. se ja havia um labirinto, dar harvest fora do tesouro faz ele sumir
	harvest()
	# arbusto so cresce em grama; garante o chao certo
	if get_ground_type() != Grounds.Grassland:
		till()
	plant(Entities.Bush)

	# cresce o labirinto NA HORA no arbusto recem-plantado
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)

	# resolve
	resolver_labirinto()


def oposto(d):
	if d == North:
		return South
	if d == South:
		return North
	if d == East:
		return West
	return East                           # d == West


def vizinho(x, y, d):
	size = get_world_size()
	if d == North:
		return (x, (y + 1) % size)
	if d == South:
		return (x, (y - 1) % size)
	if d == East:
		return ((x + 1) % size, y)
	return ((x - 1) % size, y)            # West


def melhor_direcao(ax, ay, visitado):
	# retorna a saida (grátis de sondar) para a celula nova mais proxima do alvo,
	# ou None se nao houver nenhuma celula nova ao redor (beco sem saida)
	x = get_pos_x()
	y = get_pos_y()
	melhor = None
	melhor_dist = None
	for d in [North, South, East, West]:
		if can_move(d):
			nx, ny = vizinho(x, y, d)
			if (nx, ny) not in visitado:
				dist = abs(nx - ax) + abs(ny - ay)   # distancia de Manhattan ate o tesouro
				if melhor_dist == None or dist < melhor_dist:
					melhor_dist = dist
					melhor = d
	return melhor


def resolver_labirinto():
	alvo_x, alvo_y = measure()                       # posicao do tesouro
	visitado = set()
	visitado.add((get_pos_x(), get_pos_y()))
	caminho = []                                     # pilha de direcoes p/ backtrack
	while get_entity_type() != Entities.Treasure:
		d = melhor_direcao(alvo_x, alvo_y, visitado)
		if d != None:
			move(d)                                  # anda em direcao ao alvo
			visitado.add((get_pos_x(), get_pos_y()))
			caminho.append(d)
		else:
			d = caminho.pop()                        # beco: desfaz o ultimo passo
			move(oposto(d))
	harvest()                                        # so colhe no tesouro
