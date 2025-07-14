# Clase que representa una semana de clima para una ciudad
class ClimaSemana:
    def __init__(self, ciudad):
        self.__ciudad = ciudad
        self.__temperaturas = []

    # Metodo para las temperturas diarias
    def ingresar_temperaturas(self):
        print(f"\nIngrese las temperaturas para {self.__ciudad} - Semana 1")
        for dia in range(1, 8):  # 7 días
            while True:
                try:
                    temp = float(input(f"  Día {dia}: "))
                    self.__temperaturas.append(temp)
                    break
                except ValueError:
                    print("  ❌ Entrada inválida. Ingrese un número válido.")

    # Metodo para el promedio semanal
    def calcular_promedio(self):
        if self.__temperaturas:
            return sum(self.__temperaturas) / len(self.__temperaturas)
        else:
            return 0

    # Metodo para impimir el resultado
    def mostrar_promedio(self):
        promedio = self.calcular_promedio()
        print(f"\n📊 Promedio de temperaturas en {self.__ciudad}, Semana 1: {promedio:.2f}°C")


# funcion principal para temperatura de la ciudad
def main():
    semana = ClimaSemana("Ciudad 1")
    semana.ingresar_temperaturas()
    semana.mostrar_promedio()


# Ejecutar directamente
main()