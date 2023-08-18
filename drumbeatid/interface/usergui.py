from tkinter import *
from PIL import Image, ImageTk
import os
from drumbeatid.params import *




window = Tk()
window.geometry("600x600+60+30")
# window.geometry("500x300")
window.title('drumbeatID 2.0 🥁')
# window.iconbitmap('c:/gui/codemy.ico')


def analyze():
    pass

def choosefile():
    pass


# Button to choose your file
lbl=Label(
    window, text="Choose your drumbeat sound file",
    fg='black', font=("Helvetica", 22))
lbl.place(x=60, y=50)
file_btn = Button()
# txtfld=Entry(window, text="Analyze", bd=5)
# txtfld.place(x=80, y=150)
file_btn = Button(window, text="Choose .wav file",
             borderwidth=0, command=choosefile,
             font=("Helvetica", 18), width=15)
file_btn.place(x=60, y=100)


# Creating button to analyze
# analyze_button_img = PhotoImage(file=os.path.join(IMAGES_PATH, 'power.png'))
img = Image.open(
    os.path.join(IMAGES_PATH, 'power.png')).resize((50,50))
analyze_button_img = ImageTk.PhotoImage(img)
btn = Button(window, image=analyze_button_img,
             borderwidth=0, command=analyze)
btn.place(x=285, y=400)
lbl_analyze=Label(
    window, text="Analyze",
    fg='black', font=("Helvetica", 18))
lbl_analyze.place(x=280, y=470)




window.mainloop()
