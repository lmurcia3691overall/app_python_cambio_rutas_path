import os  # Módulo para interactuar con el sistema operativo (no se usa mucho en este código)
import tkinter as tk  # Importa tkinter para crear interfaces gráficas
from tkinter import ttk, messagebox  # Importa ttk para estilos de tkinter y messagebox para cuadros de diálogo
import winreg  # Módulo para manipular el registro de Windows

# Lista de rutas de PHP disponibles
php_paths = [
    "C:\\laragon\\bin\\php\\php-8.1.10-Win32-vs16-x64",
    "C:\\laragon\\bin\\php\\php-7.3.28-Win32-VC15-x64",
    "C:\\laragon\\bin\\php\\php-7.4.9-Win32-vc15-x64",
    "C:\\laragon\\bin\\php\\php-test-pack-8.3.9"
]

# Función que actualiza la variable PATH en el registro de Windows
def update_path(selected_path, scope):
    # Define la clave del registro y el nivel de acceso según el ámbito (usuario o sistema)
    if scope == "usuario":
        reg_key = r"Environment"  # Clave de registro para variables de usuario
        access = winreg.HKEY_CURRENT_USER  # Acceso al registro de usuario
    else:
        reg_key = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"  # Clave de registro para variables del sistema
        access = winreg.HKEY_LOCAL_MACHINE  # Acceso al registro de sistema

    try:
        # Abre la clave del registro para lectura y escritura
        with winreg.OpenKey(access, reg_key, 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
            # Obtiene el valor actual de la variable PATH
            current_path, _ = winreg.QueryValueEx(key, "Path")

            # Elimina cualquier ruta de PHP previamente configurada en PATH
            new_path = ';'.join([p for p in current_path.split(';') if not p.startswith("C:\\laragon\\bin\\php")])

            # Agrega la nueva ruta PHP seleccionada al inicio del PATH
            new_path = selected_path + ";" + new_path

            # Actualiza el PATH en el registro
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)

        # Muestra un cuadro de diálogo indicando éxito en la operación
        messagebox.showinfo("Éxito", f"La ruta de PHP ha sido cambiada a:\n{selected_path}\n(en {scope})")
    except PermissionError:
        # Si no se tienen permisos de administrador, muestra un mensaje de error
        messagebox.showerror("Error", "Se requieren permisos de administrador para cambiar el PATH del sistema.")

# Función que se llama cuando el usuario hace clic en "Aplicar cambio"
def on_apply():
    # Obtiene la ruta de PHP seleccionada del combobox
    selected_path = php_var.get()
    # Obtiene el ámbito seleccionado (usuario o sistema) de los botones de opción
    scope = scope_var.get()
    # Si ambas selecciones son válidas, llama a update_path para aplicar el cambio
    if selected_path and scope:
        update_path(selected_path, scope)

# Configuración de la ventana principal de la aplicación
root = tk.Tk()  # Crea una instancia de la ventana principal
root.title("Cambiar Ruta de PHP en PATH")  # Título de la ventana
root.geometry("500x300")  # Tamaño de la ventana principal

# Etiqueta para el combobox que permite seleccionar la ruta de PHP
label = tk.Label(root, text="Seleccione la ruta de PHP:", font=("Arial", 12))
label.pack(pady=10)  # Agrega la etiqueta a la ventana con un margen vertical de 10 píxeles

# Variable para almacenar la selección de la ruta PHP en el combobox
php_var = tk.StringVar()
php_var.set(php_paths[0])  # Selección inicial del combobox (primer elemento de php_paths)

# Menú desplegable (Combobox) con las rutas de PHP
dropdown = ttk.Combobox(root, textvariable=php_var, values=php_paths, state="readonly", width=50, font=("Arial", 10))
dropdown.pack(pady=10)  # Agrega el combobox a la ventana con un margen vertical de 10 píxeles

# Variable para almacenar la selección del ámbito (usuario o sistema)
scope_var = tk.StringVar()
scope_var.set("usuario")  # Selección inicial del ámbito (usuario)

# Etiqueta para los botones de opción que permiten seleccionar el ámbito
scope_label = tk.Label(root, text="Aplicar cambio a:", font=("Arial", 12))
scope_label.pack(pady=5)  # Agrega la etiqueta con un margen vertical de 5 píxeles

# Opciones para el ámbito (usuario o sistema), como botones de opción (Radiobutton)
scope_options = [("Variables de usuario", "usuario"), ("Variables del sistema", "sistema")]

# Bucle que crea y agrega cada botón de opción para seleccionar el ámbito
for text, value in scope_options:
    radio = tk.Radiobutton(root, text=text, variable=scope_var, value=value, font=("Arial", 10))
    radio.pack(anchor="w")  # Alinea cada botón de opción a la izquierda

# Botón para aplicar el cambio en el PATH
apply_button = tk.Button(root, text="Aplicar cambio", command=on_apply, font=("Arial", 12))
apply_button.pack(pady=20)  # Agrega el botón con un margen vertical de 20 píxeles

# Inicia el bucle principal de la aplicación, permitiendo que se ejecute y sea interactiva
root.mainloop()
