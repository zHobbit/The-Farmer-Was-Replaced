import Utilidades

# ============================================================================
# POLICULTURA paralela em 3 FASES (todos os drones, sem condicao de corrida).
#
# Cada planta pede um acompanhante (get_companion) a ate 3 casas de distancia.
# Se cada drone plantasse os acompanhantes da propria linha, ele invadiria as
# linhas vizinhas e brigaria com os outros drones. Entao cada passada tem 3 fases,
# e em TODAS elas cada drone so mexe na PROPRIA linha:
#
#   Fase 1: cada drone planta a cultura na sua linha e DEVOLVE os pedidos de
#           acompanhante (tipo, x, y) daquela linha.
#   Central: o drone principal junta os pedidos, resolve conflitos (casa pedida
#           por duas plantas -> vale o primeiro) e separa pela linha de destino.
#   Fase 2: cada drone planta os acompanhantes que caem na SUA linha.
#   Fase 3: cada drone fertiliza (se a regra deixar), colhe e replanta a sua
#           linha, PULANDO as casas de acompanhante (pra nao arrancar o
#           acompanhante antes da planta do vizinho ser colhida com o bonus).
#
# Entre as fases o drone principal espera todos terminarem (wait_for).
# Culturas que ganham bonus: Grass, Bush, Tree e Carrot.
# ============================================================================

def preparar_solo(tipo):
	if tipo == Entities.Carrot:
		if get_ground_type() != Grounds.Soil:
			till()
	else:                                   # grama, arbusto, arvore -> grama
		if get_ground_type() != Grounds.Grassland:
			till()


def _fase_plantar(tipo, y):
	# FASE 1: planta a cultura na linha y e devolve os pedidos [(tipo_acomp, x, y), ...]
	size = get_world_size()
	pedidos = []
	for x in range(size):
		Utilidades.move_to(x, y)
		if get_entity_type() == None:
			preparar_solo(tipo)
			plant(tipo)
		if get_entity_type() == tipo:       # so a cultura principal pede acompanhante
			comp = get_companion()
			if comp != None:
				tc, (cx, cy) = comp
				pedidos.append((tc, cx % size, cy % size))
	return pedidos


def _fase_acompanhantes(y, lista):
	# FASE 2: planta os acompanhantes que caem na linha y. lista = [(x, tipo_acomp), ...]
	for p in lista:
		x = p[0]
		tc = p[1]
		Utilidades.move_to(x, y)
		if get_entity_type() != tc:
			harvest()                        # libera a casa: plant() so funciona em casa vazia
			preparar_solo(tc)
			plant(tc)


def _fase_colher(tipo, y, pular, fert):
	# FASE 3: fertiliza, colhe e replanta a linha y, pulando as casas de acompanhante
	size = get_world_size()
	acompanhantes = set()
	for x in pular:
		acompanhantes.add(x)
	for x in range(size):
		if x in acompanhantes:
			continue
		Utilidades.move_to(x, y)
		if fert:
			Utilidades.Fertilizar()          # fica pronta na hora
		if can_harvest():
			harvest()                        # o acompanhante esta no lugar -> sai com bonus
		if get_entity_type() != tipo:        # casa vazia ou resto de acompanhante antigo
			if get_entity_type() != None:
				harvest()
			preparar_solo(tipo)
			plant(tipo)                      # ja deixa a proxima crescendo


def policultura(tipo):
	Utilidades.trocar_chapeu(Hats.Green_Hat)
	fert = Utilidades.pode_fertilizar()      # decide 1x por passada (drone principal)
	size = get_world_size()
	Utilidades.move_to(0, 0)

	# ---- FASE 1: plantar e juntar os pedidos de acompanhante ----
	drones = []
	resultados = []
	for y in range(size):
		d = spawn_drone(_fase_plantar, tipo, y)
		if d:
			drones.append(d)
		else:
			resultados.append(_fase_plantar(tipo, y))   # sem drone livre: faz voce mesmo
	for d in drones:
		resultados.append(wait_for(d))      # wait_for devolve a lista de pedidos do drone

	# ---- CENTRAL: resolve conflitos e separa pela linha de destino ----
	por_linha = []
	for y in range(size):
		por_linha.append([])
	ja_pedida = set()
	for lista in resultados:
		for p in lista:
			alvo = (p[1], p[2])
			if alvo not in ja_pedida:       # casa pedida por duas plantas: vale o primeiro
				ja_pedida.add(alvo)
				por_linha[p[2]].append((p[1], p[0]))

	# ---- FASE 2: plantar os acompanhantes (cada drone na sua linha) ----
	drones = []
	for y in range(size):
		if len(por_linha[y]) > 0:
			d = spawn_drone(_fase_acompanhantes, y, por_linha[y])
			if d:
				drones.append(d)
			else:
				_fase_acompanhantes(y, por_linha[y])
	for d in drones:
		wait_for(d)

	# ---- FASE 3: colher e replantar (pulando as casas de acompanhante) ----
	drones = []
	for y in range(size):
		pular = []
		for p in por_linha[y]:
			pular.append(p[0])
		d = spawn_drone(_fase_colher, tipo, y, pular, fert)
		if d:
			drones.append(d)
		else:
			_fase_colher(tipo, y, pular, fert)
	for d in drones:
		wait_for(d)
