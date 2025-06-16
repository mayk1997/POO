# Función para ingresar temperaturas diarias de una semana
def ingresar_temperaturas(semana):
    print(f"\nIngrese las temperaturas diarias - Semana {semana}")
    temperaturas = []
    for dia in range(1, 8):  # 7 días
        while True:
            try:
                temp = float(input(f"  Día {dia}: "))
                temperaturas.append(temp)
                break
            except ValueError:
                print(" Entrada inválida. Ingrese un número válido.")
    return temperaturas

# Función para calcular el promedio semanal
def calcular_promedio_semanal(temperaturas):
    return sum(temperaturas) / len(temperaturas)

# Función principal para una sola ciudad
def main():
    ciudad = "Ciudad 1"

    for semana in range(1, 5):  # 4 semanas
        temps = ingresar_temperaturas(semana)
        promedio = calcular_promedio_semanal(temps)
        print(f" Promedio de temperaturas en {ciudad}, Semana {semana}: {promedio:.2f}°C\n")

# Llamar a la función principal directamente
main()