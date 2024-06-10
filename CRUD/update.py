import tkinter as tk
from tkinter import messagebox
from operazioni_db.db_operations import Database
import platform

global old_values
old_values = []
global tag_entry
tag_entry = None


def update_screen(frame, show_main_frame):
    if show_main_frame is None or not callable(show_main_frame):
        raise ValueError("show_main_frame must be a valid function")

    frame.configure(bg="#2C3E50")

    label = tk.Label(frame, text="Update Data", font=("Helvetica", 20, "bold"), bg="#2C3E50", fg="#fda836")
    label.pack(pady=20)

    # Crea un canvas all'interno del frame
    canvas = tk.Canvas(frame, bg="#2C3E50", bd=0, highlightthickness=0)
    canvas.pack(side='left', fill='both', expand=True, padx=20, pady=10)

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

    values = {"Update a single element from a document": "3"}

    v_radio = tk.StringVar(inner_content_frame)  # Variabile per memorizzare il valore selezionato
    v_checkbox = []  # Variabile per memorizzare il valore selezionato

    collection_var = tk.StringVar(inner_content_frame)
    collection_var.set("patterns")  # valore predefinito

    # Funzione di callback per aggiornare il contenuto in base alla selezione
    def update_content(*args):
        for widget in content_frame.winfo_children():
            widget.destroy()

        for widget in result_frame.winfo_children():
            widget.destroy()

        selection = v_radio.get()

        if selection == "3":
            # Collezione
            collection_label = tk.Label(content_frame, text="Collection", bg="#2C3E50", fg="#f9c686",
                                        font=("Helvetica", 16))
            collection_label.pack(side='top', pady=(0, 5), padx=(90, 0))

            collection_var.set("patterns")  # valore predefinito

            collection_options = tk.OptionMenu(content_frame, collection_var, "patterns", "responses")
            collection_options.config(width=10, bg="white", fg="black")  # Imposta la larghezza del menu a tendina
            collection_options.pack(side='top', fill='x', pady=(0, 10), padx=(90, 0))

            # Tag
            tag_label = tk.Label(content_frame, text="Tag", bg="#2C3E50", fg="#f9c686", font=("Helvetica", 16),
                                 width=10)
            tag_label.pack(side='top', fill='x', pady=(0, 5), padx=(90, 0))

            global tag_entry
            tag_entry = tk.Entry(content_frame, bg="white", fg="black", width=10)
            tag_entry.pack(side='top', fill='x', pady=(0, 10), padx=(90, 0))
            tag_entry.focus_set()
            tag_entry.icursor(0)

            search_button = tk.Button(content_frame, text="Search",
                                      command=lambda: search_elements(tag_entry.get(), collection_var.get()),
                                      bg="#2C3E50", fg="black", bd=0, highlightthickness=0, activebackground="#2C3E50")
            search_button.pack(side='top', pady=(10, 5))

    v_radio.trace("w", update_content)  # Associa la funzione di callback alla variabile v_radio

    # Funzione di callback per cercare gli elementi da eliminare
    def search_elements(tag, collection_var):
        v_checkbox.clear()
        db = Database()
        global old_values
        old_values = []

        for widget in result_frame.winfo_children():
            widget.destroy()

        elements = []
        try:
            if collection_var == "patterns":
                results = db.get_patterns_by_tag(tag)
                elements = results[0]['patterns']
            else:
                results = db.get_responses_by_tag(tag)
                elements = results[0]['responses']
            success = True
        except Exception as e:
            messagebox.showinfo("Error", f"Tag not inserted!")
            success = False

        if success:
            cb_label = tk.Label(result_frame, text="Modify elements", bg="#2C3E50", fg="#f9c686",
                                font=("Helvetica", 16))
            cb_label.pack(side='top', pady=(0, 5), padx=(90, 0))

            for element in elements:
                old_values.append(element)
                entry_var = tk.StringVar(value=element)
                v_checkbox.append(entry_var)

                entry_frame = tk.Frame(result_frame, bg="#2C3E50")
                entry_frame.pack(side='top', padx=(90, 0), anchor='w')

                entry = tk.Entry(entry_frame, textvariable=entry_var, bg="white", fg="black")
                entry.pack(side='left',pady=0, ipady=5, padx=1)

            add_button = tk.Button(result_frame, text="+", command=lambda: add_new_entry(result_frame, v_checkbox),
                                   bg="#2C3E50", fg="black", bd=0, highlightthickness=0, activebackground="#2C3E50")
            add_button.pack(side='top', padx=(90, 0), anchor='w')

    def add_new_entry(frame, checkbox_list):
        entry_var = tk.StringVar()
        checkbox_list.append(entry_var)

        entry_frame = tk.Frame(frame, bg="#2C3E50")
        entry_frame.pack(side='top', padx=(90, 0), anchor='w')

        entry = tk.Entry(entry_frame, textvariable=entry_var, bg="white", fg="black")
        entry.pack(side='left', fill='x', expand=True)

    for (text, value) in values.items():
        rb = tk.Radiobutton(inner_content_frame, text=text, variable=v_radio, value=value)
        rb.config(bg="#2C3E50", fg="white")
        rb.pack(side='top', ipady=5, padx=(90, 0))

    # Frame per contenere i widget dinamici
    content_frame = tk.Frame(inner_content_frame, bg="#2C3E50")
    content_frame.pack(expand=True, pady=10)

    result_frame = tk.Frame(inner_content_frame, bg="#2C3E50")
    result_frame.pack(expand=True, pady=10)

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
                            command=lambda: [reset_screen(collection_var, tag_entry, result_frame, v_checkbox),
                                             show_main_frame()])
    back_button.place(x=5, y=5)

    # Abilita lo scorrimento del canvas con il touchpad
    if platform.system() == 'Windows':
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int((event.delta / 120) * 2), "units"))
    elif platform.system() == 'Darwin':
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int(event.delta), "units"))

    update_button = tk.Button(frame, text="Update",
                              command=lambda: update_data(collection_var, v_checkbox, result_frame),
                              bg="#2C3E50", fg="black", bd=0, highlightthickness=0, activebackground="#2C3E50")
    update_button.pack(pady=10, side='bottom')
    update_button.place (y=470)


def reset_screen(collection_var, tag_entry, result_frame, v_checkbox):
    # Resetta la selezione della categoria
    collection_var.set("patterns")

    # Cancella il contenuto di tag_entry
    if tag_entry is not None:
        tag_entry.delete(0, tk.END)

    # Cancella tutti i figli di result_frame
    for widget in result_frame.winfo_children():
        widget.destroy()

    # Imposta tutte le checkbox come unchecked
    for checkbox in v_checkbox:
        checkbox.set("")


def update_data(collection_var, v_checkbox, result_frame):
    db = Database()
    global old_values

    if collection_var.get() is None or collection_var.get() == "":
        messagebox.showerror("Error", f"Tag not inserted!")
    else:
        try:
            selected_elements = [var.get() for var in v_checkbox if var.get()]

            # Verifica se ci sono elementi aggiunti rispetto ai vecchi valori
            if len(selected_elements) > len(old_values):
                print("elementi aggiunti")

            # Aggiorna i pattern o le risposte specifici
            if collection_var.get() == "patterns":
                for old_value, new_value in zip(old_values, selected_elements):
                    print(f"old value: {old_value}, new value: {new_value}")
                    db.update_specific_pattern(tag_entry.get(), old_value, new_value)
                # Aggiungi nuovi pattern se ce ne sono
                for new_element in selected_elements[len(old_values):]:
                    if new_element is not None and new_element != "":
                        print(new_element)
                        db.update_specific_pattern(tag_entry.get(), "to_add", new_element)
            else:
                for old_value, new_value in zip(old_values, selected_elements):
                    print(f"old value: {old_value}, new value: {new_value}")
                    db.update_specific_response(tag_entry.get(), old_value, new_value)
                # Aggiungi nuove risposte se ce ne sono
                for new_element in selected_elements[len(old_values):]:
                    if new_element is not None and new_element != "":
                        print(new_element)
                        db.update_specific_response(tag_entry.get(), "to_add", new_element)

            # Operazione completata con successo
            messagebox.showinfo("Success", "Data updated successfully")
            reset_screen(collection_var, tag_entry, result_frame, v_checkbox)
        except Exception as e:
            # Errore durante l'aggiornamento dei dati
            messagebox.showerror("Error", f"An error occurred: {e}")
