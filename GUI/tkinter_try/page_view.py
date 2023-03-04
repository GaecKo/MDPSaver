import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk


class Page(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        

class HomePage(Page):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_frame_content().pack(fill=tk.BOTH, expand=True)
    
    def create_frame_content(self) -> ctk.CTkFrame:

        self.frame_content = ctk.CTkFrame(self)

        title = ctk.CTkLabel(master=self.frame_content, width=100, height=20, text="👋 Welcome to MDPSaver!", font=("Cascadio Mono", 24), text_color="red")
        title.place(relx=0.1, rely=0.5, anchor='center')


        self.user = ImageTk.PhotoImage(Image.open("MDPSaver.png"))
        self.l2 = ctk.CTkLabel(master=self.frame_content, image=self.user, text="")
        self.l2.place(relx=0.3, rely=0.5, anchor='center')

        return self.frame_content


class AccessPassword(Page):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_frame_content().pack(fill=tk.BOTH, expand=True)
    
    def create_frame_content(self) -> ctk.CTkFrame:

        self.frame_content = ctk.CTkFrame(self)

        lbl_title = ctk.CTkLabel(self.frame_content, text="Access Password Page")
        lbl_title.pack()

        return self.frame_content

class AddPassword(Page):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_frame_content().pack(fill=tk.BOTH, expand=True)
    
    def create_frame_content(self) -> ctk.CTkFrame:

        self.frame_content = ctk.CTkFrame(self)

        lbl_title = ctk.CTkLabel(self.frame_content, text="Add Password Page")
        lbl_title.pack()

        return self.frame_content