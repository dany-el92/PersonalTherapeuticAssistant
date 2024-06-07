import tkinter as tk


def update_screen(frame, show_main_frame):
    label = tk.Label(frame, text="Welcome to the update screen")
    label.pack(pady=20, anchor='center')

    entry = tk.Entry(frame)
    entry.pack(pady=10, anchor='center')

    submit_button = tk.Button(frame, text="Update", command=lambda: print("Modifica in corso..."))
    submit_button.pack(pady=10, anchor='center')

    back_button = tk.Button(frame, text="Return to the home screen", command=show_main_frame)
    back_button.pack(pady=10, anchor='center')
