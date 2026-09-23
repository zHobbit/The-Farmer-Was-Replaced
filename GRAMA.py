import Utilidades

def Grama():
	Utilidades.trocar_chapeu(Hats.Straw_Hat)
	fert = Utilidades.pode_fertilizar()      # decide 1x por passada (drone principal)

	def tratar():
		if get_ground_type() != Grounds.Grassland:
			till()                           # grama cresce sozinha em grama
		if fert:
			Utilidades.Fertilizar()
		if can_harvest():
			harvest()

	Utilidades.for_all(tratar)
