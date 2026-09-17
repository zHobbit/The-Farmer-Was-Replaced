import Utilidades

# ============================================================================
# plantar_e_colher(tipo): numa unica passada paralela (todos os drones), em cada
# casa faz TUDO de uma vez -> prepara o solo, colhe se estiver pronto e replanta
# se estiver vazia. Visitar a casa so uma vez (colher + plantar juntos) e' o que
# maximiza a eficiencia: sem varredura dupla e sem tempo ocioso entre acoes.
# ============================================================================

def precisa_solo(tipo):
	# cenoura, abobora, cacto e girassol crescem em solo arado; o resto em grama
	return (tipo == Entities.Carrot or tipo == Entities.Pumpkin
		or tipo == Entities.Cactus or tipo == Entities.Sunflower)


def plantar_e_colher(tipo):
	def tratar():
		# 1) garante o solo certo pro tipo
		if precisa_solo(tipo):
			if get_ground_type() != Grounds.Soil:
				till()
		else:
			if get_ground_type() != Grounds.Grassland:
				till()
		# 2) colhe se estiver pronto (mesma visita)
		if can_harvest():
			harvest()
		# 3) replanta se a casa ficou vazia (mesma visita)
		if get_entity_type() == None:
			plant(tipo)
		# 4) rega culturas de solo pra crescerem mais rapido (cada drone rega as suas)
		if precisa_solo(tipo) and get_water() < 0.5:
			use_item(Items.Water)

	Utilidades.for_all(tratar)
