import tkinter as tk

class menuClienteVentana:
    def __init__ (self, ventaPrincipal, usuarios, nombreUsuarios, cerrarSesion):
        self._ventanaPrincipal = ventaPrincipal
        self._usuarios = usuarios
        self._nombreUsuarios = nombreUsuarios
        self.cerrarSesion = cerrarSesion

        self.marco = tk.Frame(self._ventanaPrincipal)
        self.marco.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(self.marco, text="Mi cuenta", font=("Arial", 17, "bold")).pack(pady=10)
        tk.Label(self.marco, text=f"Bienvenido {self._nombreUsuarios}", font=("Arial", 12, "bold")).pack(pady=4)
        