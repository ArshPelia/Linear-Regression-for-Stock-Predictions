import tkinter
import customtkinter  # <- import the CustomTkinter module

root_tk = tkinter.Tk()  # create the Tk window like you normally do
root_tk.geometry("400x240")
root_tk.title("CustomTkinter Test")


def button_function():
    stock_name = stock_entry.get()
    print("Stock name entered: ", stock_name)

customtkinter.set_appearance_mode("Dark") # Other: "Light", "System" (only macOS)
# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=root_tk, text='Execute' , corner_radius=10, command=button_function)
button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

label = customtkinter.CTkLabel(master=root_tk,
                               text="Stock Name: ",
                               width=120,
                               height=25,
                               text_color="Black",
                               corner_radius=8)
label.place(relx=0.2, rely=0.2, anchor=tkinter.CENTER)


stock_entry = customtkinter.CTkEntry(master=root_tk,
                               width=120,
                               height=25,
                               corner_radius=10)
stock_entry.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)


root_tk.mainloop()