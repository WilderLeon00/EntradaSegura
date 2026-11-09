import tkinter as tk
from tkinter import messagebox, ttk
from registro_usuario import RegistroUsuarioVentana

class menuAdminVentana:
    def __init__(self, ventanaPrinci, usuarios, nombre_usuario, cerrarSesion, boletos_db = None ):
        self._ventana = ventanaPrinci
        self._usuarios = usuarios
        self.nombre_usuario = nombre_usuario
        self._cerrarSesion = cerrarSesion

        self.marco = tk.Frame(self._ventana)
        self.marco.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(self.marco, text="Panel de Administrador", font=("Arial", 17, "bold")).pack(pady=10)
        tk.Label(self.marco, text=f"Bienvenido, {self.nombre_usuario}", font=("Arial", 12)).pack(pady=4)

        self.boletos_db = boletos_db if boletos_db is not None else {}

        self.marco = tk.Frame(self._ventana)
        self.marco.pack(fill="both", expand=True, padx=20, pady=20)

        

        tk.Label(self.marco, text="Gestion de zona y aforo", font=("Arial", 11, "bold")).pack(pady=(8, 2))

        tk.Label(self.marco, text="Nombre de la zona...").pack(anchor="w")
        self.entry_zona = tk.Entry(self.marco, font=("Arial", 10))
        self.entry_zona.pack(fill="x", pady=2)

        tk.Label(self.marco, text="Capacidad y cantidad de boletos: ").pack(anchor="w")
        self.entry_capacidad = tk.Entry(self.marco, font=("Arial", 10))
        self.entry_capacidad.pack(fill="x", pady=2)

        tk.Button(self.marco, text="Crear Zona y Boletos", font=("Arial", 10, "bold"), command=self.crear_zona_boletos).pack(pady=6, fill="x")


        tk.Label(self.marco, text="Zonas registradas en el evento:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,2))

        tabla_frame = tk.Frame(self.marco)
        tabla_frame.pack(fill="x", pady=2)

        self.tabla_zonas = ttk.Treeview(tabla_frame, columns=("Zona", "Capacidad"), show="headings", height=4)
        self.tabla_zonas.heading("Zona", text="Nombre de Zona")
        self.tabla_zonas.heading("Capacidad", text="Capacidad / Boletos")
        self.tabla_zonas.column("Zona", width=150, anchor="center")
        self.tabla_zonas.column("Capacidad", width=150, anchor="center")
        self.tabla_zonas.pack(side="left", fill="x", expand=True)
        

        tk.Button(self.marco, text="Registrar nuevo Empleado", font=("Arial", 10, "bold"), command=self.abrir_registro_empleados).pack(pady=6, fill="x")
        tk.Button(self.marco, text="Ver lista de usuarios", command=self.verUsuarios).pack(pady=4, fill="x")
        tk.Button(self.marco, text="Cerrar sesion", command=self.cerrar).pack(pady=10, fill="x")

    def crear_zona_boletos(self):
        nombre_zona = self.entry_zona.get().strip().upper()
        capacidad = self.entry_capacidad.get().strip()

        if not nombre_zona or not capacidad:
            messagebox.showwarning("campos vacios, por favor ingresar el nombre de la zona.")
            return

        try:
            capacidad = int(capacidad)
            if capacidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error, la capacidad debe ser mayor a 0")
            return
        for row_id in self.tabla_zonas.get_children():
            values = self.tabla_zonas.item(row_id, "values")
            if values[0] == nombre_zona:
                messagebox.showwarning("Duplicado", f"La zona '{nombre_zona}' ya se encuentra registrada.")
                return

        for i in range(1, capacidad + 1):
            codigo_boleto = f"{nombre_zona}-{i:03d}"
            if codigo_boleto not in self.boletos_db:
                self.boletos_db[codigo_boleto] = False

        self.tabla_zonas.insert("", tk.END, values=(nombre_zona, capacidad))

        messagebox.showwarning("Exito, "f"Zona {nombre_zona} , creada con exito y genero con capacidad {capacidad}")
        self.entry_zona.delete(0, tk.END)
        self.entry_capacidad.delete(0, tk.END)

    def abrir_registro_empleados(self):
        RegistroUsuarioVentana(self._ventana, self._usuarios, ["empleado", "administrador"])

    def ver_usuarios(self):
        total = len(self._usuarios)
        messagebox.showinfo("Usuarios," f"hay {total} usuarios registrados en el sistema")


    def verUsuarios(self):
        from tkinter import messagebox
        total = len(self._usuarios)
        messagebox.showwarning("Usuarios", f"Hay {total} usuarios registrados")

    def cerrar(self):
        if hasattr(self, 'marco') and self.marco:
            try:
                self.marco.destroy()

            except Exception:
                pass

        self._cerrarSesion()
