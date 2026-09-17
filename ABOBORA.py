import Utilidades

def plantar():
	# so replanta casa vazia ou abobora morta (nao mexe nas vivas que ainda crescem).
	# plantar em cima de morta remove ela automaticamente.
	if get_entity_type() != Entities.Pumpkin:
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Pumpkin)

def Abroba():
	# replanta em paralelo ate o campo inteiro fundir numa abobora gigante, ai colhe.
	while not can_harvest():
		Utilidades.for_all(plantar)
	harvest()
