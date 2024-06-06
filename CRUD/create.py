import tkinter as tk
from operazioni_db.db_operations import Database
from tkinter import messagebox

def create_screen(frame, show_main_frame):
    # Configuro il frame per espandersi
    frame.grid_rowconfigure(0, weight=3)
    frame.grid_columnconfigure(0, weight=3)

    # Creo un canvas all'interno del frame
    canvas = tk.Canvas(frame)
    canvas.grid(row=0, column=0, sticky='nsew')

    scrollbar = tk.Scrollbar(frame, command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')

    canvas['yscrollcommand'] = scrollbar.set

    # Creo un frame all'interno del canvas per contenere i widget
    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor='nw')

    # Aggiorno la dimensione del canvas quando il frame interno cambia
    inner_frame.bind('<Configure>', lambda event: canvas.configure(scrollregion=canvas.bbox('all')))

    # Configuro il frame interno per espandersi
    inner_frame.grid_rowconfigure(0, weight=1)
    inner_frame.grid_columnconfigure(0, weight=1)

    # Category
    category_label = tk.Label(inner_frame, text="Category")
    category_label.grid(row=0, column=0, sticky='w')

    category_var = tk.StringVar(inner_frame)
    category_var.set("patterns")  # default value

    category_options = tk.OptionMenu(inner_frame, category_var, "patterns", "responses")
    category_options.grid(row=0, column=1, sticky='ew')

    # Tag
    tag_label = tk.Label(inner_frame, text="Tag")
    tag_label.grid(row=1, column=0, sticky='w')

    tag_entry = tk.Entry(inner_frame)
    tag_entry.grid(row=1, column=1, sticky='ew')

    # Description
    description_label = tk.Label(inner_frame, text="Description")
    description_label.grid(row=2, column=0, sticky='nw')

    description_text = tk.Text(inner_frame, height=3, width=30)
    description_text.grid(row=2, column=1, sticky='ew')

    # Lista di caselle di testo per la descrizione
    description_boxes = [description_text]

    # Bottone per aggiungere una nuova casella di testo per la descrizione
    add_button = tk.Button(inner_frame, text="+", command=lambda: add_description_box(inner_frame, description_boxes))
    add_button.grid(row=3, column=1, sticky='ew')

    # Variabile per tenere traccia del numero di caselle di testo per la descrizione
    inner_frame.description_box_count = 1

    button_frame = tk.Frame(inner_frame)
    button_frame.grid(row=1000, column=0, columnspan=2, sticky='ew')

    back_button = tk.Button(button_frame, text="Return to the home screen", command=show_main_frame)
    back_button.pack(side='bottom', anchor='center')

    submit_button = tk.Button(button_frame, text="Submit", command=lambda: submit_data(category_var, tag_entry, description_boxes, show_main_frame, inner_frame))
    submit_button.pack(side='bottom', anchor='center')

def add_description_box(frame, description_boxes):
    # Incremento il contatore
    frame.description_box_count += 1

    # Aggiungo una nuova casella di testo per la descrizione
    additional_description_text = tk.Text(frame, height=3, width=30)
    additional_description_text.grid(row=2 + frame.description_box_count, column=1, sticky='ew')

    # Aggiungo la nuova casella di testo alla lista
    description_boxes.append(additional_description_text)

def submit_data(category_var, tag_entry, description_boxes, show_main_frame, inner_frame):
    db = Database()

    category = category_var.get()
    tag = tag_entry.get()
    descriptions = [box.get("1.0", tk.END).strip() for box in description_boxes]  # Get text from each description box
    # print(category, tag, descriptions)

    if not category or not tag or not all(descriptions):
        messagebox.showinfo("Error", "All fields must be filled")
        return

    if category == "patterns":
        db.insert_pattern(tag, descriptions)
    else:
        db.insert_response(tag, descriptions)

    # Pulisco la schermata
    reset_screen(category_var, tag_entry, description_boxes, inner_frame)

    # Torno alla schermata principale
    show_main_frame()

def reset_screen(category_var, tag_entry, description_boxes, inner_frame):
    # Pulizia e reset delle variabili
    category_var.set("patterns")
    tag_entry.delete(0, tk.END)

    # Riferimento alla prima casella di testo per la descrizione
    first_description_box = description_boxes[0]

    # Pulizia e rimozione delle caselle di testo per la descrizione
    for box in description_boxes[1:]:
        box.destroy()
    description_boxes.clear()

    # Pulizia della prima casella di testo per la descrizione
    first_description_box.delete("1.0", tk.END)
    description_boxes.append(first_description_box)

    # Reset conteggio caselle di testo per la descrizione
    inner_frame.description_box_count = 1

