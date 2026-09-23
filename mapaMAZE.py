import Utilidades

# ============================================================================
# Labirinto com MAPA: um mapa novo por labirinto, reaproveitado por ate 300 tesouros.
#
# Usar Weird_Substance EM CIMA do tesouro coleta o ouro e sorteia um tesouro novo
# no MESMO labirinto (ate 300 vezes). As paredes continuam; algumas so somem.
# Enquanto anda, o drone anota numa tabela os vizinhos alcancaveis de cada casa:
#   saidas[casa] = [casas vizinhas sem parede]     conhecidas = casas ja anotadas
#
#  - 1o tesouro: explora (DFS guiada pelo measure()) e vai anotando o mapa.
#  - proximos: BFS no mapa -> caminho MAIS CURTO por casas conhecidas, sem explorar.
#    Se o tesouro caiu numa parte nao mapeada, vai pelo mapa ate a casa conhecida
#    mais perto dele e so explora dali.
#  - paredes so SOMEM, entao passagem anotada como aberta continua aberta.
#  - acabaram as 300 voltas (ou a substancia): colhe; o proximo labirinto zera o mapa.
#
# OTIMIZADO pro custo do jogo (cada operacao de codigo tambem custa tick):
#  - casa = numero (y * tamanho + x): conjunto/dicionario com chave pequena e mais barato
#  - o mapa guarda direto os VIZINHOS de cada casa -> o BFS nao calcula vizinho nenhum
#  - o BFS para assim que acha o tesouro
#  - o tamanho do campo e lido uma vez so e passado adiante
# ============================================================================

VOLTAS = 300                                # o tesouro muda de lugar ate 300 vezes


def _oposto(d):
	if d == North:
		return South
	if d == South:
		return North
	if d == East:
		return West
	return East


def _distancia(a, b, size):
	# distancia de Manhattan entre duas casas numeradas
	return abs(a % size - b % size) + abs(a // size - b // size)


def _direcao(a, b, size):
	# direcao pra andar da casa a ate a casa vizinha b (so usado no caminho escolhido)
	ay = a // size
	by = b // size
	if ay == by:
		if b % size == (a % size + 1) % size:
			return East
		return West
	if by == (ay + 1) % size:
		return North
	return South


def _anotar(saidas, conhecidas, size):
	# anota as saidas da casa atual (can_move custa ~1 tick). Devolve as direcoes
	# abertas e, na mesma ordem, as casas vizinhas pra onde elas levam.
	x = get_pos_x()
	y = get_pos_y()
	aqui = y * size + x
	abertas = []
	viz = []
	if can_move(North):
		abertas.append(North)
		viz.append(((y + 1) % size) * size + x)
	if can_move(East):
		abertas.append(East)
		viz.append(y * size + (x + 1) % size)
	if can_move(South):
		abertas.append(South)
		viz.append(((y - 1) % size) * size + x)
	if can_move(West):
		abertas.append(West)
		viz.append(y * size + (x - 1) % size)
	saidas[aqui] = viz
	conhecidas.add(aqui)
	return abertas, viz


def _ir_pelo_mapa(alvo, saidas, conhecidas, size):
	# BFS so pelas casas conhecidas, parando assim que acha o tesouro. Se ele ainda
	# nao foi mapeado, vai ate a casa alcancavel mais perto dele.
	origem = get_pos_y() * size + get_pos_x()
	if origem == alvo:
		return
	vistos = set()
	vistos.add(origem)
	veio = {}                               # casa -> casa anterior no caminho
	fila = [origem]
	melhor = origem
	i = 0
	while i < len(fila):
		c = fila[i]
		i = i + 1
		if c in conhecidas:                 # so expande casas cujas saidas conhecemos
			for n in saidas[c]:
				if n not in vistos:
					vistos.add(n)
					veio[n] = c
					fila.append(n)
					if n == alvo:
						melhor = n
						i = len(fila)       # achou: encerra o BFS
						break

	if melhor != alvo:                      # nao chegou no tesouro pelo mapa
		melhor_dist = _distancia(origem, alvo, size)
		for c in fila:
			dist = _distancia(c, alvo, size)
			if dist < melhor_dist:
				melhor = c
				melhor_dist = dist

	# monta o caminho de tras pra frente e anda na ordem certa
	passos = []
	c = melhor
	while c != origem:
		passos.append(c)
		c = veio[c]
	atual = origem
	n = len(passos)
	for k in range(n):
		prox = passos[n - 1 - k]
		if not move(_direcao(atual, prox, size)):
			return
		_anotar(saidas, conhecidas, size)   # atualiza (paredes podem ter sumido)
		atual = prox


def _explorar(alvo, saidas, conhecidas, size):
	# DFS guiada pelo alvo, anotando o mapa. Usada so onde o mapa ainda nao chega.
	aqui = get_pos_y() * size + get_pos_x()
	visitado = set()
	visitado.add(aqui)
	caminho = []                            # pilha de direcoes p/ voltar de becos
	while aqui != alvo:
		abertas, viz = _anotar(saidas, conhecidas, size)
		melhor = None
		melhor_dist = None
		for k in range(len(abertas)):
			n = viz[k]
			if n not in visitado:
				dist = _distancia(n, alvo, size)
				if melhor_dist == None or dist < melhor_dist:
					melhor_dist = dist
					melhor = abertas[k]
		if melhor != None:
			if not move(melhor):
				return
			caminho.append(melhor)
		else:
			if len(caminho) == 0:
				return                      # nao ha mais pra onde ir
			move(_oposto(caminho.pop()))    # beco: volta um passo
		aqui = get_pos_y() * size + get_pos_x()
		visitado.add(aqui)


def _ir_ate(alvo, saidas, conhecidas, size):
	_anotar(saidas, conhecidas, size)
	_ir_pelo_mapa(alvo, saidas, conhecidas, size)
	if get_pos_y() * size + get_pos_x() != alvo:
		_explorar(alvo, saidas, conhecidas, size)


def Maze():
	# um labirinto completo (ate 300 tesouros). False = nao da pra continuar.
	return rodar(VOLTAS, [])


def rodar(voltas, tempos):
	# pega ate `voltas` tesouros no mesmo labirinto e anota em `tempos` quantos
	# ticks levou pra chegar em cada um (pra medir o mapa "aprendendo").
	# devolve False quando nao da pra continuar (sem substancia ou labirinto nao cresceu)
	Utilidades.trocar_chapeu(Hats.Gold_Hat)  # tambem tira o de dinossauro
	size = get_world_size()                 # lido uma vez so
	substancia = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
	if num_items(Items.Weird_Substance) < substancia:
		return False

	# cria o labirinto (harvest fora do tesouro some com um labirinto antigo)
	harvest()
	if get_ground_type() != Grounds.Grassland:
		till()
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substancia)

	saidas = {}                             # mapa NOVO para este labirinto
	conhecidas = set()

	for volta in range(voltas):
		pos = measure()                     # posicao (x, y) do tesouro atual
		if pos == None:
			return False                    # o labirinto nao cresceu
		alvo = pos[1] * size + pos[0]
		inicio = get_tick_count()           # medir e gratis
		_ir_ate(alvo, saidas, conhecidas, size)
		tempos.append(get_tick_count() - inicio)
		if get_pos_y() * size + get_pos_x() != alvo:
			harvest()                       # nao chegou: desfaz e comeca outro
			return True
		if volta == voltas - 1 or num_items(Items.Weird_Substance) < substancia:
			harvest()                       # coleta o ultimo tesouro e encerra o labirinto
			return True
		if not use_item(Items.Weird_Substance, substancia):
			harvest()                       # coleta e move o tesouro; se falhar, encerra
			return True
	return True
