import Utilidades

def tratar():
	if get_ground_type() != Grounds.Soil:
		till()
	if can_harvest():
		harvest()
	if get_entity_type() == None:
		plant(Entities.Carrot)
	if get_water() < 0.5:            # cada drone rega so as proprias casas -> sem corrida
		use_item(Items.Water)

def Cenora():
	Utilidades.for_all(tratar)
