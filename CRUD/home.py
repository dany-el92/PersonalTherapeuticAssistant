import tkinter as tk
from tkinter import font
from create import create_screen  # Importa la funzione dal file create.py
from delete import delete_screen  # Importa la funzione dal file delete.py
from retrieve import retrieve_screen
from update import update_screen


def show_frame(frame_):
    frame_.tkraise()


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.resizable(False, False)


#########################################################################

# Crea la finestra principale
root = tk.Tk()
root.title("CRUD Operations")
center_window(root, 500, 500)

header_font = font.Font(family="Helvetica", size=24, weight="bold")

# Creo i frame per le schermate
main_frame = tk.Frame(root, bg="#2C3E50")
create_frame = tk.Frame(root)
delete_frame = tk.Frame(root)
retrieve_frame = tk.Frame(root)
update_frame = tk.Frame(root)

for frame in (main_frame, create_frame, delete_frame, retrieve_frame, update_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Configura la schermata principale
main_label = tk.Label(main_frame, text="CRUD Operations", font=header_font, bg="#2C3E50", fg ="#fda836")
main_label.pack(padx=20, pady=50, anchor='s')

button_frame = tk.Frame(main_frame, bg="#2C3E50")
button_frame.pack(pady=20, padx=10)

# Buttons
button_options = {
    "font": ("Helvetica", 14),
    "bd": 0,
    "bg": "white",
    "padx": 40,
    "pady": 20,
}

create_button = tk.Button(button_frame, text="Create", command=lambda: show_frame(create_frame), **button_options)
create_button.grid(row=0, column=0, padx=40, pady=50)

delete_button = tk.Button(button_frame, text="Delete", command=lambda: show_frame(delete_frame), **button_options)
delete_button.grid(row=0, column=1, padx=40, pady=50)

retrieve_button = tk.Button(button_frame, text="Retrieve", command=lambda: show_frame(retrieve_frame), **button_options)
retrieve_button.grid(row=1, column=0, padx=40, pady=50)

update_button = tk.Button(button_frame, text="Update", command=lambda: show_frame(update_frame), **button_options)
update_button.grid(row=1, column=1, padx=40, pady=50)

# Configura le altre schermate
create_screen(create_frame, lambda: show_frame(main_frame))
delete_screen(delete_frame, lambda: show_frame(main_frame))
retrieve_screen(retrieve_frame, lambda: show_frame(main_frame))
update_screen(update_frame, lambda: show_frame(main_frame))

# Mostra la schermata principale all'avvio
show_frame(main_frame)

root.mainloop()
