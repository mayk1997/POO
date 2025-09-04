class Producto:
    def __init__(self, codigo, nombre, cantidad, precio):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio

    # Getters
    def get_codigo(self):
        return self.__codigo

    def get_nombre(self):
        return self.__nombre

    def get_cantidad(self):
        return self.__cantidad

    def get_precio(self):
        return self.__precio

    # Setters
    def set_nombre(self, nombre):
        self.__nombre = nombre

    def set_cantidad(self, cantidad):
        self.__cantidad = cantidad

    def set_precio(self, precio):
        self.__precio = precio

    def __str__(self):
        return f"{self.__nombre} | Cantidad: {self.__cantidad} | Precio: ${self.__precio:.2f}"


class Inventario:
    def __init__(self, archivo="inventario.txt"):
        self.productos = {}
        self.archivo = archivo
        self.cargar_desde_archivo()

    def guardar_en_archivo(self):
        """Guarda el inventario en archivo txt"""
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                for producto in self.productos.values():
                    f.write(f"{producto.get_codigo()},{producto.get_nombre()},{producto.get_cantidad()},{producto.get_precio()}\n")
            print(" Inventario guardado correctamente en el archivo.")
        except Exception as e:
            print(f" Error al guardar el archivo: {e}")

    def cargar_desde_archivo(self):
        """Carga los productos desde el archivo al iniciar el inventario."""
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    codigo, nombre, cantidad, precio = linea.strip().split(",")
                    self.productos[codigo] = Producto(codigo, nombre, int(cantidad), float(precio))
            print(" Inventario cargado desde el archivo.")
        except FileNotFoundError:
            print(" El archivo de inventario no existe, se creará al guardar.")
        except Exception as e:
            print(f" Error al leer el archivo: {e}")

    def agregar_producto(self, producto):
        if producto.get_codigo() in self.productos:
            print(" Error: El producto ya existe en el inventario.")
        else:
            self.productos[producto.get_codigo()] = producto
            self.guardar_en_archivo()
            print(" Producto agregado correctamente.")

    def eliminar_producto(self, codigo):
        if codigo in self.productos:
            del self.productos[codigo]
            self.guardar_en_archivo()
            print(" Producto eliminado correctamente.")
        else:
            print(" Error: Producto no encontrado.")

    def actualizar_producto(self, codigo, cantidad=None, precio=None):
        if codigo in self.productos:
            if cantidad is not None:
                self.productos[codigo].set_cantidad(cantidad)
            if precio is not None:
                self.productos[codigo].set_precio(precio)
            self.guardar_en_archivo()
            print(" Producto actualizado correctamente.")
        else:
            print(" Error: Producto no encontrado.")

    def buscar_producto(self, nombre):
        encontrados = False
        for producto in self.productos.values():
            if nombre.lower() in producto.get_nombre().lower():
                print(producto)
                encontrados = True
        if not encontrados:
            print(" No se encontró ningún producto con ese nombre.")

    def mostrar_inventario(self):
        if not self.productos:
            print(" El inventario está vacío.")
        else:
            print("\n Inventario de la Tienda:")
            for producto in self.productos.values():
                print(producto)


def menu():
    inventario = Inventario()
    while True:
        print("\n--- MENÚ DE INVENTARIO DE TIENDA ---")
        print("1. Agregar Producto")
        print("2. Eliminar Producto")
        print("3. Actualizar Producto")
        print("4. Buscar Producto")
        print("5. Mostrar Inventario")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == '6':
            print(" Saliendo del sistema de inventario...")
            break
        elif opcion == '1':
            try:
                codigo = input("Ingrese el código del producto: ")
                nombre = input("Ingrese el nombre del producto: ")
                cantidad = int(input("Ingrese la cantidad en stock: "))
                precio = float(input("Ingrese el precio del producto: "))
                producto = Producto(codigo, nombre, cantidad, precio)
                inventario.agregar_producto(producto)
            except ValueError:
                print(" Error: La cantidad debe ser un número entero y el precio un número decimal.")
        elif opcion == '2':
            codigo = input("Ingrese el código del producto a eliminar: ")
            inventario.eliminar_producto(codigo)
        elif opcion == '3':
            codigo = input("Ingrese el código del producto a actualizar: ")
            cantidad = input("Nueva cantidad (dejar en blanco para no cambiar): ")
            precio = input("Nuevo precio (dejar en blanco para no cambiar): ")
            try:
                cantidad = int(cantidad) if cantidad else None
                precio = float(precio) if precio else None
                inventario.actualizar_producto(codigo, cantidad, precio)
            except ValueError:
                print(" Error: La cantidad debe ser un número entero y el precio un número decimal.")
        elif opcion == '4':
            nombre = input("Ingrese el nombre del producto a buscar: ")
            inventario.buscar_producto(nombre)
        elif opcion == '5':
            inventario.mostrar_inventario()
        else:
            print(" Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    menu()