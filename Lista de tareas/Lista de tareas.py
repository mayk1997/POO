import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, csv, os, uuid
from datetime import datetime

try:
    from tkcalendar import DateEntry
    CALENDAR = True
except ImportError:
    CALENDAR = False


class GestorDeTareas:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestor de Tareas - Tkinter")
        self.archivo_datos = "datos_tareas.json"
        self.lista_tareas = []

        self.construir_ui()
        self.cargar_datos()
        self.actualizar_lista()

    def construir_ui(self):
        # --- parte superior ---
        marco_top = ttk.Frame(self.master, padding=5)
        marco_top.pack(fill="x")

        self.entrada = ttk.Entry(marco_top)
        self.entrada.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entrada.bind("<Return>", lambda e: self.agregar())

        self.nivel = tk.StringVar(value="Normal")
        ttk.Combobox(marco_top, textvariable=self.nivel,
                     values=["Baja", "Normal", "Alta"], state="readonly").pack(side="left", padx=5)

        if CALENDAR:
            self.fecha = DateEntry(marco_top, width=12)
        else:
            self.fecha = ttk.Entry(marco_top, width=12)
            self.fecha.insert(0, "YYYY-MM-DD")
        self.fecha.pack(side="left", padx=5)

        ttk.Button(marco_top, text="Agregar", command=self.agregar).pack(side="left", padx=5)
        ttk.Button(marco_top, text="Finalizar", command=self.cambiar_estado).pack(side="left", padx=5)
        ttk.Button(marco_top, text="Borrar", command=self.eliminar).pack(side="left", padx=5)

        # --- filtros ---
        marco_filtros = ttk.Frame(self.master, padding=5)
        marco_filtros.pack(fill="x")

        ttk.Label(marco_filtros, text="Buscar:").pack(side="left")
        self.buscar_txt = tk.StringVar()
        ttk.Entry(marco_filtros, textvariable=self.buscar_txt).pack(side="left", fill="x", expand=True, padx=5)
        self.buscar_txt.trace_add("write", lambda *args: self.actualizar_lista())

        self.estado_filtro = tk.StringVar(value="Todas")
        ttk.Combobox(marco_filtros, textvariable=self.estado_filtro,
                     values=["Todas", "Activas", "Completadas"], state="readonly").pack(side="left", padx=5)
        self.estado_filtro.trace_add("write", lambda *args: self.actualizar_lista())

        self.nivel_filtro = tk.StringVar(value="Todas")
        ttk.Combobox(marco_filtros, textvariable=self.nivel_filtro,
                     values=["Todas", "Baja", "Normal", "Alta"], state="readonly").pack(side="left", padx=5)
        self.nivel_filtro.trace_add("write", lambda *args: self.actualizar_lista())

        # --- tabla ---
        columnas = ("Descripción", "Prioridad", "Fecha límite", "Estado")
        self.tabla = ttk.Treeview(self.master, columns=columnas, show="headings", selectmode="extended", height=18)
        for col in columnas:
            self.tabla.heading(col, text=col)
            ancho = 200 if col == "Descripción" else 120
            self.tabla.column(col, width=ancho, anchor="center")
        self.tabla.pack(fill="both", expand=True, padx=5, pady=5)

        self.tabla.bind("<Double-1>", lambda e: self.cambiar_estado())
        self.master.bind("<Delete>", lambda e: self.eliminar())

    def agregar(self):
        texto = self.entrada.get().strip()
        if not texto:
            messagebox.showwarning("Aviso", "La tarea no puede estar vacía")
            return

        if CALENDAR:
            fecha_limite = self.fecha.get_date().strftime("%Y-%m-%d")
        else:
            raw = self.fecha.get().strip()
            try:
                datetime.strptime(raw, "%Y-%m-%d")
                fecha_limite = raw
            except Exception:
                fecha_limite = ""

        nueva = {
            "id": str(uuid.uuid4()),
            "texto": texto,
            "prioridad": self.nivel.get(),
            "fecha": fecha_limite,
            "hecha": False
        }
        self.lista_tareas.append(nueva)
        self.entrada.delete(0, tk.END)
        self.guardar()
        self.actualizar_lista()

    def cambiar_estado(self):
        for item in self.tabla.selection():
            tid = self.tabla.item(item, "tags")[0]
            for t in self.lista_tareas:
                if t["id"] == tid:
                    t["hecha"] = not t["hecha"]
        self.guardar()
        self.actualizar_lista()

    def eliminar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar tareas seleccionadas?"):
            return
        ids = [self.tabla.item(i, "tags")[0] for i in seleccion]
        self.lista_tareas = [t for t in self.lista_tareas if t["id"] not in ids]
        self.guardar()
        self.actualizar_lista()

    def actualizar_lista(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        buscar = (self.buscar_txt.get() or "").lower()
        est = self.estado_filtro.get()
        niv = self.nivel_filtro.get()

        for t in self.lista_tareas:
            if buscar and buscar not in t["texto"].lower() and buscar not in t["fecha"].lower():
                continue
            if est == "Activas" and t["hecha"]:
                continue
            if est == "Completadas" and not t["hecha"]:
                continue
            if niv != "Todas" and t["prioridad"] != niv:
                continue

            estado = "Completada" if t["hecha"] else "Pendiente"
            self.tabla.insert("", "end",
                              values=(t["texto"], t["prioridad"], t["fecha"], estado),
                              tags=(t["id"],))

    def guardar(self):
        with open(self.archivo_datos, "w", encoding="utf-8") as f:
            json.dump(self.lista_tareas, f, indent=2, ensure_ascii=False)

    def cargar_datos(self):
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, "r", encoding="utf-8") as f:
                    self.lista_tareas = json.load(f)
            except Exception:
                self.lista_tareas = []


if __name__ == "__main__":
    root = tk.Tk()
    app = GestorDeTareas(root)
    root.mainloop()