"""
sistema_productos.py

Sistema de gestión de inventario de productos con interfaz Tkinter y persistencia en CSV.

"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv, os
from datetime import datetime

ARCHIVO_PRODUCTOS = "productos.csv"
ARCHIVO_HISTORIAL = "historial.csv"
ENCABEZADOS = ["id", "name", "category", "quantity", "price", "description"]


# ---------- Clase Producto ----------
class Producto:
    def __init__(self, id="", name="", category="", quantity=0, price=0.0, description=""):
        self.id = str(id)
        self.name = str(name)
        self.category = str(category)
        try:
            self.quantity = int(quantity)
        except (ValueError, TypeError):
            self.quantity = 0
        try:
            self.price = float(price)
        except (ValueError, TypeError):
            self.price = 0.0
        self.description = str(description)

    def a_lista(self):
        return [
            self.id,
            self.name,
            self.category,
            str(self.quantity),
            f"{self.price:.2f}",
            self.description
        ]

    @classmethod
    def desde_dict(cls, d):
        return cls(
            id=d.get("id", ""),
            name=d.get("name", ""),
            category=d.get("category", ""),
            quantity=d.get("quantity", 0),
            price=d.get("price", 0.0),
            description=d.get("description", "")
        )


# ---------- Clase GestorProductos ----------
class GestorProductos:
    def __init__(self, archivo=ARCHIVO_PRODUCTOS):
        self.archivo = archivo
        if not os.path.exists(self.archivo):
            self._crear_con_ejemplos()

    def _crear_con_ejemplos(self):
        ejemplos = [
            Producto(id="P001", name="Lapicero", category="Papelería", quantity=120, price=0.50, description="Azul"),
            Producto(id="P002", name="Cuaderno A4", category="Papelería", quantity=50, price=1.75, description="80 hojas"),
            Producto(id="P003", name="Mouse USB", category="Electrónica", quantity=20, price=8.99, description="Cable 1.2m"),
        ]
        self.guardar_todos(ejemplos)

    def cargar_todos(self):
        productos = []
        if not os.path.exists(self.archivo):
            return productos
        try:
            with open(self.archivo, newline="", encoding="utf-8") as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    row = {k: fila.get(k, "") for k in ENCABEZADOS}
                    productos.append(Producto.desde_dict(row))
        except Exception as e:
            print("Error al leer CSV:", e)
            return []
        return productos

    def guardar_todos(self, lista_productos):
        try:
            with open(self.archivo, "w", newline="", encoding="utf-8") as f:
                escritor = csv.writer(f)
                escritor.writerow(ENCABEZADOS)
                for producto in lista_productos:
                    escritor.writerow(producto.a_lista())
        except Exception as e:
            print("Error al guardar CSV:", e)

    def agregar_producto(self, producto: Producto):
        productos = self.cargar_todos()
        exist = {p.id: p for p in productos}
        exist[producto.id] = producto
        self.guardar_todos(list(exist.values()))
        self._registrar_historial("Agregar", producto.id, producto.name, producto.quantity, "Nuevo registro")

    def actualizar_producto(self, prod_id: str, nuevo_producto: Producto) -> bool:
        productos = self.cargar_todos()
        modificado = False
        for i, p in enumerate(productos):
            if p.id == prod_id:
                # calcular cambio de cantidad para historial
                diff = nuevo_producto.quantity - p.quantity
                productos[i] = nuevo_producto
                modificado = True
                self._registrar_historial("Actualizar", nuevo_producto.id, nuevo_producto.name, diff, "Edición")
                break
        if modificado:
            self.guardar_todos(productos)
        return modificado

    def eliminar_producto(self, prod_id: str) -> bool:
        productos = self.cargar_todos()
        filtrado = [p for p in productos if p.id != prod_id]
        if len(filtrado) == len(productos):
            return False
        self.guardar_todos(filtrado)
        self._registrar_historial("Eliminar", prod_id, "", 0, "Eliminado")
        return True

    def _registrar_historial(self, event, product_id, name, quantity_change, note):
        encabezados = ["timestamp", "event", "product_id", "name", "quantity_change", "note"]
        nuevo = [datetime.now().isoformat(), event, product_id, name, quantity_change, note]
        existe = os.path.exists(ARCHIVO_HISTORIAL)
        with open(ARCHIVO_HISTORIAL, "a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            if not existe:
                escritor.writerow(encabezados)
            escritor.writerow(nuevo)


# ---------- Interfaz gráfica ----------
class InterfazProductos:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("🛒 Sistema de Gestión de Productos")
        self.ventana.geometry("950x600")
        self.gestor = GestorProductos()
        self.productos = self.gestor.cargar_todos()
        self._crear_widgets()
        self.cargar_tabla()

    def _crear_widgets(self):
        marco_formulario = ttk.LabelFrame(self.ventana, text="Información del producto", padding=8)
        marco_formulario.pack(fill="x", padx=8, pady=8)

        campos = [
            ("ID", "id"), ("Nombre", "name"), ("Categoría", "category"),
            ("Cantidad", "quantity"), ("Precio", "price"), ("Descripción", "description")
        ]
        self.entradas = {}
        fila, col = 0, 0
        for etiqueta, clave in campos:
            lbl = ttk.Label(marco_formulario, text=f"{etiqueta}:")
            lbl.grid(row=fila, column=col * 2, padx=6, pady=4, sticky="w")
            ent = ttk.Entry(marco_formulario, width=30)
            ent.grid(row=fila, column=col * 2 + 1, padx=6, pady=4, sticky="w")
            self.entradas[clave] = ent
            col += 1
            if col >= 2:
                col = 0
                fila += 1

        marco_botones = ttk.Frame(self.ventana, padding=6)
        marco_botones.pack(fill="x", padx=8)
        ttk.Button(marco_botones, text="Agregar", command=self.agregar_producto).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Editar", command=self.editar_producto).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Eliminar", command=self.eliminar_producto).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Guardar cambios", command=self.guardar_cambios).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Importar CSV", command=self.importar_csv).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Exportar CSV", command=self.exportar_csv).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Limpiar campos", command=self.limpiar_campos).pack(side="left", padx=4)

        marco_tabla = ttk.Frame(self.ventana, padding=6)
        marco_tabla.pack(fill="both", expand=True, padx=8, pady=8)

        columnas = ENCABEZADOS[:]
        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings", selectmode="browse")
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize(), command=lambda c=col: self._ordenar_por(c, False))
            self.tabla.column(col, width=150, anchor="w")

        style = ttk.Style()
        style.configure("Treeview", foreground="black", rowheight=22)
        style.configure("Treeview.Heading", font=("TkDefaultFont", 9, "bold"))

        vsb = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tabla.pack(side="left", fill="both", expand=True)

        self.tabla.bind("<<TreeviewSelect>>", self.mostrar_detalles)

        self.estado_var = tk.StringVar(value="Listo")
        etiqueta_estado = ttk.Label(self.ventana, textvariable=self.estado_var, relief="sunken", anchor="w")
        etiqueta_estado.pack(side="bottom", fill="x")

    def cargar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        if self.productos is None:
            self.productos = []
        for p in self.productos:
            self.tabla.insert("", "end", values=p.a_lista())
        self.tabla.update_idletasks()

    def mostrar_detalles(self, event=None):
        sel = self.tabla.selection()
        if not sel: return
        vals = self.tabla.item(sel[0], "values")
        for i, clave in enumerate(ENCABEZADOS):
            ent = self.entradas.get(clave)
            if ent is not None:
                ent.delete(0, tk.END)
                ent.insert(0, vals[i])

    def _leer_formulario(self):
        datos = {clave: self.entradas[clave].get().strip() for clave in ENCABEZADOS}
        if not datos["id"] or not datos["name"]:
            messagebox.showwarning("Validación", "Debes ingresar al menos ID y Nombre.")
            return False, None
        try:
            quantity = int(datos["quantity"]) if datos["quantity"] else 0
        except ValueError:
            messagebox.showwarning("Validación", "Cantidad debe ser entero.")
            return False, None
        try:
            price = float(datos["price"]) if datos["price"] else 0.0
        except ValueError:
            messagebox.showwarning("Validación", "Precio debe ser número.")
            return False, None
        producto = Producto(
            id=datos["id"], name=datos["name"], category=datos["category"],
            quantity=quantity, price=price, description=datos["description"]
        )
        return True, producto

    def agregar_producto(self):
        ok, producto = self._leer_formulario()
        if not ok: return
        self.gestor.agregar_producto(producto)
        self.productos = self.gestor.cargar_todos()
        self.cargar_tabla()
        self.estado_var.set(f"Producto {producto.id} agregado.")
        self.limpiar_campos()

    def editar_producto(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un producto para editar.")
            return
        ok, producto = self._leer_formulario()
        if not ok: return
        id_actual = self.tabla.item(sel[0], "values")[0]
        success = self.gestor.actualizar_producto(id_actual, producto)
        if success:
            self.productos = self.gestor.cargar_todos()
            self.cargar_tabla()
            self.estado_var.set(f"Producto {id_actual} modificado.")
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "No se pudo modificar el producto (ID no encontrado).")

    def eliminar_producto(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un producto para eliminar.")
            return
        id_actual = self.tabla.item(sel[0], "values")[0]
        resp = messagebox.askyesno("Confirmar", f"¿Eliminar el producto con ID {id_actual}?")
        if not resp: return
        success = self.gestor.eliminar_producto(id_actual)
        if success:
            self.productos = self.gestor.cargar_todos()
            self.cargar_tabla()
            self.estado_var.set(f"Producto {id_actual} eliminado.")
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "No se encontró el producto a eliminar.")

    def guardar_cambios(self):
        nueva_lista = []
        for item in self.tabla.get_children():
            vals = self.tabla.item(item, "values")
            d = {k: vals[i] for i, k in enumerate(ENCABEZADOS)}
            nueva_lista.append(Producto.desde_dict(d))
        self.gestor.guardar_todos(nueva_lista)
        self.productos = self.gestor.cargar_todos()
        self.cargar_tabla()
        self.estado_var.set(f"Cambios guardados ({datetime.now().strftime('%H:%M:%S')}).")

    def importar_csv(self):
        ruta = filedialog.askopenfilename(title="Importar CSV", filetypes=[("Archivos CSV", "*.csv"), ("Todos", "*.*")])
        if not ruta: return
        try:
            with open(ruta, newline="", encoding="utf-8") as f:
                lector = csv.DictReader(f)
                importados = []
                for fila in lector:
                    row = {k: fila.get(k, "") for k in ENCABEZADOS}
                    importados.append(Producto.desde_dict(row))
            existentes = {p.id: p for p in self.gestor.cargar_todos()}
            for p in importados:
                existentes[p.id] = p
            combinados = list(existentes.values())
            self.gestor.guardar_todos(combinados)
            self.productos = self.gestor.cargar_todos()
            self.cargar_tabla()
            messagebox.showinfo("Importar", f"Importados {len(importados)} registros (merge realizado).")
            self.estado_var.set(f"Importados {len(importados)} registros desde {os.path.basename(ruta)}.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo importar CSV: {e}")

    def exportar_csv(self):
        ruta = filedialog.asksaveasfilename(title="Exportar CSV", defaultextension=".csv",
                                            filetypes=[("Archivos CSV", "*.csv"), ("Todos", "*.*")])
        if not ruta: return
        try:
            productos = self.gestor.cargar_todos()
            with open(ruta, "w", newline="", encoding="utf-8") as f:
                escritor = csv.writer(f)
                escritor.writerow(ENCABEZADOS)
                for p in productos:
                    escritor.writerow(p.a_lista())
            messagebox.showinfo("Exportar", f"Exportado {len(productos)} registros a {ruta}")
            self.estado_var.set(f"Exportado {len(productos)} registros a {os.path.basename(ruta)}.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar CSV: {e}")

    def limpiar_campos(self):
        for ent in self.entradas.values():
            ent.delete(0, tk.END)
        self.estado_var.set("Campos limpiados.")

    def _ordenar_por(self, col, descendente):
        datos = [(self.tabla.set(k, col), k) for k in self.tabla.get_children('')]
        try:
            datos.sort(key=lambda t: float(t[0]) if t[0] != "" else 0.0, reverse=descendente)
        except ValueError:
            datos.sort(key=lambda t: t[0].lower(), reverse=descendente)
        for index, (val, k) in enumerate(datos):
            self.tabla.move(k, '', index)
        self.tabla.heading(col, command=lambda c=col: self._ordenar_por(c, not descendente))


# ---------- Ejecutar aplicación ----------
def main():
    root = tk.Tk()
    app = InterfazProductos(root)
    root.mainloop()


if __name__ == "__main__":
    main()