# Clase que simula una conexión a una base de datos
class ConexionBD:
    def __init__(self, nombre_bd):
        # Constructor: se ejecuta al crear el objeto
        self.nombre_bd = nombre_bd
        print(f"Conectado a la base de datos '{self.nombre_bd}'.")

    def ejecutar_consulta(self):
        # Metodo ingreso de consulta BUSQUEDA
        print(f"Ejecutando consulta en '{self.nombre_bd}'...")

    def __del__(self):
        # Destructor: se ejecuta al eliminar el objeto o al finalizar el programa
        print(f"Conexión con '{self.nombre_bd}' cerrada.")


# Bloque principal
if __name__ == "__main__":
    conexion = ConexionBD("clientes2025")  # Se llama al constructor
    conexion.ejecutar_consulta()

    del conexion  # Llamamos al destructor

    print("Fin del script.")