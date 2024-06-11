import tkinter as tk
from tkinter import scrolledtext
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
        self.chat_area = None
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
        self.center_window(450, 650)

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
                                     fg="#f9c686", bg="#34495E")
        self.header_label.pack(padx=10, pady=15)

        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Helvetica", 14), bg="white",
                                                   fg=self.text_color, state=tk.DISABLED)
        self.chat_area.pack(padx=15, pady=(15, 0), fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(self.root, bg="#34495E", height=50)
        self.input_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.entry_var = tk.StringVar()
        self.entry_box = tk.Entry(self.input_frame, textvariable=self.entry_var, font=("Helvetica", 14), bg="white",
                                  fg="black", relief="flat")
        self.entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5), pady=10)
        self.entry_box.bind("<Return>", self.send_message)

        self.send_image = Image.open("chatbot/icons/send_icon.png")
        self.send_image = self.send_image.resize((30, 30), Image.LANCZOS)
        self.send_icon = ImageTk.PhotoImage(self.send_image)
        self.send_button = tk.Label(self.input_frame, image=self.send_icon, bg="#34495E")
        self.send_button.pack(side=tk.RIGHT, padx=(5, 10), pady=10)
        self.send_button.bind("<Button-1>", lambda event: self.send_message())

        # Load user and bot avatars
        self.user_avatar_image = Image.open("chatbot/icons/user_icon.png")
        self.user_avatar_image = self.user_avatar_image.resize((30, 30), Image.LANCZOS)
        self.user_avatar = ImageTk.PhotoImage(self.user_avatar_image)

        self.bot_avatar_image = Image.open("chatbot/icons/bot_icon.png")
        self.bot_avatar_image = self.bot_avatar_image.resize((30, 30), Image.LANCZOS)
        self.bot_avatar = ImageTk.PhotoImage(self.bot_avatar_image)

    def send_message(self, event=None):
        user_message = self.entry_var.get().strip()
        if user_message:
            self.display_message("You", user_message, self.user_color, "right")
            self.entry_var.set("")
            self.get_response(user_message)

    def get_response(self, user_message):
        tag = self.db.text_search(user_message, "patterns")
        if tag:
            responses = self.db.get_documents_by_tag("responses", tag)
            if responses:
                response = responses[0].get("responses", ["Sorry, I don't understand."])[0]
                self.display_message("Bot", response, self.bot_color, "left")
            else:
                self.display_message("Bot", "Sorry, I don't understand.", self.bot_color, "left")
        else:
            self.display_message("Bot", "Sorry, I don't understand.", self.bot_color, "left")

    def display_message(self, sender, message, color, align):
        self.chat_area.config(state=tk.NORMAL)
        timestamp = datetime.datetime.now().strftime("%H:%M")

        if align == "right":
            self.chat_area.insert(tk.END, f"\n{timestamp} {sender}: {message}\n", 'right')
            self.chat_area.tag_configure('right', justify='right')
        else:
            self.chat_area.insert(tk.END, f"\n{timestamp} {sender}: {message}\n", 'left')
            self.chat_area.tag_configure('left', justify='left')

        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(False, False)