import hashlib
import hmac
import os
import re
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path


def generar_hash(contrasena):
    """Devuelve 'sal$hash' usando PBKDF2-SHA256 con una sal aleatoria."""
    sal = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", contrasena.encode("utf-8"), sal, 100_000)
    return f"{sal.hex()}${hash_bytes.hex()}"


def verificar_contrasena(contrasena, almacenado):
    """Compara la contraseña escrita contra el 'sal$hash' guardado."""
    try:
        sal_hex, hash_hex = almacenado.split("$")
        sal = bytes.fromhex(sal_hex)
    except ValueError:
        return False
    hash_nuevo = hashlib.pbkdf2_hmac("sha256", contrasena.encode("utf-8"), sal, 100_000)
    return hmac.compare_digest(hash_nuevo.hex(), hash_hex)



PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]{3,100}$")
PATRON_CORREO = re.compile(r"^[\w.+\-]+@[\w\-]+(\.[\w\-]+)+$")


class RegistroUsuarioVentana(tk.Toplevel):
    """Ventana secundaria con el formulario de registro de usuarios (RF1).

    Parámetros:
      padre            -> ventana que la abre (login o menú principal)
      usuarios         -> diccionario compartido donde se guardan los usuarios
      roles_permitidos -> lista de roles que se pueden elegir en el formulario
      al_registrar     -> función opcional que se ejecuta al registrar con éxito
                          (así la ventana padre se entera del nuevo usuario)
    """

    def __init__(self, padre, usuarios, roles_permitidos, al_registrar=None):
        super().__init__(padre)
        self.usuarios = usuarios
        self.al_registrar = al_registrar

        self.title("Registro de usuario")
        self.geometry("360x680")
        self.resizable(False, False)
        self.transient(padre)   # se muestra encima de la ventana padre
        self.grab_set()         # bloquea la ventana padre hasta cerrar esta

        marco = tk.Frame(self)
        marco.pack(fill="both", expand=True, padx=20, pady=15)

        # Logo 
        ruta_logo = Path(__file__).resolve().parent / "Imag" / "logo.png"

        if ruta_logo.exists():
            try:
                self.logo = tk.PhotoImage(file=str(ruta_logo)).subsample(8, 8)
                tk.Label(marco, image=self.logo).pack(pady=5, anchor="center")
            except tk.TclError:
                tk.Label(marco, text="No se puede cargar el logo").pack(pady=5)
        else:
            tk.Label(marco, text="[logo del proyecto]",
                     font=("Arial", 12, "bold")).pack(pady=5)

        tk.Label(marco, text="Registro de usuario",
                 font=("Arial", 16, "bold")).pack(pady=8)

        # ----- Campos del formulario -----
        tk.Label(marco, text="Nombre completo:").pack(anchor="w")
        self.campo_nombre = tk.Entry(marco)
        self.campo_nombre.pack(fill="x", pady=4)

        tk.Label(marco, text="Correo electrónico:").pack(anchor="w")
        self.campo_correo = tk.Entry(marco)
        self.campo_correo.pack(fill="x", pady=4)

        tk.Label(marco, text="Rol:").pack(anchor="w")
        self.campo_rol = ttk.Combobox(marco, values=roles_permitidos, state="readonly")
        self.campo_rol.current(0)
        if len(roles_permitidos) == 1:
            self.campo_rol.config(state="disabled")  # rol fijo, no se puede cambiar
        self.campo_rol.pack(fill="x", pady=4)

        tk.Label(marco, text="Contraseña (mín. 8 caracteres, letras y números):").pack(anchor="w")
        self.campo_contrasena = tk.Entry(marco, show="*")
        self.campo_contrasena.pack(fill="x", pady=4)

        tk.Label(marco, text="Confirmar contraseña:").pack(anchor="w")
        self.campo_confirmar = tk.Entry(marco, show="*")
        self.campo_confirmar.pack(fill="x", pady=4)

        self.var_mostrar = tk.BooleanVar(value=False)
        tk.Checkbutton(marco, text="Mostrar contraseñas", variable=self.var_mostrar,
                       command=self._alternar_contrasena).pack(anchor="w")

        self.var_datos = tk.BooleanVar(value=False)
        tk.Checkbutton(marco,
                       text="Autorizo el tratamiento de mis datos\npersonales (Ley 1581 de 2012)",
                       justify="left", variable=self.var_datos).pack(anchor="w", pady=8)

        # ----- Botones -----
        tk.Button(marco, text="Registrar", command=self.registrar).pack(pady=5)
        tk.Button(marco, text="Cancelar", command=self.destroy).pack()

        self.bind("<Return>", lambda evento: self.registrar())
        self.campo_nombre.focus_set()

    # ----- Métodos -----
    def _alternar_contrasena(self):
        simbolo = "" if self.var_mostrar.get() else "*"
        self.campo_contrasena.config(show=simbolo)
        self.campo_confirmar.config(show=simbolo)

    def _validar(self, nombre, correo, rol, contrasena, confirmar):
        """Devuelve un texto con el error encontrado, o None si todo está bien."""
        if not (nombre and correo and rol and contrasena and confirmar):
            return "Complete todos los campos."
        if not PATRON_NOMBRE.match(nombre):
            return "El nombre solo puede tener letras y espacios (mínimo 3 caracteres)."
        if not PATRON_CORREO.match(correo):
            return "El correo electrónico no tiene un formato válido."
        if correo in self.usuarios:
            return "Ese correo ya está registrado."
        if len(contrasena) < 8:
            return "La contraseña debe tener al menos 8 caracteres."
        if not (re.search(r"[A-Za-z]", contrasena) and re.search(r"\d", contrasena)):
            return "La contraseña debe combinar letras y números."
        if contrasena != confirmar:
            return "Las contraseñas no coinciden."
        if not self.var_datos.get():
            return "Debe autorizar el tratamiento de datos personales."
        return None

    def registrar(self):
        nombre = self.campo_nombre.get().strip()
        correo = self.campo_correo.get().strip().lower()
        rol = self.campo_rol.get()
        contrasena = self.campo_contrasena.get()
        confirmar = self.campo_confirmar.get()

        error = self._validar(nombre, correo, rol, contrasena, confirmar)
        if error:
            messagebox.showwarning("Datos inválidos", error, parent=self)
            return

        # Se guarda el hash, nunca la contraseña real
        self.usuarios[correo] = {
            "nombre": nombre,
            "contrasena": generar_hash(contrasena),
            "rol": rol,
            "estado": "ACTIVA",
        }

        messagebox.showinfo("Registro exitoso",
                            f"Usuario {nombre} registrado como {rol}.", parent=self)

        if self.al_registrar:
            self.al_registrar(correo)   # avisa a la ventana padre
        self.destroy()