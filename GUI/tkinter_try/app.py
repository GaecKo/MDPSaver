import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import ImageTk, Image



ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

class Login:
    def __init__(self, master: ctk.CTk) -> None:
        self.master = master
        self.set_attributes()
        self.components()

    def set_attributes(self):
        self.master.geometry("400x500")
        self.master.resizable(False, False)
        self.master.wm_title("MDPSaver Login") 
        self.tr = None
    
    def manage_mode(self):
        """
        Function that changes light mode 
        """
        if self.tr == None:
            self.tr = ctk.AppearanceModeTracker()
        if self.tr.get_mode() == 0:
            ctk.set_appearance_mode("dark")
            self.ldb.configure(text="Light")
        else:
            ctk.set_appearance_mode("light")
            self.ldb.configure(text="Dark")

    def components(self):

        # Dark / Light mode part
        self.mode = ctk.CTkImage(Image.open("moon.png").resize((20,20), Image.LANCZOS), Image.open("sun.png").resize((20,20), Image.LANCZOS))
        self.ldb = ctk.CTkButton(master=self.master, image=self.mode, text="Light", 
                                width=30, height=20, compound="left", fg_color='white', 
                                text_color='black', hover_color='#AFAFAF', command=self.manage_mode) # onclick, will start manage_mode function 
        self.ldb.place(relx=0.83, rely=0.05, anchor='center')

        # Main Title 
        self.l1 = ctk.CTkLabel(master=self.master, 
                    text="MDPSaver", font=("Lucida Console", 26))
        self.l1.place(relx=0.5, rely=0.05, anchor='center')

        # Child Frame for login form
        self.f1 = ctk.CTkFrame(master=self.master, 
                    width=300, height=400)
        self.f1.place(relx=0.5, rely=0.5, anchor='center')

        # User Logo
        self.user = ImageTk.PhotoImage(Image.open("user2.png").resize((100, 100), Image.LANCZOS))
        self.l2 = ctk.CTkLabel(master=self.f1, image=self.user, width=100, height=100, text="")
        self.l2.place(relx=0.5, rely=0.23, anchor='center')
        # Username 
        self.l3 = ctk.CTkLabel(master=self.f1, width=100, height=20, text="GaecKo", font=("Lucida Console", 20), text_color="red")
        self.l3.place(relx=0.5, rely=0.48, anchor='center')

        
        # Password entry 
        self.e1 = ctk.CTkEntry(master=self.f1, width=220, placeholder_text='Password', show="*")
        self.e1.place(relx=0.5, rely=0.65, anchor='center')
        self.e1.bind("<Return>", self.alert_end)

        # Login button 
        self.b1 = ctk.CTkButton(master=self.f1, 
                    width=220, text="Login", corner_radius=6)
        self.b1.place(relx=0.5, rely=0.8, anchor='center')

    def alert_end(self, event):
        print(f"User has logged in (event : {event})")

    def start(self):
        self.master.mainloop() 
    

        


if __name__ == "__main__":
    login = ctk.CTk()  # create CTk window like you do with the Tk window
    gui = Login(login)
    gui.start()


