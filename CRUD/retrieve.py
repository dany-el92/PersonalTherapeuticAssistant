import tkinter as tk


def retrieve_screen(frame, show_main_frame):
    label = tk.Label(frame, text="Welcome to the retrieve screen")
    label.pack(pady=20, anchor='center')

    entry = tk.Entry(frame)
    entry.pack(pady=10, anchor='center')

    submit_button = tk.Button(frame, text="Retrieve", command=lambda: print("Ricerca in corso..."))
    submit_button.pack(pady=10, anchor='center')

    back_button = tk.Button(frame, text="Return to the home screen", command=show_main_frame)
    back_button.pack(pady=10, anchor='center')
