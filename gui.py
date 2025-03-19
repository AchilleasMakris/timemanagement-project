import customtkinter
from tkinter import *

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1000x600")
app.title("Time Management System")

# Function to clear the window for new frames
def clear_window():
    for widget in app.winfo_children():
        widget.destroy()



frame = customtkinter.CTkFrame(master=app,
                               width=350,
                               height=250,
                               bg_color="black",
                               fg_color="white",
                               corner_radius=10)
frame.pack(padx=20, pady=20)


user_id_entry = customtkinter.CTkEntry(master=frame,
                                        placeholder_text="User ID",
                                        width=200,
                                        height=30,
                                        corner_radius=10)
user_id_entry.place(relx=0.5, rely=0.2, anchor=CENTER)



password_entry = customtkinter.CTkEntry(master=frame,
                                        placeholder_text="Password",
                                        width=200,
                                        height=30,
                                        show="*",
                                        corner_radius=10)

password_entry.place(relx=0.5, rely=0.4, anchor=CENTER)

button = customtkinter.CTkButton(master=frame,
                                 text="Login",
                                 width=200,
                                 height=30,
                                 corner_radius=10)

button.place(relx=0.5, rely=0.6, anchor=CENTER)



app.mainloop()