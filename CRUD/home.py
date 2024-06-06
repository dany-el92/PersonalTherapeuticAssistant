import tkinter as tk
from create import create_screen  # Importa la funzione dal file create.py
from delete import delete_screen  # Importa la funzione dal file delete.py

def show_frame(frame):
    frame.tkraise()

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")
    window.resizable(False, False)

# Crea la finestra principale
root = tk.Tk()
root.title("Operazioni CRUD")
center_window(root, 500, 500)

# Creo i frame per le schermate
main_frame = tk.Frame(root)
create_frame = tk.Frame(root)
delete_frame = tk.Frame(root)

for frame in (main_frame, create_frame, delete_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Configura la schermata principale
main_label = tk.Label(main_frame, text="Home Screen")
main_label.pack(pady=20, anchor='center')

create_button = tk.Button(main_frame, text="Create", command=lambda: show_frame(create_frame))
create_button.pack(pady=10)

delete_button = tk.Button(main_frame, text="Delete", command=lambda: show_frame(delete_frame))
delete_button.pack(pady=10)

# Configura la schermata "Crea"
create_screen(create_frame, lambda: show_frame(main_frame))  # Passa la funzione per tornare alla schermata principale

# Configura la schermata "Elimina"
delete_screen(delete_frame, lambda: show_frame(main_frame))  # Passa la funzione per tornare alla schermata principale

# Mostra la schermata principale all'avvio
show_frame(main_frame)

root.mainloop()

