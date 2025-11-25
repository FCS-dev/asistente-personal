"""
Diálogos UI adicionales requeridos.
Clases:
VentanaEstados(): manejo de cambios de estado
VentanaTags(): selección interactiva de tags
CuadrosEstadisticos(): generación con matplotlib para gráficos estadísticos
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
from utils.constantes import ESTADOS_VALIDOS


class VentanaEstados(simpledialog.Dialog):
    """
    Diálogo para cambiar el estado de una tarea.
    Muestra información actual y permite seleccionar nuevo estado.
    """

    def __init__(self, parent, title="Cambiar Estado", initial_data=None):
        """
        Args:
            parent: Widget padre (ventana principal)
            title: Título del diálogo
            initial_data: Dict con claves: tipo, id, tarea, fecha, prioridad, estado, tag
        """
        self.initial_data = initial_data or {}
        super().__init__(parent, title)

    def body(self, master):
        # Construye el cuerpo del diálogo.
        if self.initial_data.get("tipo") != "tarea":
            return None

        # Extraer datos
        tarea = self.initial_data.get("tarea", "")
        fecha = self.initial_data.get("fecha", "")
        prioridad = self.initial_data.get("prioridad", "")
        estado = self.initial_data.get("estado", "")
        tags = self.initial_data.get("tag", "")

        # Mostrar información actual
        tk.Label(master, text="Tarea").grid(row=0, column=0, sticky="e")
        tk.Label(master, text=tarea).grid(row=0, column=1, sticky="w")
        tk.Label(master, text="Fecha").grid(row=1, column=0, sticky="e")
        tk.Label(master, text=fecha).grid(row=1, column=1, sticky="w")
        tk.Label(master, text="Prioridad").grid(row=2, column=0, sticky="e")
        tk.Label(master, text=prioridad).grid(row=2, column=1, sticky="w")
        tk.Label(master, text="Tags").grid(row=3, column=0, sticky="e")
        tk.Label(master, text=tags).grid(row=3, column=1, sticky="w")
        tk.Label(master, text="Estado").grid(row=4, column=0, sticky="e")

        self.estado_var = tk.StringVar(value=estado)

        # Crear radiobuttons dinámicamente
        for idx, estado_opcion in enumerate(ESTADOS_VALIDOS):
            rb = tk.Radiobutton(
                master,
                text=estado_opcion,
                variable=self.estado_var,
                value=estado_opcion,
                command=self._actualizar_estado_entry,
            )
            rb.grid(row=4 + idx, column=1, sticky="w")

        # Entry interno para sincronización
        self.tarea_estado_entry = tk.Entry(master, width=11)
        self._actualizar_estado_entry()

        return self.tarea_estado_entry

    def _actualizar_estado_entry(self):
        # Sincroniza el entry con el radiobutton seleccionado.
        valor = self.estado_var.get()
        self.tarea_estado_entry.config(state="normal")
        self.tarea_estado_entry.delete(0, tk.END)
        self.tarea_estado_entry.insert(0, valor)
        self.tarea_estado_entry.config(state="readonly")

    def apply(self):
        # Guarda el resultado cuando se presiona OK.
        self.result = {
            "estado": self.tarea_estado_entry.get().strip(),
        }


class VentanaTags(simpledialog.Dialog):
    """
    Diálogo para seleccionar tags mediante checkboxes.
    Permite cargar tags de BD o de lista provista.
    """

    def __init__(
        self,
        parent,
        lista_tags=None,
        initial_tags=None,
        bd=None,
        tipo=None,
        title="Seleccionar Tags",
    ):
        """
        Args:
            parent: Widget padre (ventana principal)
            lista_tags: Lista de strings con tags disponibles
            initial_tags: Tags inicialmente seleccionados (str separado por comas o lista)
            bd: Instancia de Persistencia para cargar tags desde BD
            tipo: 'Tareas'|'Eventos'|'Notas' (necesario si se carga de BD)
            title: Título del diálogo
        """
        # Cargar lista de tags desde BD si no fue provista
        if lista_tags is None:
            if bd is not None and tipo is not None:
                try:
                    filas = bd.todos_los_tags(tipo)
                    lista_tags = [f[0] for f in filas]
                except Exception:
                    lista_tags = []
            else:
                lista_tags = []

        self.lista_tags = lista_tags

        # Normalizar tags iniciales
        if initial_tags:
            if isinstance(initial_tags, (list, tuple, set)):
                self.initial_tags = set([t.strip() for t in initial_tags])
            else:
                self.initial_tags = set(
                    [t.strip() for t in initial_tags.split(",") if t.strip()]
                )
        else:
            self.initial_tags = set()

        self.vars = []  # Lista de tuplas (tag, IntVar)
        super().__init__(parent, title)

    def body(self, master):
        # Construye el cuerpo del diálogo con checkboxes dinámicos.
        tk.Label(master, text="Selecciona los Tags:").grid(row=0, column=0, sticky="w")

        checkbox_frame = tk.Frame(master)
        checkbox_frame.grid(row=1, column=0, sticky="w")

        for tag in self.lista_tags:
            var = tk.IntVar()
            if tag in self.initial_tags:
                var.set(1)

            chk = tk.Checkbutton(checkbox_frame, text=tag, variable=var)
            chk.pack(anchor="w")
            self.vars.append((tag, var))

        return None

    def apply(self):
        # Guarda los tags seleccionados como cadena separada por comas.
        seleccionados = [tag for tag, var in self.vars if var.get() == 1]
        self.result = ",".join(seleccionados) if seleccionados else ""


class CuadrosEstadisticos(tk.Toplevel):
    """
    Ventana para mostrar gráficos estadísticos de tareas, eventos y notas.
    Contiene 3 botones para mostrar diferentes gráficos usando matplotlib.
    """

    def __init__(self, parent, bd=None, title="Cuadros Estadísticos"):
        """
        Args:
            parent: Widget padre (ventana principal)
            bd: Instancia de Persistencia para cargar info desde BD
            title: Título de la ventana
        """
        super().__init__(parent)
        self.title(title)
        self.bd = bd
        self.geometry("500x250")

        # Frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título
        titulo = tk.Label(
            main_frame,
            text="Gráficos disponibles",
            font=("Arial", 14, "bold"),
        )
        titulo.pack(pady=10)

        # Botones
        btn_tareas_tags = tk.Button(
            main_frame,
            text="Incidencia de Tags (Barras)",
            command=self.mostrar_grafico_tags,
            width=50,
            height=2,
        )
        btn_tareas_tags.pack(pady=5, fill=tk.BOTH)

        btn_eventos_intervalo = tk.Button(
            main_frame,
            text="Items por Intervalo de 3 días (Histograma)",
            command=self.mostrar_grafico_intervalo,
            width=50,
            height=2,
        )
        btn_eventos_intervalo.pack(pady=5, fill=tk.BOTH)

        btn_notas_dia = tk.Button(
            main_frame,
            text="Items creados por Día (Línea)",
            command=self.mostrar_grafico_por_dia,
            width=50,
            height=2,
        )
        btn_notas_dia.pack(pady=5, fill=tk.BOTH)

    def mostrar_grafico_tags(self):
        # Muestra gráfico de barras con incidencia de tags.
        if not self.bd:
            return
        try:
            import matplotlib.pyplot as plt

            tags_data = self.bd.obtener_tags()
            if not tags_data:
                messagebox.showwarning("Aviso", "No hay tags registrados")
                return
            tags = list(tags_data.keys())
            cantidades = list(tags_data.values())
            plt.figure(figsize=(10, 6))
            plt.bar(tags, cantidades, color="steelblue", edgecolor="navy")
            plt.title("Incidencia de Tags en Tareas", fontsize=14, fontweight="bold")
            plt.xlabel("Tags (Etiquetas)", fontsize=12)
            plt.ylabel("Cantidad de Tareas", fontsize=12)
            plt.xticks(rotation=45, ha="right")
            plt.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráfico: {str(e)}")

    def mostrar_grafico_intervalo(self):
        # Muestra histograma con eventos por intervalo de 3 días.
        if not self.bd:
            return
        try:
            import matplotlib.pyplot as plt

            eventos_data = self.bd.obtener_cantidad_por_dia()
            if not eventos_data:
                messagebox.showwarning("Aviso", "No hay datos registrados")
                return
            fechas = [item[0] for item in eventos_data]
            cantidades = [item[1] for item in eventos_data]

            plt.figure(figsize=(12, 6))
            plt.hist(
                cantidades,
                bins=3,
                color="coral",
                edgecolor="darkred",
            )
            plt.title(
                "Histograma: cantidad de items registrados. (Intervalo: 3 días)",
                fontsize=14,
                fontweight="bold",
            )
            plt.xlabel("Fechas", fontsize=12)
            plt.ylabel("Cantidad de Items", fontsize=12)
            plt.xticks(range(len(fechas)), fechas, rotation=45, ha="right")
            plt.grid(axis="y", alpha=0.3)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráfico: {str(e)}")

    def mostrar_grafico_por_dia(self):
        # Muestra gráfico de línea por día.
        if not self.bd:
            return
        try:
            import matplotlib.pyplot as plt

            items_data = self.bd.obtener_cantidad_por_dia()
            if not items_data:
                messagebox.showwarning("Aviso", "No hay datos registrados")
                return

            fechas = [item[0] for item in items_data]
            cantidades = [item[1] for item in items_data]

            plt.figure(figsize=(12, 6))
            plt.plot(
                range(len(fechas)),
                cantidades,
                marker="o",
                linestyle="-",
                color="green",
                linewidth=2,
                markersize=6,
                label="Tareas/Enventos/Notas por día",
            )
            plt.title(
                "Items creados por día",
                fontsize=14,
                fontweight="bold",
            )
            plt.xlabel("Fechas", fontsize=12)
            plt.ylabel("Cantidad", fontsize=12)
            plt.xticks(
                range(0, len(fechas), max(1, len(fechas) // 6)),
                [fechas[i] for i in range(0, len(fechas), max(1, len(fechas) // 6))],
                rotation=45,
                ha="right",
            )
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráfico: {str(e)}")
