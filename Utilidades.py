plant_type = get_companion()


def andar():
	frente = get_pos_x()
	cima = get_pos_y()
	if frente < get_world_size() - 1:
		frente = frente + 1
	elif frente == get_world_size() - 1:
		if cima < get_world_size() - 1:
			cima = cima + 1
		else:
			cima = 0
		move_to(0, cima)
		frente = get_pos_x() 
	move_to(frente, cima)


def move_n_dir(n, dir):
	for i in range(n):
		move(dir)


def for_all(f):
	# roda f() em cada casa da fazenda em paralelo: 1 drone por linha.
	# se nao houver drone livre, o proprio drone faz a linha e volta pra coluna 0.
	# espera todos terminarem antes de retornar.
	size = get_world_size()
	def linha():
		for i in range(size - 1):
			f()
			move(East)
		f()
	drones = []
	for i in range(size):
		d = spawn_drone(linha)
		if d:
			drones.append(d)
		else:
			linha()
			move_to(0, get_pos_y())
		move(North)
	for d in drones:
		wait_for(d)
	

def ARAR(tipo):
	if tipo == Entities.Carrot or tipo == Entities.Pumpkin:
		if get_ground_type() != Grounds.Soil:
			till()
	elif tipo != None:
		if get_ground_type() != Grounds.Grassland:
			till()

def wait_until_grown():
	while not can_harvest():
		pass


def COLHER():
	if get_entity_type() == Entities.Dead_Pumpkin:
		plant(Entities.Pumpkin)
	if can_harvest() == True:
		harvest()
	
		
def REGAR():
	while get_water() < 1:
		use_item(Items.Water)
	
		
def plant_check():
	if plant_type == get_entity_type():
		return True
	else:
		return False

def is_even(num):
	return num % 2 == 0
	
def Maze():
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)		


def POLICULTUTRA():
	initial_locx = get_pos_x()
	initial_locy = get_pos_y()
	plant_type, (x, y) = get_companion()
	move_to(x, y)
	if get_entity_type() == plant_type:
		move_to(initial_locx, initial_locy)
	else:
		COLHER()
		ARAR(plant_type)
		plant(plant_type)
		REGAR()
		move_to(initial_locx, initial_locy)
		COLHER()
	
			
def move_to(x, y):
	# vai pelo caminho MAIS CURTO usando a volta pela borda (o campo da a volta).
	# Anda um numero fixo de passos, entao nunca fica preso num while infinito.
	size = get_world_size()
	dx = (x - get_pos_x()) % size        # quantos passos pro Leste
	if dx <= size // 2:
		for i in range(dx):
			move(East)
	else:
		for i in range(size - dx):       # mais perto pelo Oeste
			move(West)
	dy = (y - get_pos_y()) % size        # quantos passos pro Norte
	if dy <= size // 2:
		for i in range(dy):
			move(North)
	else:
		for i in range(size - dy):       # mais perto pelo Sul
			move(South)


# ============================================================================
# FERTILIZANTE com histerese: gasta ate acabar; depois so volta a gastar quando
# o estoque juntar LIMITE_FERTILIZANTE de novo.
# Atencao: planta fertilizada fica INFECTADA -> metade da colheita vira
# Weird_Substance (que alimenta os labirintos).
# ============================================================================

LIMITE_FERTILIZANTE = 50000
fertilizando = num_items(Items.Fertilizer) >= LIMITE_FERTILIZANTE


def pode_fertilizar():
	# chamar no drone principal, 1x por passada; o resultado vai pros outros drones
	global fertilizando
	qtd = num_items(Items.Fertilizer)
	if fertilizando and qtd < 1:
		fertilizando = False             # acabou: para de gastar
	elif not fertilizando and qtd >= LIMITE_FERTILIZANTE:
		fertilizando = True              # juntou 50k de novo: volta a gastar
	return fertilizando


def Fertilizar():
	# acelera a planta sob o drone ate ela ficar pronta (cada dose tira 2s do
	# crescimento). Para se nao conseguir usar: sem fertilizante ou sem planta.
	while not can_harvest():
		if not use_item(Items.Fertilizer):
			break


# ============================================================================
# CHAPEUS: cada funcao usa o seu, pra saber de longe o que esta rodando.
#   GRAMA  -> Straw_Hat     MADERA  -> Tree_Hat     CENOURA     -> Carrot_Hat
#   ABOBORA-> Pumpkin_Hat   CACTO   -> Cactus_Hat   POLICULTURA -> Green_Hat
#   FAZENDA-> Brown_Hat     MAZE    -> Wizard_Hat   segundoMAZE -> Gold_Hat
#   DINOSSAURO -> Dinosaur_Hat
# ============================================================================

def trocar_chapeu(chapeu):
	# equipa o chapeu pedido. Obs: sair do chapeu de dinossauro colhe a cauda (ossos).
	change_hat(chapeu)