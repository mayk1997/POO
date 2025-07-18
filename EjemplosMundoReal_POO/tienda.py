class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
        self.mercancia = 10  # mercancia a reducir en venta


    def vender(self):
        if self.mercancia > 0:
            self.mercancia -= 1
            print(f"Se vendió 1 {self.nombre}. mercancia restante: {self.mercancia}")
        else:
            print(f"No hay mercancia disponible de {self.nombre}.")

    def __str__(self):
        return f"Producto: {self.nombre}, Precio: ${self.precio}, mercancia: {self.mercancia}"


class Cliente:
    def __init__(self, nombre):
        self.nombre = nombre

    def comprar_producto(self, producto):
        print(f"{self.nombre} está comprando {producto.nombre}...")
        producto.vender()

    def __str__(self):
        return f"Cliente: {self.nombre}"

# Ejemplo de uso
# Crear un producto
producto1 = Producto("Chocolate",2)

# Crear un cliente
cliente1 = Cliente("Carlos")

# Mostrar estado inicial
print(producto1)
print(cliente1)

# Cliente compra el producto
cliente1.comprar_producto(producto1)

# Mostrar estado final
print(producto1)