import tkinter as tk
from tkinter import messagebox

class menuStaffVentana:
    def __init__(self, ventanaPrincipal, usuarios, nombreUsuarios, cerrarSesion, boletos_db = None):
        self._vetanaPrincipal = ventanaPrincipal
        self._usuarios = usuarios
        self._nombreUsuarios = nombreUsuarios
        self._cerrarSesion = cerrarSesion

        self.boletos_db = boletos_db if boletos_db is not None else {}

        self.marco = tk.Frame(self._vetanaPrincipal)
        self.marco.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(self.marco, text="Panel de empleado", font=("Arial", 17, "bold")).pack(pady=10)
        tk.Label(self.marco, text=f"Bienvenido, {self._nombreUsuarios}", font=("Arial", 12)).pack(pady=4)


        tk.Label(self.marco, text="Ingrese el codigo del boleto", font=("Arial", 12)).pack(pady=4)
        self.entry_codigo = tk.Entry(self.marco, font=("Arial", 14), justify="center")
        self.entry_codigo.pack(pady=5, ipadx=10, ipady=5)
        self.entry_codigo.focus()

        tk.Button(self.marco, text="Validar Acceso", font=("Arial", 11, "bold"), command=self.validar_boleto).pack(pady=10, ipadx=10, ipady=5)
        self.lbl_resultados = tk.Label(self.marco, text="Esperando Escaneo....", font=("Arial", 12, "bold"))
        self.lbl_resultados.pack(pady=10)


        tk.Button(self.marco, text="Cerrar Sesion", command=self._cerrarSesion).pack(pady=20)

    def validar_boleto(self):
        codigo = self.entry_codigo.get().strip()

        if not codigo:
            messagebox.showwarning("No puede ingresar este campo vacio")
            return

        if codigo in self.boletos_db:
            if self.boletos_db[codigo] == True:
                self.lbl_resultados.config(text="Acceso denegado, este boleto ya fue utilizado")
            else:
                self.boletos_db[codigo] = True
                self.lbl_resultados.config(text="Acceso permitido")
        else:
            self.lbl_resultados.config(text="ESTE BOLETO NO ESTA EN EL SISTEMA")

        self.entry_codigo.delete(0, tk.END)
        self.entry_codigo.focus()    





    

    def cerrar(self):
        self.marco.destroy()
        self._cerrarSesion()
        