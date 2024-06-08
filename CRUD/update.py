import tkinter as tk
from tkinter import messagebox
from operazioni_db.db_operations import Database
import json
from bson import ObjectId


def json_converter(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def retrieve_data(tag, category):
    db = Database()

    if category == "patterns":
        patterns = db.get_patterns_by_tag(tag)
        print(patterns)
        print("\n")
        print((len(patterns)))
        print("\n")
        return patterns
    else:
        responses = db.get_responses_by_tag(tag)
        print(responses)
        print("\n")
        print((len(responses)))
        print("\n")
        return responses


def update_ui(category, tag_label):
    if category == "patterns":
        tag_label.config(text="Pattern")
    elif category == "responses":
        tag_label.config(text="Response")


def reset_update_screen(tag_entry, result_text, category_var):
    tag_entry.delete(0, tk.END)
    category_var.set("patterns")
    result_text.delete('1.0', tk.END)


def update_screen(frame, show_main_frame):
    frame.configure(bg="#2C3E50")

    label = tk.Label(frame, text="Update Data", font=("Helvetica", 20, "bold"), bg="#2C3E50", fg="white")
    label.pack(pady=20)

    category_label = tk.Label(frame, text="Category", font=("Helvetica", 14), bg="#2C3E50", fg="white")
    category_label.pack(pady=5)

    category_var = tk.StringVar(frame)
    category_var.set("patterns")

    category_options = tk.OptionMenu(frame, category_var, "patterns", "responses")
    category_options.config(font=("Helvetica", 14), bg="white", fg="black")
    category_options.pack(pady=5)

    tag_label = tk.Label(frame, text="Pattern", font=("Helvetica", 14), bg="#2C3E50", fg="white")
    tag_label.pack(pady=5)

    tag_entry = tk.Entry(frame, font=("Helvetica", 14), bg="white", fg="black")
    tag_entry.pack(pady=0, ipady=5, padx=1)

    tag_entry.focus_set()
    tag_entry.icursor(0)

    def category_changed(*args):
        new_category = category_var.get()
        update_ui(new_category, tag_label)

    category_var.trace("w", category_changed)
    update_ui(category_var.get(), tag_label)

    button_options = {
        "font": ("Helvetica", 14),
        "bd": 0,
        "bg": "white",
        "padx": 10,
        "pady": 10,
    }

    button_options_retrieve = {
        "font": ("Helvetica", 14),
        "bd": 0,
        "bg": "white",
        "padx": 0,
        "pady": 0,
    }

    back_button_options = {
        "font": ("Helvetica", 10),
        "bd": 0,
        "bg": "white",
        "padx": 0,
        "pady": 0,
    }

    submit_button = tk.Button(frame, text="Retrieve", **button_options_retrieve,
                              command=lambda: retrieve_and_display(tag_entry.get(), category_var.get(), result_text))
    submit_button.pack(pady=5)

    result_text = tk.Text(frame, height=10, width=55, font=("Helvetica", 12), bg="white", fg="black")
    result_text.pack(pady=5, ipady=5, ipadx=5)

    back_button = tk.Button(frame, text="⬅", **back_button_options,
                            command=lambda: [reset_update_screen(tag_entry, result_text, category_var),
                                             show_main_frame()])
    back_button.place(x=5, y=5)

    update_button = tk.Button(frame, text="Update", **button_options,
                              command=lambda: update(tag_entry.get(), category_var.get(), result_text, tag_entry,
                                                     category_var))
    update_button.pack(pady=10)


def retrieve_and_display(tag, category, result_text):
    if not tag:
        messagebox.showinfo("Error", "Tag field must be filled")
        return

    data = retrieve_data(tag, category)

    if data:
        if isinstance(data, list) and len(data) > 0:
            result_text.delete('1.0', tk.END)
            result_text.insert(tk.END, json.dumps(data, indent=4, default=json_converter))
        else:
            result_text.delete('1.0', tk.END)
            result_text.insert(tk.END, "No data found for this tag")
    else:
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "No data found for this tag")


def update(tag, category, result_text, tag_entry, category_var):
    if not tag:
        messagebox.showinfo("Error", "Tag field must be filled")
        return
    to_update = result_text.get("1.0", "end-1c")
    print(to_update)

    try:
        to_update_list = json.loads(to_update)
        if not isinstance(to_update_list, list):
            raise ValueError("Data is not a list")
    except json.JSONDecodeError as e:
        print(e)
        messagebox.showinfo("Error", f"Invalid data")
        return
    except ValueError as e:
        print(e)
        messagebox.showinfo("Error", f"Invalid data format")
        return

    db = Database()
    success = True
    for document in to_update_list:
        if '_id' not in document:
            messagebox.showinfo("Error", "Document ID is missing")
            success = False
            break
        update_data = {category: document[category]}
        if not db.update_document_by_tag(category, tag, update_data):
            success = False

    if success:
        messagebox.showinfo("Success", "Documents updated successfully!")
        reset_update_screen(tag_entry, result_text, category_var)
    else:
        messagebox.showinfo("Error", "Some documents were not updated")
        reset_update_screen(tag_entry, result_text, category_var)
