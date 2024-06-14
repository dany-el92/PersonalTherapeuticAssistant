import tkinter as tk
from PIL import Image, ImageTk
import datetime


class ChatbotApp:
    def __init__(self, root, db):
        self.send_button = None
        self.send_icon = None
        self.send_image = None
        self.entry_box = None
        self.entry_var = None
        self.input_frame = None
        self.chat_area_frame = None
        self.canvas = None
        self.scrollbar = None
        self.scrollable_frame = None
        self.header_label = None
        self.header_frame = None
        self.text_color = None
        self.user_color = None
        self.bot_color = None
        self.bg_color = None
        self.user_avatar_image = None
        self.user_avatar = None
        self.bot_avatar_image = None
        self.bot_avatar = None
        self.root = root
        self.db = db

        self.setup_gui()
        self.center_window(350, 550)

    def setup_gui(self):
        self.root.title("Chatbot")
        self.root.geometry("450x650")
        self.root.resizable(False, False)

        self.bg_color = "#2C3E50"
        self.bot_color = "#c4d1de"
        self.user_color = "#f6f8fa"
        self.text_color = "#2C3E50"
        self.root.config(bg=self.bg_color)

        self.header_frame = tk.Frame(self.root, bg="#34495E", height=60)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)
        self.header_label = tk.Label(self.header_frame, text="SupportBot", font=("Helvetica", 18, "bold"),
                                     fg="#fda836", bg="#34495E")
        self.header_label.pack(padx=10, pady=15)

        self.chat_area_frame = tk.Frame(self.root, bg="white")
        self.chat_area_frame.pack(padx=15, pady=(15, 0), ipadx=5, ipady=5, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.chat_area_frame, bg="white", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.chat_area_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.input_frame = tk.Frame(self.root, bg="#34495E", height=50)
        self.input_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.entry_var = tk.StringVar()
        self.entry_box = tk.Entry(self.input_frame, textvariable=self.entry_var, font=("Helvetica", 14), bg="white",
                                  fg="black", relief="flat", insertbackground="black")
        self.entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5), pady=10)
        self.entry_box.bind("<Return>", self.send_message)

        self.send_image = Image.open("icons/send_icon.png")
        self.send_image = self.send_image.resize((30, 30), Image.LANCZOS)
        self.send_icon = ImageTk.PhotoImage(self.send_image)
        self.send_button = tk.Label(self.input_frame, image=self.send_icon, bg="#34495E")
        self.send_button.pack(side=tk.RIGHT, padx=(5, 10), pady=10)
        self.send_button.bind("<Button-1>", lambda event: self.send_message())

        # Load user and bot avatars
        self.user_avatar_image = Image.open("icons/user_icon.png")
        self.user_avatar_image = self.user_avatar_image.resize((30, 30), Image.LANCZOS)
        self.user_avatar = ImageTk.PhotoImage(self.user_avatar_image)

        self.bot_avatar_image = Image.open("icons/bot_icon.png")
        self.bot_avatar_image = self.bot_avatar_image.resize((30, 30), Image.LANCZOS)
        self.bot_avatar = ImageTk.PhotoImage(self.bot_avatar_image)

    def send_message(self, event=None):
        user_message = self.entry_var.get().strip()
        if user_message:
            self.display_message("You", user_message, self.user_color, "right", self.user_avatar)
            self.entry_var.set("")
            self.get_response(user_message)

    def get_response(self, user_message):
        tag = self.db.text_search(user_message, "patterns")
        if tag:
            responses = self.db.get_documents_by_tag("responses", tag)
            if responses:
                response = responses[0].get("responses", ["Sorry, I don't understand."])[0]
                self.display_message("Bot", response, self.bot_color, "left", self.bot_avatar)
            else:
                self.display_message("Bot", "Sorry, I don't understand.", self.bot_color, "left", self.bot_avatar)
        else:
            self.display_message("Bot", "Sorry, I don't understand.", self.bot_color, "left", self.bot_avatar)

    def display_message(self, sender, message, color, align, icon):
        timestamp = datetime.datetime.now().strftime("%H:%M")

        message_frame = tk.Frame(self.scrollable_frame, bg="white")
        if align == "left":
            message_frame.pack(pady=5, padx=10, anchor="w")
        else:
            message_frame.pack(pady=5, padx=10, anchor="e")

        if align == "right":
            avatar_label = tk.Label(message_frame, image=icon, bg="white")
            avatar_label.pack(side="right", anchor="e")
            message_label = tk.Label(message_frame, text=message, bg=color, fg=self.text_color, font=("Helvetica", 12),
                                     wraplength=200, justify='right')
            message_label.pack(side="right", padx=5, anchor="e")
            timestamp_label = tk.Label(message_frame, text=timestamp, font=("Helvetica", 8), bg="white",
                                       fg=self.text_color)
            timestamp_label.pack(side="right", padx=5, anchor="e")
        else:
            avatar_label = tk.Label(message_frame, image=icon, bg="white")
            avatar_label.pack(side=tk.LEFT, anchor="w")
            message_label = tk.Label(message_frame, text=message, bg=color, fg=self.text_color, font=("Helvetica", 12),
                                     wraplength=200, justify='left')
            message_label.pack(side=tk.LEFT, padx=(5, 5), anchor="w")
            timestamp_label = tk.Label(message_frame, text=timestamp, font=("Helvetica", 8), bg="white",
                                       fg=self.text_color)
            timestamp_label.pack(side=tk.LEFT, padx=(5, 5), anchor="w")

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(False, False)
