import customtkinter as ctk
import tkinter as tk
from tkinter import ttk 
from page_view import AccessPassword, AddPassword, HomePage
from PIL import Image, ImageTk


class SettingsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # key: Functionnality itself
        # value: Page object (ctk.CTkFrame)
        self.functionnalities = {}

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.create_frame_treeview().grid(row=0, column=0, sticky="wns")

        self.create_frame_page().grid(row=0, column=1)

        self.load_pages()

    def load_pages(self):
        self.add_page(setting_name="Access Password", page=AccessPassword)

        self.add_page(setting_name="Add Password", page=AddPassword)

        self.add_page(setting_name="Home Page", page=HomePage)

        self.pack(fill=tk.BOTH, expand=True)

        self.show_page("Home Page")

    def create_frame_page(self) -> ctk.CTkFrame:
        self.frame_page = ctk.CTkFrame(self)
        return self.frame_page

    def create_frame_treeview(self) -> ctk.CTkFrame:
        self.frame_treeview = ctk.CTkFrame(self)

        self.treeview_settings = SettingsTreeview(self.frame_treeview)
        self.treeview_settings.bind("<<TreeviewSelect>>", self.on_treeview_selection_changed)
        self.treeview_settings.pack(fill=tk.BOTH, expand=True)

        return self.frame_treeview
    
    def on_treeview_selection_changed(self, event):
        selected_item = self.treeview_settings.focus()

        setting_name = self.treeview_settings.item(selected_item).get("text")
        self.show_page(setting_name)


    def show_page(self, setting_name:str):
        for page_name in self.functionnalities.keys():
            self.functionnalities[page_name].pack_forget()
        self.functionnalities[setting_name].pack(fill=tk.BOTH, expand=True)
    
    def add_page(self, setting_name: str, page):
        
        self.functionnalities[setting_name] = page(self.frame_page)
        self.treeview_settings.add_setting(section_text=setting_name)


class SettingsTreeview(ttk.Treeview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.heading("#0", text="MDPSaver Functions")
    

    def add_setting(self, section_text: str):
        self.insert(parent="", index=tk.END, text=section_text)

if __name__ == "__main__":
    root = ctk.CTk()

    root.geometry("640x480")


    settings = SettingsView(root)
    

    root.mainloop()