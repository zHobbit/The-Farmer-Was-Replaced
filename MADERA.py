import Utilidades

def Madera():
	Utilidades.COLHER()
	n = get_pos_y() + get_pos_x()
	if Utilidades.is_even(n):
		plant(Entities.Tree)
	else:
		plant(Entities.Bush)
	Utilidades.POLICULTUTRA()
	Utilidades.andar()