import Utilidades

def tratar():
	if get_ground_type() != Grounds.Grassland:
		till()                       # grama cresce sozinha em grama
	if can_harvest():
		harvest()

def Grama():
	Utilidades.for_all(tratar)
