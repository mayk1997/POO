class Instrumento:

    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo

    def tocar(self):
        print("Tocando", self.nombre)


class Guitarra(Instrumento):

    def __init__(self, nombre, tipo, cuerdas):
        super().__init__(nombre, tipo)
        self.cuerdas = cuerdas

    def afinar(self):
        print("Afinando las", self.cuerdas, "cuerdas de la guitarra")


class Piano(Instrumento):

    def __init__(self, nombre, tipo, teclas):
        super().__init__(nombre, tipo)
        self.teclas = teclas

    def afinar(self):
        print("Afinando un piano con", self.teclas, "teclas")

guitarra = Guitarra("Gibson Les Paul", "Eléctrica", 6)
piano = Piano("Yamaha C7", "Acústico", 88)

# APLICAMOS EL METODO
guitarra.tocar()
guitarra.afinar()

piano.tocar()
piano.afinar()