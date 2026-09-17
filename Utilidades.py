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
	
			
def move_to(x,y):
	distance_east = x - get_pos_x() 
	distance_north = y - get_pos_y()
	size = get_world_size()
	if distance_east < size / 2 or (distance_east < 0 and abs(distance_east) > size / 2):
		move_direction = East
	else:
		move_direction = West
	while get_pos_x() != x:
		move(move_direction)
	if distance_north < size / 2 or (distance_north < 0 and abs(distance_north) > size / 2):
		move_direction = North
	else:
		move_direction = South
	while get_pos_y() != y:
		move(move_direction)