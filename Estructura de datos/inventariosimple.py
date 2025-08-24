class Articulo:
    def __init__(self, codigo, nombre, stock, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.stock = stock
        self.precio = precio

    def __str__(self):
        return f"{self.nombre} | Stock: {self.stock} | Precio: ${self.precio:.2f}"


class InventarioTienda:
    def __init__(self):
        self.articulos = {}

    def agregar_articulo(self, articulo):
        if articulo.codigo in self.articulos:
            print(" Error: El artículo ya existe en el inventario.")
        else:
            self.articulos[articulo.codigo] = articulo
            print(" Artículo agregado correctamente.")

    def eliminar_articulo(self, codigo):
        if codigo in self.articulos:
            del self.articulos[codigo]
            print(" Artículo eliminado.")
        else:
            print(" Error: Artículo no encontrado.")

    def actualizar_articulo(self, codigo, stock=None, precio=None):
        if codigo in self.articulos:
            if stock is not None:
                self.articulos[codigo].stock = stock
            if precio is not None:
                self.articulos[codigo].precio = precio
            print(" Artículo actualizado.")
        else:
            print(" Error: Artículo no encontrado.")

    def buscar_articulo(self, nombre):
        encontrados = False
        for articulo in self.articulos.values():
            if nombre.lower() in articulo.nombre.lower():
                print(articulo)
                encontrados = True
        if not encontrados:
            print(" No se encontró ningún artículo con ese nombre.")

    def mostrar_inventario(self):
        if not self.articulos:
            print(" El inventario está vacío.")
        else:
            print("\n Inventario de la Tienda:")
            for articulo in self.articulos.values():
                print(articulo)


def menu():
    inventario = InventarioTienda()
    while True:
        print("\n--- MENÚ DE INVENTARIO DE TIENDA ---")
        print("1. Agregar Artículo")
        print("2. Eliminar Artículo")
        print("3. Actualizar Artículo")
        print("4. Buscar Artículo")
        print("5. Mostrar Inventario")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == '6':
            print("Saliendo del sistema de inventario...")
            break
        elif opcion == '1':
            codigo = input("Ingrese el código del artículo: ")
            nombre = input("Ingrese el nombre del artículo: ")
            stock = int(input("Ingrese la cantidad en stock: "))
            precio = float(input("Ingrese el precio del artículo: "))
            articulo = Articulo(codigo, nombre, stock, precio)
            inventario.agregar_articulo(articulo)
        elif opcion == '2':
            codigo = input("Ingrese el código del artículo a eliminar: ")
            inventario.eliminar_articulo(codigo)
        elif opcion == '3':
            codigo = input("Ingrese el código del artículo a actualizar: ")
            stock = input("Nuevo stock (dejar en blanco para no cambiar): ")
            precio = input("Nuevo precio (dejar en blanco para no cambiar): ")
            stock = int(stock) if stock else None
            precio = float(precio) if precio else None
            inventario.actualizar_articulo(codigo, stock, precio)
        elif opcion == '4':
            nombre = input("Ingrese el nombre del artículo a buscar: ")
            inventario.buscar_articulo(nombre)
        elif opcion == '5':
            inventario.mostrar_inventario()
        else:
            print("Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    menu()
