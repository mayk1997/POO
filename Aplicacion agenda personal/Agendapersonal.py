import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import json, os

try:
    from tkcalendar import DateEntry
    TKCALENDAR_OK = True
except ImportError:
    TKCALENDAR_OK = False

ARCHIVO_DATOS = "mis_eventos.json"


class GestorAgenda(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Eventos")
        self.geometry("1000x640")
        self.resizable(False, False)

        # Marco principal
        principal = ttk.Frame(self, padding=8)
        principal.pack(fill="both", expand=True)

        # Configuración de columnas
        principal.columnconfigure(0, weight=3)
        principal.columnconfigure(1, weight=1)

        # Crear las secciones
        self._construir_lista(principal)
        self._construir_formulario(principal)
        self._construir_botones(principal)

        # Cargar datos previos o ejemplos
        self._cargar_eventos()

    def _construir_lista(self, parent):
        marco_lista = ttk.LabelFrame(parent, text="Agenda de Eventos")
        marco_lista.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))

        columnas = ("fecha", "hora", "detalle")
        self.tabla = ttk.Treeview(marco_lista, columns=columnas, show="headings", height=20)
        for col, txt in zip(columnas, ("Fecha", "Hora", "Descripción")):
            self.tabla.heading(col, text=txt)

        self.tabla.column("fecha", width=100, anchor="center")
        self.tabla.column("hora", width=80, anchor="center")
        self.tabla.column("detalle", width=500, anchor="w")

        scroll = ttk.Scrollbar(marco_lista, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scroll.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.tabla.bind("<Double-1>", self._editar_evento)

    def _construir_formulario(self, parent):
        marco_form = ttk.LabelFrame(parent, text="Nuevo / Editar", padding=8)
        marco_form.grid(row=0, column=1, sticky="nsew")

        # Fecha
        ttk.Label(marco_form, text="Fecha:").grid(row=0, column=0, sticky="w")
        if TKCALENDAR_OK:
            self.campo_fecha = DateEntry(marco_form, date_pattern="dd/MM/yyyy")
        else:
            self.campo_fecha = ttk.Entry(marco_form)
            self.campo_fecha.insert(0, date.today().strftime("%d/%m/%Y"))
        self.campo_fecha.grid(row=0, column=1, pady=4, sticky="ew")

        # Hora
        ttk.Label(marco_form, text="Hora:").grid(row=1, column=0, sticky="w")
        self.campo_hora = ttk.Entry(marco_form)
        self.campo_hora.insert(0, "08:00")
        self.campo_hora.grid(row=1, column=1, pady=4, sticky="ew")

        # Descripción
        ttk.Label(marco_form, text="Descripción:").grid(row=2, column=0, sticky="nw")
        self.campo_desc = tk.Text(marco_form, width=25, height=6)
        self.campo_desc.grid(row=2, column=1, pady=4, sticky="ew")

        # Botones internos
        marco_bot = ttk.Frame(marco_form)
        marco_bot.grid(row=3, column=0, columnspan=2, pady=6, sticky="ew")
        ttk.Button(marco_bot, text="Guardar Evento", command=self.agregar_evento).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(marco_bot, text="Limpiar", command=self._limpiar_campos).pack(side="left", expand=True, fill="x", padx=2)

    def _construir_botones(self, parent):
        marco_acciones = ttk.LabelFrame(parent, text="Acciones")
        marco_acciones.grid(row=1, column=1, sticky="nsew", pady=(10,0))

        ttk.Button(marco_acciones, text="Eliminar Seleccionado", command=self.eliminar_evento).pack(fill="x", pady=4)
        ttk.Button(marco_acciones, text="Guardar Agenda", command=self._guardar_eventos).pack(fill="x", pady=4)
        ttk.Button(marco_acciones, text="Cerrar", command=self._salir).pack(fill="x", pady=4)

    # ---------------- Lógica ----------------
    def agregar_evento(self):
        fecha_txt = self.campo_fecha.get().strip()
        hora_txt = self.campo_hora.get().strip()
        descripcion = self.campo_desc.get("1.0", "end").strip()

        if not fecha_txt or not hora_txt or not descripcion:
            messagebox.showwarning("Campos vacíos", "Debes llenar todos los campos.")
            return

        try:
            datetime.strptime(fecha_txt, "%d/%m/%Y")
            datetime.strptime(hora_txt, "%H:%M")
        except ValueError:
            messagebox.showerror("Error de formato", "Usa formato DD/MM/YYYY y HH:MM (24h).")
            return

        self.tabla.insert("", "end", values=(fecha_txt, hora_txt, descripcion))
        self._ordenar_tabla()
        self._limpiar_campos()

    def eliminar_evento(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0], "values")
        if messagebox.askyesno("Confirmar", f"¿Eliminar el evento del {valores[0]} a las {valores[1]}?"):
            for s in seleccion:
                self.tabla.delete(s)

    def _salir(self):
        if messagebox.askyesno("Salir", "¿Quieres guardar los eventos antes de cerrar?"):
            self._guardar_eventos()
        self.destroy()

    # ---------------- Utilidades ----------------
    def _limpiar_campos(self):
        if TKCALENDAR_OK:
            self.campo_fecha.set_date(date.today())
        else:
            self.campo_fecha.delete(0, "end")
            self.campo_fecha.insert(0, date.today().strftime("%d/%m/%Y"))
        self.campo_hora.delete(0, "end")
        self.campo_hora.insert(0, "08:00")
        self.campo_desc.delete("1.0", "end")

    def _guardar_eventos(self):
        datos = []
        for item in self.tabla.get_children():
            f, h, d = self.tabla.item(item, "values")
            datos.append({"fecha": f, "hora": h, "descripcion": d})
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        messagebox.showinfo("Guardado", f"Se guardaron {len(datos)} evento(s).")

    def _cargar_eventos(self):
        if os.path.exists(ARCHIVO_DATOS):
            try:
                with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                    eventos = json.load(f)
                for ev in eventos:
                    self.tabla.insert("", "end", values=(ev["fecha"], ev["hora"], ev["descripcion"]))
                self._ordenar_tabla()
                return
            except Exception:
                pass

        hoy = date.today().strftime("%d/%m/%Y")
        ejemplos = [
            (hoy, "09:00", "Clase de inglés"),
            (hoy, "14:00", "Reunión de proyecto"),
            (hoy, "19:30", "Cenar con amigos")
        ]
        for e in ejemplos:
            self.tabla.insert("", "end", values=e)

    def _ordenar_tabla(self):
        filas = list(self.tabla.get_children())
        def clave(it):
            f, h, _ = self.tabla.item(it, "values")
            try:
                return datetime.strptime(f"{f} {h}", "%d/%m/%Y %H:%M")
            except:
                return datetime.max
        filas_ordenadas = sorted(filas, key=clave)
        for i, fila in enumerate(filas_ordenadas):
            self.tabla.move(fila, "", i)

    def _editar_evento(self, event):
        item = self.tabla.focus()
        if not item: return
        f, h, d = self.tabla.item(item, "values")
        VentanaEdicion(self, item, f, h, d, self._guardar_edicion)

    def _guardar_edicion(self, item, f, h, d):
        self.tabla.item(item, values=(f, h, d))
        self._ordenar_tabla()
        messagebox.showinfo("Editado", "Evento actualizado correctamente.")


class VentanaEdicion(tk.Toplevel):
    def __init__(self, padre, item, f, h, d, callback):
        super().__init__(padre)
        self.title("Editar Evento")
        self.geometry("320x240")
        self.resizable(False, False)
        self.item = item
        self.callback = callback

        ttk.Label(self, text="Fecha:").pack(anchor="w", padx=8, pady=2)
        if TKCALENDAR_OK:
            self.campo_fecha = DateEntry(self, date_pattern="dd/MM/yyyy")
            self.campo_fecha.set_date(datetime.strptime(f, "%d/%m/%Y"))
        else:
            self.campo_fecha = ttk.Entry(self)
            self.campo_fecha.insert(0, f)
        self.campo_fecha.pack(fill="x", padx=8)

        ttk.Label(self, text="Hora:").pack(anchor="w", padx=8, pady=2)
        self.campo_hora = ttk.Entry(self)
        self.campo_hora.insert(0, h)
        self.campo_hora.pack(fill="x", padx=8)

        ttk.Label(self, text="Descripción:").pack(anchor="w", padx=8, pady=2)
        self.campo_desc = tk.Text(self, height=5)
        self.campo_desc.insert("1.0", d)
        self.campo_desc.pack(fill="both", padx=8, pady=2)

        ttk.Button(self, text="Guardar", command=self._guardar).pack(side="left", expand=True, fill="x", padx=6, pady=6)
        ttk.Button(self, text="Cancelar", command=self.destroy).pack(side="left", expand=True, fill="x", padx=6, pady=6)

    def _guardar(self):
        f = self.campo_fecha.get().strip()
        h = self.campo_hora.get().strip()
        d = self.campo_desc.get("1.0", "end").strip()
        try:
            datetime.strptime(f, "%d/%m/%Y")
            datetime.strptime(h, "%H:%M")
        except ValueError:
            messagebox.showerror("Formato incorrecto", "Revisa la fecha y la hora.")
            return
        if not d:
            messagebox.showwarning("Sin descripción", "La descripción no puede estar vacía.")
            return
        self.callback(self.item, f, h, d)
        self.destroy()


if __name__ == "__main__":
    if not TKCALENDAR_OK:
        print("Nota: instala tkcalendar para usar el calendario visual.")
    app = GestorAgenda()
    app.mainloop()