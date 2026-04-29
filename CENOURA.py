import Utilidades

def Cenora():
	Utilidades.COLHER()
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Carrot)
	Utilidades.POLICULTUTRA()
	Utilidades.REGAR()
	Utilidades.andar()