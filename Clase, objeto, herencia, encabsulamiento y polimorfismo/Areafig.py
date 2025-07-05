# Clase base
class Figura:
    def __init__(self, nombre):
        self.nombre = nombre

    def area(self):

        return 0

    def descripcion(self):
        return f"Figura geométrica: {self.nombre}"

# Clase derivada para Rectangulo
class Rectangulo(Figura):
    def __init__(self, ancho, alto):
        super().__init__("Rectángulo")
        #atributos privados (encapsulamiento)
        self.__ancho = ancho
        self.__alto = alto

    # Polimorfismo sobreescrito en area()
    def area(self):

        return self.__ancho * self.__alto

    # Polimorfismo sobreescrito en descripcion ()
    def descripcion(self):
        return f"{super().descripcion()} con ancho={self.__ancho} y alto={self.__alto}"

# Clase derivada Circulo
class Circulo(Figura):
    def __init__(self, radio):
        super().__init__("Círculo")
        #atributo privado
        self.__radio = radio

    # Polimorfismo sobreescrito en area()
    def area(self):

        return 3.1416 * (self.__radio ** 2)

    # Polimorfismo sobreescrito en descripcion ()
    def descripcion(self):
        return f"{super().descripcion()} con radio={self.__radio}"

def main():

    rect = Rectangulo(5, 3)
    circ = Circulo(4)

    print("\n--- Rectángulo ---")
    print(rect.descripcion())  # imprime el metodo descripcion
    print(f"Área: {rect.area()}")  # Llama al metodo sobrescrito area

    print("\n--- Círculo ---")
    print(circ.descripcion())  # imprime el metodo descripción
    print(f"Área: {circ.area()}")  # Llama al metodo sobrescrito area

if __name__ == "__main__":
    main()