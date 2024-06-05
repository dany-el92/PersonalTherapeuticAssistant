from operazioni_db.db_operations import Database
from chatbot.chatbot import ChatbotApp
import tkinter as tk

if __name__ == "__main__":
    db = Database()
    root = tk.Tk()
    app = ChatbotApp(root, db)
    root.mainloop()
