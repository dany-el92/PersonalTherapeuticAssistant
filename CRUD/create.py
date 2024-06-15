import tkinter as tk
from tkinter import ttk
from operazioni_db.db_operations import Database
from tkinter import messagebox
import platform

def create_screen(frame, show_main_frame):
    frame.configure(bg="#2C3E50")

    label = tk.Label(frame, text="Create Data", font=("Helvetica", 20, "bold"), bg="#2C3E50", fg="#fda836")
    label.pack(pady=20)

    # Crea un canvas all'interno del frame
    canvas = tk.Canvas(frame, bg="#2C3E50", bd=0, highlightthickness=0)
    canvas.pack(side='left', fill='both', expand=True, padx=10, pady=10)

    # Aggiungi una scrollbar al frame
    scrollbar = tk.Scrollbar(frame, command=canvas.yview)
    scrollbar.pack(side='right', fill='y')

    canvas['yscrollcommand'] = scrollbar.set

    # Crea un frame interno al canvas per contenere i widget
    inner_frame = tk.Frame(canvas, bg="#2C3E50")
    canvas.create_window((0, 0), window=inner_frame, anchor='nw')

    # Aggiorna la dimensione del canvas quando il frame interno cambia
    inner_frame.bind('<Configure>', lambda event: canvas.configure(scrollregion=canvas.bbox('all')))

    # Centra gli elementi all'interno del frame
    inner_content_frame = tk.Frame(inner_frame, bg="#2C3E50")
    inner_content_frame.pack(expand=True, pady=10)

    # Imposta altezza del canvas in base al contenuto
    canvas_height = inner_content_frame.winfo_reqheight()
    canvas.config(height=canvas_height)

    # Imposta altezza della scrollbar
    scrollbar.config(command=canvas.yview, orient="vertical")

    # Collezione
    collection_label = tk.Label(inner_content_frame, text="Collection", bg="#2C3E50", fg="#f9c686", font=("Helvetica", 16))
    collection_label.pack(side='top', pady=(0, 5), padx=(90, 0))

    collection_var = tk.StringVar(inner_content_frame)
    collection_var.set("patterns")  # valore predefinito

    collection_options = tk.OptionMenu(inner_content_frame, collection_var, "patterns", "responses")
    collection_options.config(width=10,  bg="white", fg="black")  # Imposta la larghezza del menu a tendina
    collection_options.pack(side='top', fill='x', pady=(0, 10), padx=(90, 0))

    # Tag
    tag_label = tk.Label(inner_content_frame, text="Tag", bg="#2C3E50", fg="#f9c686", font=("Helvetica", 16), width=10)
    tag_label.pack(side='top', fill='x', pady=(0, 5), padx=(90, 0))

    tag_entry = tk.Entry(inner_content_frame, bg="white", fg="black", width=10, insertbackground="black")
    tag_entry.pack(side='top', fill='x', pady=(0, 10), padx=(90, 0))

    # Descrizione
    description_label = tk.Label(inner_content_frame, text="Description", bg="#2C3E50", fg="#f9c686", font=("Helvetica", 16))
    description_label.pack(side='top', pady=(0, 5), padx=(90, 0))

    description_frame = tk.Frame(inner_content_frame, bg="#2C3E50")
    description_frame.pack(side='top', fill='x')

    description_text = tk.Text(description_frame, height=3, width=40, bg="white", fg="black", insertbackground="black")
    description_text.pack(side='top', fill='x', pady=(0, 10), padx=(90, 0))

    # Lista di caselle di testo per la descrizione
    description_boxes = [description_text]

    # Bottone per aggiungere una nuova casella di testo per la descrizione
    add_button = tk.Button(inner_content_frame, text="+", command=lambda: add_description_box(description_frame, description_boxes),
                           bg="#2C3E50", fg="black", bd=0, highlightthickness=0, activebackground="#2C3E50")
    add_button.pack(side='left', pady=(0, 10), padx=(90, 0))

    button_frame = tk.Frame(inner_content_frame, bg="#2C3E50")
    button_frame.pack(side='top', fill='x', pady=20, padx=(90, 0))

    # Pulsanti
    back_button_options = {
        "font": ("Helvetica", 10),
        "bd": 0,
        "bg": "white",
        "fg": "black",
        "padx": 0,
        "pady": 0,
        "highlightthickness": 0,
        "activebackground": "white"
    }

    back_button = tk.Button(frame, text="⬅", **back_button_options,
                            command=lambda: [reset_screen(collection_var, tag_entry, description_boxes),
                            show_main_frame()])
    back_button.place(x=5, y=5)

    submit_button = tk.Button(button_frame, text="Submit", command=lambda: submit_data(collection_var, tag_entry, description_boxes, show_main_frame),
                              bg="#2C3E50", fg="black", bd=0, highlightthickness=0, activebackground="#2C3E50")
    submit_button.pack(side='right', padx=10)

    # Abilita lo scorrimento del canvas con il touchpad
    if platform.system() == 'Windows':
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int((event.delta / 120) * 2), "units"))
    elif platform.system() == 'Darwin':
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int(event.delta), "units"))

def add_description_box(description_frame, description_boxes):
    # Aggiungi una nuova casella di testo per la descrizione
    additional_description_text = tk.Text(description_frame, height=3, width=20, bg="white", fg="black", insertbackground="black")
    additional_description_text.pack(side='top', fill='x', pady=(0, 10), padx=(90, 0))

    # Aggiungi la nuova casella di testo alla lista
    description_boxes.append(additional_description_text)

def submit_data(category_var, tag_entry, description_boxes, show_main_frame):
    db = Database()

    category = category_var.get()
    tag = tag_entry.get()
    descriptions = [box.get("1.0", tk.END).strip() for box in description_boxes]  # Ottieni il testo da ciascuna casella di testo della descrizione

    if not category or not tag or not all(descriptions):
        messagebox.showinfo("Error", "All fields must be filled")
        return

    try:
        if category == "patterns":
            db.insert_pattern(tag, descriptions)
        else:
            db.insert_response(tag, descriptions)

        messagebox.showinfo("Success", "Data inserted successfully")

    except Exception as e:
        messagebox.showinfo("Error", f"An error occurred: {e}")

    # Pulisci lo schermo
    reset_screen(category_var, tag_entry, description_boxes)


def reset_screen(category_var, tag_entry, description_boxes):
    # Pulisci e resetta le variabili
    category_var.set("patterns")
    tag_entry.delete(0, tk.END)

    # Riferimento alla prima casella di testo per la descrizione
    first_description_box = description_boxes[0]
    first_description_box.delete("1.0", tk.END)

    # Pulisci e rimuovi le caselle di testo per la descrizione
    for box in description_boxes[1:]:
        box.destroy()
    description_boxes
