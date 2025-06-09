class Restaurante:

    def describir(self):
        print("Este es un restaurante general.")


class Pizzeria(Restaurante):

    def describir(self):
        print("Este restaurante ofrece pizzas artesanales.")


class Cafeteria(Restaurante):

    def describir(self):
        print("Este lugar sirve cafés y postres.")


def mostrar_descripcion(restaurante):
    restaurante.describir()

restaurante_general = Restaurante()
pizzeria = Pizzeria()
cafeteria = Cafeteria()

# Mostrar descripciones usando polimorfismo
mostrar_descripcion(restaurante_general)
mostrar_descripcion(pizzeria)
mostrar_descripcion(cafeteria)
