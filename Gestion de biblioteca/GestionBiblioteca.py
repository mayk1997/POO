import ast

class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        self.__datos = (titulo, autor)  # tupla inmutable
        self.__categoria = categoria
        self.__isbn = isbn

    # Getters
    def get_titulo(self):
        return self.__datos[0]

    def get_autor(self):
        return self.__datos[1]

    def get_categoria(self):
        return self.__categoria

    def get_isbn(self):
        return self.__isbn

    def __str__(self):
        return f"{self.get_titulo()} por {self.get_autor()} | Categoría: {self.get_categoria()} | ISBN: {self.get_isbn()}"


class Usuario:
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.libros_prestados = []  # lista de ISBNs

    def __str__(self):
        return f"{self.nombre} (ID: {self.id_usuario}) - Libros prestados: {len(self.libros_prestados)}"


class Biblioteca:
    def __init__(self, archivo_libros="libros.txt", archivo_usuarios="usuarios.txt"):
        self.libros = {}  # ISBN -> Libro
        self.usuarios = {}  # ID -> Usuario
        self.ids_usuarios = set()
        self.archivo_libros = archivo_libros
        self.archivo_usuarios = archivo_usuarios
        self.cargar_libros()
        self.cargar_usuarios()

    # ----------------- Archivos -----------------
    def guardar_libros(self):
        try:
            with open(self.archivo_libros, "w", encoding="utf-8") as f:
                for libro in self.libros.values():
                    f.write(f"{libro.get_titulo()},{libro.get_autor()},{libro.get_categoria()},{libro.get_isbn()}\n")
            print("Libros guardados correctamente.")
        except Exception as e:
            print(f"Error al guardar libros: {e}")

    def cargar_libros(self):
        try:
            with open(self.archivo_libros, "r", encoding="utf-8") as f:
                for linea in f:
                    titulo, autor, categoria, isbn = linea.strip().split(",")
                    self.libros[isbn] = Libro(titulo, autor, categoria, isbn)
            print("Libros cargados desde archivo.")
        except FileNotFoundError:
            print("Archivo de libros no encontrado, se creará al guardar.")
        except Exception as e:
            print(f"Error al cargar libros: {e}")

    def guardar_usuarios(self):
        try:
            with open(self.archivo_usuarios, "w", encoding="utf-8") as f:
                for usuario in self.usuarios.values():
                    f.write(f"{usuario.id_usuario},{usuario.nombre},{usuario.libros_prestados}\n")
            print("Usuarios guardados correctamente.")
        except Exception as e:
            print(f"Error al guardar usuarios: {e}")

    def cargar_usuarios(self):
        try:
            with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                for linea in f:
                    id_usuario, nombre, libros_prestados = linea.strip().split(",", 2)
                    usuario = Usuario(nombre, id_usuario)
                    usuario.libros_prestados = ast.literal_eval(libros_prestados)
                    self.usuarios[id_usuario] = usuario
                    self.ids_usuarios.add(id_usuario)
            print("Usuarios cargados desde archivo.")
        except FileNotFoundError:
            print("Archivo de usuarios no encontrado, se creará al guardar.")
        except Exception as e:
            print(f"Error al cargar usuarios: {e}")

    # ----------------- Gestión de libros -----------------
    def agregar_libro(self, libro):
        if libro.get_isbn() in self.libros:
            print("Error: El libro ya existe.")
        else:
            self.libros[libro.get_isbn()] = libro
            self.guardar_libros()
            print("Libro agregado correctamente.")

    def eliminar_libro(self, isbn):
        if isbn in self.libros:
            del self.libros[isbn]
            self.guardar_libros()
            print("Libro eliminado correctamente.")
        else:
            print("Error: Libro no encontrado.")

    def buscar_libro(self, criterio):
        encontrados = False
        for libro in self.libros.values():
            if (criterio.lower() in libro.get_titulo().lower() or
                criterio.lower() in libro.get_autor().lower() or
                criterio.lower() in libro.get_categoria().lower()):
                print(libro)
                encontrados = True
        if not encontrados:
            print("No se encontraron libros con ese criterio.")

    # ----------------- Gestión de usuarios -----------------
    def registrar_usuario(self, usuario):
        if usuario.id_usuario in self.ids_usuarios:
            print("Error: ID de usuario ya registrado.")
        else:
            self.usuarios[usuario.id_usuario] = usuario
            self.ids_usuarios.add(usuario.id_usuario)
            self.guardar_usuarios()
            print("Usuario registrado correctamente.")

    def dar_baja_usuario(self, id_usuario):
        if id_usuario in self.ids_usuarios:
            del self.usuarios[id_usuario]
            self.ids_usuarios.remove(id_usuario)
            self.guardar_usuarios()
            print("Usuario dado de baja correctamente.")
        else:
            print("Error: Usuario no encontrado.")

    # ----------------- Préstamos -----------------
    def prestar_libro(self, id_usuario, isbn):
        if id_usuario not in self.ids_usuarios:
            print("Usuario no registrado.")
            return
        if isbn not in self.libros:
            print("Libro no disponible.")
            return
        usuario = self.usuarios[id_usuario]
        if isbn in usuario.libros_prestados:
            print("El usuario ya tiene este libro prestado.")
            return
        usuario.libros_prestados.append(isbn)
        self.guardar_usuarios()
        print(f"Libro '{self.libros[isbn].get_titulo()}' prestado a {usuario.nombre}.")

    def devolver_libro(self, id_usuario, isbn):
        if id_usuario not in self.ids_usuarios:
            print("Usuario no registrado.")
            return
        usuario = self.usuarios[id_usuario]
        if isbn in usuario.libros_prestados:
            usuario.libros_prestados.remove(isbn)
            self.guardar_usuarios()
            print(f"Libro '{self.libros[isbn].get_titulo()}' devuelto por {usuario.nombre}.")
        else:
            print("El usuario no tiene este libro prestado.")

    def listar_libros_prestados(self, id_usuario):
        if id_usuario not in self.ids_usuarios:
            print("Usuario no registrado.")
            return
        usuario = self.usuarios[id_usuario]
        if not usuario.libros_prestados:
            print("El usuario no tiene libros prestados.")
        else:
            print(f"Libros prestados por {usuario.nombre}:")
            for isbn in usuario.libros_prestados:
                print(self.libros[isbn])

# ----------------- Menú -----------------
def menu():
    biblioteca = Biblioteca()
    while True:
        print("\n--- MENÚ BIBLIOTECA DIGITAL ---")
        print("1. Agregar Libro")
        print("2. Eliminar Libro")
        print("3. Buscar Libro")
        print("4. Registrar Usuario")
        print("5. Dar de Baja Usuario")
        print("6. Prestar Libro")
        print("7. Devolver Libro")
        print("8. Listar Libros Prestados por Usuario")
        print("9. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == '9':
            print("Saliendo del sistema...")
            break
        elif opcion == '1':
            titulo = input("Título del libro: ")
            autor = input("Autor: ")
            categoria = input("Categoría: ")
            isbn = input("ISBN: ")
            libro = Libro(titulo, autor, categoria, isbn)
            biblioteca.agregar_libro(libro)
        elif opcion == '2':
            isbn = input("ISBN del libro a eliminar: ")
            biblioteca.eliminar_libro(isbn)
        elif opcion == '3':
            criterio = input("Ingrese título, autor o categoría para buscar: ")
            biblioteca.buscar_libro(criterio)
        elif opcion == '4':
            nombre = input("Nombre del usuario: ")
            id_usuario = input("ID de usuario: ")
            usuario = Usuario(nombre, id_usuario)
            biblioteca.registrar_usuario(usuario)
        elif opcion == '5':
            id_usuario = input("ID de usuario a dar de baja: ")
            biblioteca.dar_baja_usuario(id_usuario)
        elif opcion == '6':
            id_usuario = input("ID de usuario: ")
            isbn = input("ISBN del libro a prestar: ")
            biblioteca.prestar_libro(id_usuario, isbn)
        elif opcion == '7':
            id_usuario = input("ID de usuario: ")
            isbn = input("ISBN del libro a devolver: ")
            biblioteca.devolver_libro(id_usuario, isbn)
        elif opcion == '8':
            id_usuario = input("ID de usuario: ")
            biblioteca.listar_libros_prestados(id_usuario)
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu()