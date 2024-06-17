import tkinter as tk
from tkinter import ttk, messagebox
from operazioni_db.db_operations import Database
from tkinter import *
import platform


def delete_screen(frame, show_main_frame):
    frame.configure(bg="#2C3E50")

    label = tk.Label(frame, text="Delete Data", font=("Helvetica", 20, "bold"), bg="#2C3E50", fg="#fda836")
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

    # Opzioni di cancellazione
    options_label = tk.Label(inner_content_frame, text="Deletion options", bg="#2C3E50", fg="#f9c686",
                             font=("Helvetica", 16))
    options_label.pack(side='top', pady=(0, 5), padx=(90, 0))

    values = {"Delete all documents in a collection": "1",
              "Delete a document": "2",
              "Delete a single element from a document": "3"}

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

        if selection == "1":  # Elimina tutti i documenti di una collezione
            # Collezione
            collection_label = tk.Label(content_frame, text="Collection", bg="#2C3E50", fg="#f9c686",
                                        font=("Helvetica", 16))
            collection_label.pack(side='top', pady=(0, 5), padx=(90, 0))

            collection_var = tk.StringVar(content_frame)
            collection_var.set("patterns")  # valore predefinito

            collection_options = tk.OptionMenu(content_frame, collection_var, "patterns", "responses")
            collection_options.config(width=10, bg="white", fg="black")  # Imposta la larghezza del menu a tendina
            collection_options.pack(side='top', fill='x', pady=(0, 10), padx=(90, 0))

            tag_entry = None

        elif selection == "2":  # Elimina un documento
            # Collezione
            collection_label = tk.Label(content_frame, text="Collection", bg="#2C3E50", fg="#f9c686",
                                        font=("Helvetica", 16))
            collection_label.pack(side='top', pady=(0, 5), padx=(90, 0))

            collection_var = tk.StringVar(content_frame)
            collection_var.set("patterns")  # valore predefinito

            collection_options = tk.OptionMenu(content_frame, collection_var, "patterns", "responses")
            collection_options.config(width=10, bg="white", fg="black")  # Imposta la larghezza del menu a tendina
            collection_options.pack(side='top', fill='x', pady=(0, 10), padx=(90, 0))

            # Tag
            tag_label = tk.Label(content_frame, text="Tag", bg="#2C3E50", fg="#f9c686", font=("Helvetica", 16),
                                 width=10)
            tag_label.pack(side='top', fill='x', pady=(0, 5), padx=(90, 0))

            tag_entry = tk.Entry(content_frame, bg="white", fg="black", width=10, insertbackground="black")
            tag_entry.pack(side='top', fill='x', pady=(0, 10), padx=(90, 0))

        elif selection == "3":  # Elimina un singolo elemento da un documento
            # Collezione
            collection_label = tk.Label(content_frame, text="Collection", bg="#2C3E50", fg="#f9c686",
                                        font=("Helvetica", 16))
            collection_label.pack(side='top', pady=(0, 5), padx=(90, 0))

            collection_var = tk.StringVar(content_frame)
            collection_var.set("patterns")  # valore predefinito

            collection_options = tk.OptionMenu(content_frame, collection_var, "patterns", "responses")
            collection_options.config(width=10, bg="white", fg="black")  # Imposta la larghezza del menu a tendina
            collection_options.pack(side='top', fill='x', pady=(0, 10), padx=(90, 0))

            # Tag
            tag_label = tk.Label(content_frame, text="Tag", bg="#2C3E50", fg="#f9c686", font=("Helvetica", 16),
                                 width=10)
            tag_label.pack(side='top', fill='x', pady=(0, 5), padx=(90, 0))

            tag_entry = tk.Entry(content_frame, bg="white", fg="black", width=10, insertbackground="black")
            tag_entry.pack(side='top', fill='x', pady=(0, 10), padx=(90, 0))

            search_button = tk.Button(content_frame, text="Search",
                                      command=lambda: search_elements(tag_entry.get(), collection_var.get()),
                                      bg="#2C3E50", fg="black", bd=0, highlightthickness=0, activebackground="#2C3E50")
            search_button.pack(side='top', pady=(10, 5))

        button_frame = tk.Frame(content_frame, bg="#2C3E50")
        button_frame.pack(side='top', fill='x', padx=(90, 0))

        delete_button = tk.Button(button_frame, text="Delete",
                                  command=lambda: delete_data(v_radio, collection_var, tag_entry, v_checkbox,
                                                              content_frame, result_frame),
                                  bg="#2C3E50", fg="black", bd=0, highlightthickness=0, activebackground="#2C3E50")
        delete_button.pack(side='right')

    v_radio.trace("w", update_content)  # Associa la funzione di callback alla variabile v_radio

    # Funzione di callback per cercare gli elementi da eliminare
    def search_elements(tag, collection_var):
        v_checkbox.clear()
        db = Database()

        for widget in result_frame.winfo_children():
            widget.destroy()

        try:
            if collection_var == "patterns":
                results = db.get_patterns_by_tag(tag)
                elements = results[0]['patterns']
            else:
                results = db.get_responses_by_tag(tag)
                elements = results[0]['responses']
            success = True
        except Exception as e:
            error = e
            success = False

        if success:
            cb_label = tk.Label(result_frame, text="Select elements to delete", bg="#2C3E50", fg="#f9c686",
                                font=("Helvetica", 16))
            cb_label.pack(side='top', pady=(0, 5), padx=(90, 0))

            for element in elements:
                check_var = tk.StringVar()
                v_checkbox.append(check_var)

                cb = tk.Checkbutton(result_frame, text=element, variable=check_var, onvalue=element,
                                    offvalue="", bg="#2C3E50", fg="white", selectcolor="#2C3E50")
                cb.pack(side='top', padx=(90, 0), anchor='w')
        else:
            messagebox.showinfo("Error", f"Tag not inserted or tag not present in the collection selected!")

    for (text, value) in values.items():
        rb = Radiobutton(inner_content_frame, text=text, variable=v_radio, value=value)
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
                            command=lambda: [reset_screen(v_radio, collection_var, content_frame, result_frame),
                                             show_main_frame()])
    back_button.place(x=5, y=5)

    # Abilita lo scorrimento del canvas con il touchpad
    if platform.system() == 'Windows':
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int((event.delta / 120) * 2), "units"))
    elif platform.system() == 'Darwin':
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int(event.delta), "units"))


def reset_screen(v_radio, category_var, content_frame, result_frame):
    # Resetta la selezione del RadioButton
    v_radio.set(None)

    # Resetta la selezione della categoria
    category_var.set("patterns")

    # Rimuove tutti i widget dai frame di contenuto e risultato
    for frame in (content_frame, result_frame):
        for widget in frame.winfo_children():
            widget.destroy()


def delete_data(v_radio, collection_var, tag_entry, v_checkbox, content_frame, result_frame):
    db = Database()

    # Verifica che tutti i campi siano compilati
    if v_radio.get() == "2" and not tag_entry.get():
        messagebox.showinfo("Error", "Please fill in all fields")
        return

    if v_radio.get() == "3" and (not tag_entry.get() or not any(var.get() for var in v_checkbox)):
        messagebox.showinfo("Error", "Please fill in all fields and select at least one element")
        return

    success = False

    if v_radio.get() == "1":
        try:
            db.delete_all_documents(collection_var.get())
            success = True
        except Exception as e:
            error = e
            success = False

    elif v_radio.get() == "2":
        try:
            db.delete_documents_by_tag(collection_var.get(), tag_entry.get())
            success = True
        except Exception as e:
            error = e
            success = False

    elif v_radio.get() == "3":
        try:
            selected_elements = [var.get() for var in v_checkbox if var.get()]

            if collection_var.get() == "patterns":
                db.delete_specific_patterns(tag_entry.get(), selected_elements)
            else:
                db.delete_specific_responses(tag_entry.get(), selected_elements)
            success = True
        except Exception as e:
            error = e
            success = False

    if success:
        messagebox.showinfo("Success", "Data deleted successfully")
        reset_screen(v_radio, collection_var, content_frame, result_frame)
    else:
        messagebox.showinfo("Error", f"Tag not inserted or tag not present in the collection selected!")
