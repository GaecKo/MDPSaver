#importing required modules
# import tkinter
# import customtkinter
# from PIL import ImageTk,Image

# customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
# customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green


# app = customtkinter.CTk()  #creating cutstom tkinter window
# app.geometry("800x500")
# app.title('Login')



# def button_function():
#     app.destroy()            # destroy current window and creating new one 
#     w = customtkinter.CTk()  
#     w.geometry("1280x720")
#     w.title('Welcome')
#     l1=customtkinter.CTkLabel(master=w, text="Home Page",font=('Century Gothic',60))
#     l1.place(relx=0.5, rely=0.5,  anchor=tkinter.CENTER)
#     w.mainloop()
    


# img1=ImageTk.PhotoImage(Image.open("pattern.png"))
# l1=customtkinter.CTkLabel(master=app,image=img1)
# l1.pack()

# #creating custom frame
# frame=customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
# frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# l2=customtkinter.CTkLabel(master=frame, text="Log into your Account",font=('Century Gothic',20))
# l2.place(x=50, y=45)

# label1 = customtkinter.CTkLabel(master=frame, text="Gaecko")
# label1.place(x=50, y=110)

# # entry1=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
# # entry1.place(x=50, y=110)

# entry2=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
# entry2.place(x=50, y=165)

# l3=customtkinter.CTkLabel(master=frame, text="Forget password?",font=('Century Gothic',12))
# l3.place(x=155,y=195)

# #Create custom button
# button1 = customtkinter.CTkButton(master=frame, width=220, text="Login", command=button_function, corner_radius=6)
# button1.place(x=50, y=240)

# # You can easily integrate authentication system 

# app.mainloop()

import tkinter as tk

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Create a container for the menu and content frames
        container = tk.Frame(self)
        container.pack(side="left", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create the menu frame
        menu_frame = tk.Frame(container)
        menu_frame.grid(row=0, column=0, sticky="nsew")
        menu_frame.config(bg='gray')
        self.frames = {}
        
        # Add the different menu options
        button1 = tk.Button(menu_frame, text="Option 1", command=lambda: self.show_frame("Option1"))
        button1.pack(side="top", fill="x")
        button2 = tk.Button(menu_frame, text="Option 2", command=lambda: self.show_frame("Option2"))
        button2.pack(side="top", fill="x")
        button3 = tk.Button(menu_frame, text="Option 3", command=lambda: self.show_frame("Option3"))
        button3.pack(side="top", fill="x")
        
        # Create the content frame
        content_frame = tk.Frame(container)
        content_frame.grid(row=0, column=1, sticky="nsew")

        # Add the different frames for each menu option
        self.frames["Option1"] = tk.Frame(content_frame, bg='red')
        self.frames["Option2"] = tk.Frame(content_frame, bg='blue')
        self.frames["Option3"] = tk.Frame(content_frame, bg='green')
        
        for f in self.frames.values():
            f.grid(row=0, column=0, sticky="nsew")
            tk.Label(f, text=f"This is the content for {f}").pack()
        
        self.show_frame("Option1")

    def show_frame(self, page_name):
        """Show the selected frame."""
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
