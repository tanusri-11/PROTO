from tkinter import *
from PIL import Image, ImageTk, ImageFilter
from main import Action
from main import takeCommand
def User_send():
    send = entry1.get()
    bot = Action(send)
    text.insert(END, "USER  --> " + send + "\n")
    if bot != None:
        text.insert(END, "PROTO <-- " + str(bot) + "\n")
    if bot == "ok sir":
        root.destroy()
def ask():
    ask_val = takeCommand()
    bot_val = Action(ask_val)
    text.insert(END, "USER  --> " + ask_val + "\n")
    if bot_val != None:
        text.insert(END, "PROTO <-- " + str(bot_val) + "\n")
    if bot_val == "ok sir":
        root.destroy()
def delete_text():
    print("remove")
    text.delete("1.0", "end")
def on_entry_click(event):
    if entry1.get() == 'Enter your text here':
        entry1.delete(0, "end")  # Delete the placeholder text
        entry1.config(fg='black')  # Change text color to black

def on_focus_out(event):
    if not entry1.get():  # If the entry is empty
        entry1.insert(0, 'Enter your text here')  # Insert placeholder text
        entry1.config(fg='grey')  # Change text color to grey

root = Tk()
root.geometry("990x900")
root.title("PROTO Assistant")
root.resizable(False, False)
root.config(bg="#242073")

# Main Frame
Main_frame = LabelFrame(root, padx=280, pady=0, relief="sunken")
Main_frame.config(bg="#6865DF")
Main_frame.grid(row=0, column=1, padx=55, pady=40)

# Text Lable
Text_label = Label(Main_frame, text="PROTO Assistant", font=("comic Sans ms", 14, "bold"), bg="#6F67B9")
Text_label.grid(row=0, column=0, padx=20, pady=10)

# Image
Display_Image = ImageTk.PhotoImage(Image.open("image.png"))
Image_Label = Label(Main_frame, image=Display_Image)
Image_Label.grid(row=1, column=0, pady=20)

# Add a text widget

text = Text(root, font='Courier 10 bold', bg="#C7BEEE", borderwidth=3)
text.grid(row=2, column=2,sticky="nsew")
text.place(x=100, y=400, width=775, height=300)


# Add a entry widget
entry1 = Entry(root, justify=LEFT,borderwidth=2, relief=SOLID)
entry1.place(x=100, y=725, width=775, height=50)

entry1.insert(0, 'Enter your commands HERE')
entry1.config(fg='grey')
entry1.bind('<FocusIn>', on_entry_click)
entry1.bind('<FocusOut>', on_focus_out)

# Add a text button1
button1 = Button(root, text="ASK",bg="#8AA4F5", pady=16, padx=40, borderwidth=3, relief=SOLID ,command=ask)
button1.place(x=100, y=800)

# Add a text button2
button2 = Button(root, text="SEND", bg="#8AA4F5", pady=16, padx=40, borderwidth=3, relief=SOLID, command=User_send)
button2.place(x=740, y=800)

# Add a text button3
button3 = Button(root, text="CLEAR",bg="#8AA4F5", pady=16, padx=40, borderwidth=3, relief=SOLID, command=delete_text)
button3.place(x=420, y=800)

root.mainloop()