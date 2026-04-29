import GRAMA
import MADERA
import CENOURA
import ABOBORA
import Utilidades

clear()

while True:
	while num_items(Items.Hay) <= 64*64:
		GRAMA.Grama()
	while num_items(Items.Wood) <= num_items(Items.Hay):
		MADERA.Madera()
	while num_items(Items.Wood) >= 64:
		CENOURA.Cenora()
	while num_items(Items.Carrot) >= 64:
		ABOBORA.Abroba()