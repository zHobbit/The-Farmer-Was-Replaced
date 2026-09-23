import Utilidades

def Madera():
	Utilidades.trocar_chapeu(Hats.Tree_Hat)
	fert = Utilidades.pode_fertilizar()      # decide 1x por passada (drone principal)

	def tratar():
		if get_ground_type() != Grounds.Grassland:
			till()
		if get_entity_type() == None:
			plant(Entities.Tree)             # arvore rende mais madeira que arbusto
		if fert:
			Utilidades.Fertilizar()          # fica pronta na hora
		if can_harvest():
			harvest()
			plant(Entities.Tree)             # ja deixa a proxima crescendo

	Utilidades.for_all(tratar)
