import tkinter as tk
from tkinter import messagebox, ttk
from registro_usuario import RegistroUsuarioVentana

class menuAdminVentana:
    def __init__(self, ventanaPrinci, usuarios, nombre_usuario, cerrarSesion, boletos_db=None):
        self._ventana = ventanaPrinci
        self._usuarios = usuarios
        self.nombre_usuario = nombre_usuario
        self._cerrarSesion = cerrarSesion

        # Inicializar la base de datos compartida de boletos si no viene creada
        # Estructura: {"VIP-001": {"estado": "DISPONIBLE", "zona": "VIP", "precio": 100.0, "propietario": None}}
        self.boletos_db = boletos_db if boletos_db is not None else {}

        # Único marco principal limpio
        self.marco = tk.Frame(self._ventana)
        self.marco.pack(fill="both", expand=True, padx=20, pady=15)

        tk.Label(self.marco, text="Panel de Administrador", font=("Arial", 16, "bold")).pack(pady=5)
        tk.Label(self.marco, text=f"Bienvenido, {self.nombre_usuario}", font=("Arial", 11), fg="gray").pack(pady=(0, 10))

        # --- Sección de Creación de Zonas ---
        frame_creacion = tk.LabelFrame(self.marco, text="Gestión de Zonas y Aforo", padx=10, pady=10)
        frame_creacion.pack(fill="x", pady=5)

        tk.Label(frame_creacion, text="Nombre de la zona:").pack(anchor="w")
        self.entry_zona = tk.Entry(frame_creacion, font=("Arial", 10))
        self.entry_zona.pack(fill="x", pady=2)

        tk.Label(frame_creacion, text="Capacidad / Cantidad de boletos:").pack(anchor="w")
        self.entry_capacidad = tk.Entry(frame_creacion, font=("Arial", 10))
        self.entry_capacidad.pack(fill="x", pady=2)

        tk.Label(frame_creacion, text="Precio por boleto ($):").pack(anchor="w")
        self.entry_precio = tk.Entry(frame_creacion, font=("Arial", 10))
        self.entry_precio.pack(fill="x", pady=2)

        tk.Button(
            frame_creacion, 
            text="Crear Zona y Generar Boletos", 
            font=("Arial", 10, "bold"), 
            command=self.crear_zona_boletos
        ).pack(pady=8, fill="x")

        # --- Tabla de Zonas Registradas ---
        tk.Label(self.marco, text="Zonas registradas en el evento:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 2))

        tabla_frame = tk.Frame(self.marco)
        tabla_frame.pack(fill="x", pady=2)

        self.tabla_zonas = ttk.Treeview(tabla_frame, columns=("Zona", "Capacidad", "Precio"), show="headings", height=4)
        self.tabla_zonas.heading("Zona", text="Nombre de Zona")
        self.tabla_zonas.heading("Capacidad", text="Capacidad")
        self.tabla_zonas.heading("Precio", text="Precio ($)")
        self.tabla_zonas.column("Zona", width=120, anchor="center")
        self.tabla_zonas.column("Capacidad", width=100, anchor="center")
        self.tabla_zonas.column("Precio", width=100, anchor="center")
        self.tabla_zonas.pack(side="left", fill="x", expand=True)

        # --- Botones de Gestión de Usuarios ---
        tk.Button(self.marco, text="Registrar nuevo Empleado", font=("Arial", 10), command=self.abrir_registro_empleados).pack(pady=4, fill="x")
        tk.Button(self.marco, text="Ver lista de usuarios", font=("Arial", 10), command=self.verUsuarios).pack(pady=4, fill="x")
        
        # --- Botón Cerrar Sesión ---
        tk.Button(self.marco, text="Cerrar sesión", font=("Arial", 10, "bold"), command=self.cerrar).pack(pady=10, fill="x")

    def crear_zona_boletos(self):
        nombre_zona = self.entry_zona.get().strip().upper()
        capacidad_str = self.entry_capacidad.get().strip()
        precio_str = self.entry_precio.get().strip()

        if not nombre_zona or not capacidad_str or not precio_str:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos de la zona.")
            return

        try:
            capacidad = int(capacidad_str)
            precio = float(precio_str)
            if capacidad <= 0 or precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La capacidad debe ser un entero mayor a 0 y el precio un número válido.")
            return

        # Verificar si la zona ya existe en la tabla
        for row_id in self.tabla_zonas.get_children():
            values = self.tabla_zonas.item(row_id, "values")
            if values[0] == nombre_zona:
                messagebox.showwarning("Duplicado", f"La zona '{nombre_zona}' ya se encuentra registrada.")
                return

        # Generar los boletos individuales en la base de datos compartida
        prefijo = nombre_zona[:3]
        for i in range(1, capacidad + 1):
            codigo_boleto = f"{prefijo}-{i:03d}"
            if codigo_boleto not in self.boletos_db:
                self.boletos_db[codigo_boleto] = {
                    "estado": "DISPONIBLE",
                    "zona": nombre_zona,
                    "precio": precio,
                    "propietario": None
                }

        # Insertar en la tabla visual del admin
        self.tabla_zonas.insert("", tk.END, values=(nombre_zona, capacidad, f"${precio:.2f}"))

        messagebox.showinfo("Éxito", f"Zona '{nombre_zona}' creada con éxito y {capacidad} boletos generados.")
        self.entry_zona.delete(0, tk.END)
        self.entry_capacidad.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)

    def abrir_registro_empleados(self):
        RegistroUsuarioVentana(self._ventana, self._usuarios, ["empleado", "administrador"])

    def verUsuarios(self):
        total = len(self._usuarios)
        messagebox.showinfo("Usuarios", f"Hay {total} usuarios registrados en el sistema.")

    def cerrar(self):
        if hasattr(self, 'marco') and self.marco:
            try:
                self.marco.destroy()
            except Exception:
                pass
        self._cerrarSesion()