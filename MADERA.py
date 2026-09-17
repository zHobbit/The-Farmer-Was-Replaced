import Utilidades

def tratar():
	if get_ground_type() != Grounds.Grassland:
		till()
	if can_harvest():
		harvest()
	if get_entity_type() == None:
		plant(Entities.Tree)         # arvore rende mais madeira que arbusto

def Madera():
	Utilidades.for_all(tratar)
