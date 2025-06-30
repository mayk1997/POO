# Programa para calcular el área de un rectángulo

# Función que calcula el área dada la base y la altura
def calcular_area_rectangulo(base, altura):
    area = base * altura
    return area

# Variables que almacenan las dimensiones del rectángulo
base_rectangulo = 5.5       # float
altura_rectangulo = 3.4      # float

# Variable que indica si las dimensiones son válidas (boolean)
dimensiones_validas = base_rectangulo > 0 and altura_rectangulo > 0

# Variable que almacena el mensaje de resultado (string)
mensaje_resultado = ""

if dimensiones_validas:
    area_rectangulo = calcular_area_rectangulo(base_rectangulo, altura_rectangulo)
    mensaje_resultado = f"El área del rectángulo con base {base_rectangulo} y altura {altura_rectangulo} es {area_rectangulo}."
else:
    mensaje_resultado = "Las dimensiones deben ser mayores que cero."

print(mensaje_resultado)