import Utilidades


def Abroba():
	
	podi = []
	tanao = 0
	tamanho = 0
		
	for v in range(get_world_size() * get_world_size()):
		if get_ground_type() !=  Grounds.Soil and get_entity_type() != Entities.Pumpkin:
			till()
			plant(Entities.Pumpkin)
		elif get_entity_type() != Entities.Pumpkin:
			plant(Entities.Pumpkin)
		if tamanho == 6:
			for i in range(tamanho):
				if podi[i] == Entities.Pumpkin:
					tanao = tanao + 1
			if tanao == 6:
				Utilidades.COLHER()
				tanao = 0
			else:
				tanao = 0
			if tamanho == 6 and tanao != 6:
				for i in range(tamanho):
					podi.pop()
				tanao = 0
		podi.append(get_entity_type())
		tamanho = len(podi)
		Utilidades.andar()