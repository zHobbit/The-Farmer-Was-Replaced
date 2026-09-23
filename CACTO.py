import Utilidades

# ============================================================================
# Cacto PARALELO (multi-drone):
#  1) planta o campo todo em paralelo (for_all)
#  2) ordena cada LINHA num drone (linhas sao disjuntas -> sem corrida)
#  3) ordena cada COLUNA num drone (colunas sao disjuntas -> sem corrida)
#  4) colhe 1 -> a colheita se espalha pelo campo inteiro (rende (lado*lado)**2)
#
# Ordem exigida: cada linha crescente Oeste->Leste e cada coluna crescente
# Sul->Norte. Como so da pra trocar vizinhos (swap), usamos bubble sort.
# ============================================================================

def plantar_cacto():
	if get_ground_type() != Grounds.Soil:
		till()
	if get_entity_type() != Entities.Cactus:
		plant(Entities.Cactus)


def ordena_linha_aqui():
	# bubble sort da linha onde este drone esta (empurra maiores pro Leste)
	size = get_world_size()
	trocou = True
	while trocou:
		trocou = False
		Utilidades.move_to(0, get_pos_y())
		for x in range(size - 1):
			if measure() > measure(East):
				swap(East)
				trocou = True
			move(East)


def ordena_coluna_aqui():
	# bubble sort da coluna onde este drone esta (empurra maiores pro Norte)
	size = get_world_size()
	trocou = True
	while trocou:
		trocou = False
		Utilidades.move_to(get_pos_x(), 0)
		for y in range(size - 1):
			if measure() > measure(North):
				swap(North)
				trocou = True
			move(North)


def Cacto():
	# sem fertilizante de proposito: cacto cresce em ~1s e a infeccao cortaria
	# pela metade a colheita gigante do campo ordenado.
	Utilidades.trocar_chapeu(Hats.Cactus_Hat)
	size = get_world_size()

	# 1) planta em paralelo
	Utilidades.move_to(0, 0)
	Utilidades.for_all(plantar_cacto)

	# 2) ordena LINHAS em paralelo (1 drone por linha)
	Utilidades.move_to(0, 0)
	drones = []
	for y in range(size):
		d = spawn_drone(ordena_linha_aqui)
		if d:
			drones.append(d)
		else:
			ordena_linha_aqui()
		move(North)
	for d in drones:
		wait_for(d)

	# 3) ordena COLUNAS em paralelo (1 drone por coluna)
	Utilidades.move_to(0, 0)
	drones = []
	for x in range(size):
		d = spawn_drone(ordena_coluna_aqui)
		if d:
			drones.append(d)
		else:
			ordena_coluna_aqui()
		move(East)
	for d in drones:
		wait_for(d)

	# 4) colhe um -> cascata pega o campo todo
	Utilidades.move_to(0, 0)
	while not can_harvest():
		pass
	harvest()
