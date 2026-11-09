import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from menuStaff import menuStaffVentana
from menuCliente import menuClienteVentana
from menuAdmin import menuAdminVentana
from registro_usuario import RegistroUsuarioVentana, generar_hash, verificar_contrasena

usuarios = {
    "admin": {
        "nombre": "Admin",
        "contrasena": generar_hash("admin123"),
        "rol": "administrador",
        "estado": "ACTIVA",
    },
    "empleado": {
        "nombre": "Empleado",
        "contrasena": generar_hash("empleado123"),
        "rol": "staff",
        "estado": "ACTIVA",
    },
    "cliente": {
        "nombre": "Cliente",
        "contrasena": generar_hash("cliente123"),
        "rol": "cliente",
        "estado": "ACTIVA",
    },
}

sistema_boletos_db = {}


def iniciar_sesion():
    nombre_usuario = campo_usuario.get().strip().lower()
    contrasena = campo_contrasena.get()

    if nombre_usuario == "" or contrasena == "":
        messagebox.showwarning("Datos requeridos", "Ingrese el usuario y contraseña")
        return

    if nombre_usuario in usuarios and verificar_contrasena(contrasena, usuarios[nombre_usuario]["contrasena"]):
        if usuarios[nombre_usuario]["estado"] != "ACTIVA":
            messagebox.showwarning("Cuenta no disponible", "Su cuenta no está activa.")
            return

        rol_usuario = usuarios[nombre_usuario]["rol"]
        nombre_real = usuarios[nombre_usuario]["nombre"]
        
        messagebox.showinfo("Acceso Autorizado", f"Bienvenido, {nombre_usuario}.\nRol: {rol_usuario}")
        
        # Cargamos el menú correspondiente limpiando la ventana
        cargar_menu(rol_usuario, nombre_real)
    else:
        messagebox.showwarning("Error de acceso", "Usuario o contraseña equivocadas")
        campo_contrasena.delete(0, tk.END)


def cargar_menu(rol_usuario, nombre_real):
    # Destruye absolutamente todo lo que esté en la ventana (elimina el login por completo)
    for widget in ventana.winfo_children():
        widget.destroy()

    # Instancia el menú según el rol pasándole la función de cerrar sesión para volver al login
    if rol_usuario == "staff":
        menuStaffVentana(ventana, usuarios, nombre_real, mostrar_login, sistema_boletos_db)
    elif rol_usuario == "administrador":
        menuAdminVentana(ventana, usuarios, nombre_real, mostrar_login, sistema_boletos_db)
    elif rol_usuario == "cliente":
        menuClienteVentana(ventana, usuarios, nombre_real, mostrar_login)


def mostrar_login():
    # Destruye absolutamente todo lo que esté en la ventana (elimina cualquier menú anterior)
    for widget in ventana.winfo_children():
        widget.destroy()

    # Volvemos a construir el marco de login limpio y ordenado arriba
    global campo_usuario, campo_contrasena, marco_login
    
    marco_login = tk.Frame(ventana)
    marco_login.pack(fill="both", expand=True, padx=20, pady=20)

    
    ruta_logo = Path(__file__).resolve().parent / "Imag" / "logo.png"
    if ruta_logo.exists():
        try:
            global imagen_logo        
            imagen_logo = tk.PhotoImage(file=str(ruta_logo)).subsample(8, 8)
            etiqueta_logo = tk.Label(marco_login, image=imagen_logo)
            etiqueta_logo.pack(pady=10, anchor="center")
        except tk.TclError:
            tk.Label(marco_login, text="No se puede cargar el logo").pack(pady=10)
    else:
        tk.Label(marco_login, text="[logo del proyecto]", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Label(marco_login, text="Inicio de sesion", font=("Arial", 18, "bold")).pack(pady=10)

    tk.Label(marco_login, text="Usuario o correo:").pack(anchor="w")
    campo_usuario = tk.Entry(marco_login)
    campo_usuario.pack(fill="x", pady=5)

    tk.Label(marco_login, text="Contraseña:").pack(anchor="w")
    campo_contrasena = tk.Entry(marco_login, show="*")
    campo_contrasena.pack(fill="x", pady=5)

    tk.Button(marco_login, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=10)
    tk.Label(marco_login, text="¿No tienes cuenta?").pack(pady=(10, 0))
    tk.Button(marco_login, text="Crear cuenta", command=abrir_registro_publico).pack(pady=5)


def precargar_usuario(correo):
    campo_usuario.delete(0, tk.END)
    campo_usuario.insert(0, correo)
    campo_contrasena.focus_set()


def abrir_registro_publico():
    RegistroUsuarioVentana(ventana, usuarios, ["cliente"], al_registrar=precargar_usuario)


# --- Configuración Inicial de la Ventana ---
ventana = tk.Tk()
ventana.title("EntradaSegura")
ventana.geometry("520x820")
ventana.resizable(False, False)

# Arrancamos mostrando el login
mostrar_login()

ventana.mainloop()