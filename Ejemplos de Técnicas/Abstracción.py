
class Libro:

    def __init__(self, titulo, autor, paginas):
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas

    def leer(self):
        print(f"Estás leyendo '{self.titulo}' de {self.autor}.")

    def info(self):
        print(f"Título: {self.titulo}")
        print(f"Autor: {self.autor}")
        print(f"Páginas: {self.paginas}")

mi_libro = Libro("Harry Potter", "J.K. Rowling",223)
        # Mostrar información del libro
mi_libro.info()
        # Simular que lo estás leyendo
mi_libro.leer()