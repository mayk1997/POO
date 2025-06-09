class TarjetaCredito:

    def __init__(self, titular, limite):
        self.titular = titular
        self.__limite = limite
        self.__saldo = 0

    def comprar(self, monto):
        if self.__saldo + monto <= self.__limite:
            self.__saldo += monto
            print(f"Compra de {monto} realizada.")
        else:
            print("Compra rechazada: excede el límite.")

    def pagar(self, monto):
        if monto > 0:
            self.__saldo -= monto
            print(f"Pago de {monto} registrado.")

    def mostrar_saldo(self):
        print(f"Saldo actual: {self.__saldo}")
#EJEMPLO
tarjeta = TarjetaCredito("Juan Pérez", 1000)
tarjeta.comprar(200)
tarjeta.comprar(900)  # Debe rechazar porque excede el límite
tarjeta.pagar(150)