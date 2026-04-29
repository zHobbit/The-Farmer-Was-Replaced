import Utilidades

def Maze():
	for i in range(get_world_size() * get_world_size()):
		Utilidades.COLHER()
		plant(Entities.Bush)
		Utilidades.andar()
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)
	birinto =  True
	while birinto == True:
		andar_na_parede()
						
		
def andar_na_parede():
	
	def anda_memo():
		 
		str : ultimo_mov
		
		if can_move(West) == False and can_move(North) == False and can_move(East) == False:
			if ultimo_mov != "South"
				move(South)
				ultimo_mov = "South"
			elif can_move(West) == False and can_move(South) == False and can_move(East) == False:
				move(North)
				if can_move(South) == False and can_move(North) == False and can_move(East) == False:
					move(West)
				elif can_move(West) == False and can_move(North) == False and can_move(South) == False:
					move(East) 
				elif can_move(West) == False and can_move(South) == False and can_move(East) == False:
					move(North)
				elif can_move(South) == False and can_move(North) == False and can_move(East) == False:
					move(West)
				elif can_move(West) == False and can_move(North) == False and can_move(South) == False:
					move(East)
			
	while get_entity_type() != Entities.Treasure:
		anda_memo()
	harvest()
	