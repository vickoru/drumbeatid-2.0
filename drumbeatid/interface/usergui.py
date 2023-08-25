from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from drumbeatid.params import *
from drumbeatid.interface.main import predict


window = Tk()
window.geometry("600x600+60+30")
# window.geometry("500x300")
window.title('drumbeatID 2.0 🥁')
# window.iconbitmap('c:/gui/codemy.ico')

db_path_var = StringVar()


def choosefile():
    db_path = filedialog.askopenfilename(initialdir=AUDIO_TEST_FILEPATH,
                                    title="Choose a drumbeat",
                                    filetypes=(("wav Files", "*.wav"), ))
    # strip out the directory info and .mp3 extension from the song name
    # db = db.replace("C:/gui/audio/", "")
	# db = db.replace(".mp3", "")
    db_path_var.set(db_path)
	# Add song to listbox
    db_box.insert(END, db_path)

def analyze(audiofile):
    # pass
    # prediction = predict(audiofile=audiofile)

    lbl_=Label(
    window, text='prediction',
    fg='black', font=("Helvetica", 22))
    lbl_.place(x=60, y=350)



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

#


# Create Master Frame
master_frame = Frame(window)
master_frame.pack(pady=20)

# Create Playlist Box
db_box = Listbox(master_frame, bg="black", fg="black",
                 width=60, selectbackground="green", selectforeground="black")
# db_box = Listbox(master_frame)
db_box.place(x=100, y=250)

# Creating button to analyze
# analyze_button_img = PhotoImage(file=os.path.join(IMAGES_PATH, 'power.png'))
img = Image.open(
    os.path.join(IMAGES_PATH, 'power.png')).resize((50,50))
analyze_button_img = ImageTk.PhotoImage(img)
# btn = Button(window, image=analyze_button_img,
#              borderwidth=0, command=analyze(AUDIO_TEST_FILEPATH))
# btn.place(x=285, y=400)
lbl_analyze=Label(
    window, text="Analyze",
    fg='black', font=("Helvetica", 18))
lbl_analyze.place(x=280, y=470)


window.mainloop()
