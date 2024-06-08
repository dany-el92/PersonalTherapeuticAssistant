import tkinter as tk
from tkinter import messagebox
from operazioni_db.db_operations import Database


def retrieve_data(tag, category):
    db = Database()

    if category == "patterns":
        if tag == "*":
            patterns = db.get_all_patterns()
        else:
            patterns = db.get_patterns_by_tag(tag)
        print(patterns)
        print("\n")
        print((len(patterns)))
        print("\n")
        return patterns
    else:
        if tag == "*":
            responses = db.get_all_responses()
        else:
            responses = db.get_responses_by_tag(tag)
        print(responses)
        print("\n")
        print((len(responses)))
        print("\n")
        return responses


def update_ui(category, tag_label):
    # Nascondi o mostra i widget in base alla categoria selezionata
    if category == "patterns":
        tag_label.config(text="Pattern")
    elif category == "responses":
        tag_label.config(text="Response")


def reset_retrieve_screen(tag_entry, result_text, category_var):
    tag_entry.delete(0, tk.END)
    category_var.set("patterns")
    result_text.delete('1.0', tk.END)


def retrieve_screen(frame, show_main_frame):
    frame.configure(bg="#2C3E50")

    label = tk.Label(frame, text="Retrieve Data", font=("Helvetica", 20, "bold"), bg="#2C3E50", fg="white")
    label.pack(pady=20)

    # Category
    category_label = tk.Label(frame, text="Category", font=("Helvetica", 14), bg="#2C3E50", fg="white")
    category_label.pack(pady=5)

    category_var = tk.StringVar(frame)
    category_var.set("patterns")  # default value

    category_options = tk.OptionMenu(frame, category_var, "patterns", "responses")
    category_options.config(font=("Helvetica", 14), bg="white", fg="black")
    category_options.pack(pady=5)

    # Tag
    tag_label = tk.Label(frame, text="Pattern", font=("Helvetica", 14), bg="#2C3E50", fg="white")
    tag_label.pack(pady=5)

    tag_entry = tk.Entry(frame, font=("Helvetica", 14), bg="white", fg="black", insertbackground="black")
    tag_entry.pack(pady=0, ipady=5, padx=1)
    tag_entry.focus_set()

    tag_entry.focus_set()
    tag_entry.icursor(0)

    tag_label_star = tk.Label(frame, text="inserisci * per selezionare tutti i tag", font=("Helvetica", 10),
                              bg="#2C3E50", fg="white")
    tag_label_star.pack(pady=15)

    # Result
    result_text = tk.Text(frame, height=10, width=55, font=("Helvetica", 12), bg="white", fg="black")
    result_text.pack(pady=5, ipady=15, ipadx=15)

    # Funzione di callback per aggiornare la UI quando la categoria viene cambiata
    def category_changed(*args):
        # Ottieni la nuova categoria selezionata
        new_category = category_var.get()
        # Aggiorna l'interfaccia utente in base alla nuova categoria
        update_ui(new_category, tag_label)

    # Associa la funzione di callback alla variabile category_var
    category_var.trace("w", category_changed)

    # Aggiorna l'interfaccia utente in base alla categoria corrente
    update_ui(category_var.get(), tag_label)

    # Buttons
    button_options = {
        "font": ("Helvetica", 14),
        "bd": 0,
        "bg": "white",
        "padx": 10,
        "pady": 10,
    }

    # Buttons
    back_button_options = {
        "font": ("Helvetica", 10),
        "bd": 0,
        "bg": "white",
        "padx": 0,
        "pady": 0,
    }

    submit_button = tk.Button(frame, text="Retrieve", **button_options,
                              command=lambda: retrieve_and_display(tag_entry.get(), category_var.get(), result_text))
    submit_button.pack(pady=10)

    back_button = tk.Button(frame, text="⬅", **back_button_options,
                            command=lambda: [reset_retrieve_screen(tag_entry, result_text, category_var),
                                             show_main_frame()])
    back_button.place(x=5, y=5)


def retrieve_and_display(tag, category, result_text):
    if not tag:
        messagebox.showinfo("Error", "Tag field must be filled")
        return

    data = retrieve_data(tag, category)

    if data:
        if isinstance(data, list) and len(data) > 0:
            if category == "responses":
                # Estrai le risposte da ogni dizionario nella lista
                all_responses = [item for response in data for item in response.get('responses', [])]
                print(all_responses)
                print("\n")
                print(len(all_responses))
                result_text.delete('1.0', tk.END)
                result_text.insert(tk.END, "\n".join(all_responses))
            else:
                # Estrai i patterns da ogni dizionario nella lista
                all_patterns = [item for response in data for item in response.get('patterns', [])]
                print(all_patterns)
                print("\n")
                print(len(all_patterns))
                result_text.delete('1.0', tk.END)
                result_text.insert(tk.END, "\n".join(all_patterns))
        else:
            result_text.delete('1.0', tk.END)
            result_text.insert(tk.END, "No data found for this tag")
    else:
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "No data found for this tag")

