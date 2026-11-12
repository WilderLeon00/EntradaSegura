import tkinter as tk
from tkinter import ttk, messagebox

class menuClienteVentana:
    def __init__(self, ventanaPrinci, usuarios, nombre_cliente, cerrarSesion, boletos_db=None):
        self._ventana = ventanaPrinci
        self._usuarios = usuarios
        self.nombre_cliente = nombre_cliente
        self._cerrarSesion = cerrarSesion
        self.boletos_db = boletos_db if boletos_db is not None else {}

        # Ajustar tamaño cómodo para la ventana de cliente
        self._ventana.geometry("520x580")

        self.marco = tk.Frame(self._ventana)
        self.marco.pack(fill="both", expand=True, padx=20, pady=15)

        # --- Encabezado ---
        tk.Label(self.marco, text=f"Bienvenido, {self.nombre_cliente}", font=("Arial", 16, "bold")).pack(pady=(0, 5))
        tk.Label(self.marco, text="Panel de Compra de Boletos", font=("Arial", 11), fg="gray").pack(pady=(0, 15))

        # --- Tabla de Resumen de Zonas y Disponibilidad ---
        tk.Label(self.marco, text="Zonas y Disponibilidad:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        columnas = ("zona", "precio", "disponibles")
        self.tabla_zonas = ttk.Treeview(self.marco, columns=columnas, show="headings", height=4)
        self.tabla_zonas.heading("zona", text="Zona")
        self.tabla_zonas.heading("precio", text="Precio ($)")
        self.tabla_zonas.heading("disponibles", text="Disponibles")

        self.tabla_zonas.column("zona", width=150, anchor="center")
        self.tabla_zonas.column("precio", width=120, anchor="center")
        self.tabla_zonas.column("disponibles", width=120, anchor="center")
        self.tabla_zonas.pack(fill="x", pady=5)

        # --- Sección de Compra ---
        frame_compra = tk.LabelFrame(self.marco, text="Comprar Boleto", padx=10, pady=10)
        frame_compra.pack(fill="x", pady=10)

        tk.Label(frame_compra, text="Seleccione Zona:").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_zonas = ttk.Combobox(frame_compra, state="readonly", width=20)
        self.combo_zonas.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(
            frame_compra,
            text="Comprar Entrada",
            bg="#2e7d32",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.comprar_boleto
        ).grid(row=0, column=2, padx=5, pady=5)

        # --- Tabla de Mis Boletos Adquiridos ---
        tk.Label(self.marco, text="Mis Entradas Compradas:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 0))
        
        col_mis_boletos = ("codigo", "zona", "precio", "estado")
        self.tabla_mis_boletos = ttk.Treeview(self.marco, columns=col_mis_boletos, show="headings", height=5)
        self.tabla_mis_boletos.heading("codigo", text="Código")
        self.tabla_mis_boletos.heading("zona", text="Zona")
        self.tabla_mis_boletos.heading("precio", text="Precio")
        self.tabla_mis_boletos.heading("estado", text="Estado")

        self.tabla_mis_boletos.column("codigo", width=130, anchor="center")
        self.tabla_mis_boletos.column("zona", width=110, anchor="center")
        self.tabla_mis_boletos.column("precio", width=90, anchor="center")
        self.tabla_mis_boletos.column("estado", width=100, anchor="center")
        self.tabla_mis_boletos.pack(fill="x", pady=5)

        # --- Botón Cerrar Sesión ---
        tk.Button(self.marco, text="Cerrar Sesión", font=("Arial", 10), command=self.cerrar).pack(pady=15)

        # Cargar datos iniciales
        self.actualizar_vistas()

    def obtener_resumen_zonas(self):
        """Agrupa los datos de boletos_db para mostrarlos en la tabla de zonas"""
        resumen = {}
        for codigo, datos in self.boletos_db.items():
            zona = datos["zona"]
            if zona not in resumen:
                resumen[zona] = {"precio": datos["precio"], "capacidad": 0, "disponibles": 0}
            
            resumen[zona]["capacidad"] += 1
            if datos["estado"] == "DISPONIBLE":
                resumen[zona]["disponibles"] += 1
        return resumen

    def actualizar_vistas(self):
        # 1. Limpiar y llenar tabla de zonas
        for item in self.tabla_zonas.get_children():
            self.tabla_zonas.delete(item)

        resumen_zonas = self.obtener_resumen_zonas()
        lista_nombres_zonas = []

        for zona, info in resumen_zonas.items():
            self.tabla_zonas.insert("", tk.END, values=(zona, f"${info['precio']:.2f}", info["disponibles"]))
            if info["disponibles"] > 0:
                lista_nombres_zonas.append(zona)

        self.combo_zonas["values"] = lista_nombres_zonas
        if lista_nombres_zonas:
            self.combo_zonas.current(0)
        else:
            self.combo_zonas.set('')

        # 2. Limpiar y llenar tabla de boletos del cliente
        for item in self.tabla_mis_boletos.get_children():
            self.tabla_mis_boletos.delete(item)

        for codigo, datos in self.boletos_db.items():
            if datos["propietario"] == self.nombre_cliente:
                self.tabla_mis_boletos.insert("", tk.END, values=(codigo, datos["zona"], f"${datos['precio']:.2f}", datos["estado"]))

    def comprar_boleto(self):
        zona_seleccionada = self.combo_zonas.get()
        if not zona_seleccionada:
            messagebox.showwarning("Atención", "Selecciona una zona válida con disponibilidad.")
            return

        # Buscar el primer boleto disponible de esa zona y asignarlo
        codigo_asignado = None
        for codigo, datos in self.boletos_db.items():
            if datos["zona"] == zona_seleccionada and datos["estado"] == "DISPONIBLE":
                datos["estado"] = "VENDIDO"
                datos["propietario"] = self.nombre_cliente
                codigo_asignado = codigo
                break

        if codigo_asignado:
            messagebox.showinfo(
                "¡Compra Exitosa!",
                f"Has adquirido un boleto para la zona {zona_seleccionada}.\nTu código único es: {codigo_asignado}"
            )
            self.actualizar_vistas()
        else:
            messagebox.showerror("Agotado", f"Lo sentimos, ya no quedan boletos disponibles en la zona {zona_seleccionada}.")

    def cerrar(self):
        if hasattr(self, 'marco') and self.marco:
            try:
                self.marco.destroy()
            except Exception:
                pass
        self._cerrarSesion()