# Import packages
from tkinter import *
from PIL import ImageTk, Image
from easygoogletranslate import EasyGoogleTranslate
import pytesseract
from tkinter import filedialog, messagebox

try:
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\Tesseract.exe'  # must change to your path
except:
    messagebox.showwarning("Tesseract Error", "Before running the program, you must download Tesseract and change the "
                                              "path in the source code to your own path. Link in readme.txt")

root = Tk()
root.title("Image Transcriber")
root.geometry("800x800")

clicked = StringVar()
clicked.set("English")

lang_dict = {"Albanian": "sq",
             "Arabic": "ar",
             "Armenian": "hy",
             "Bengali": "bn",
             "Bosnian": "bs",
             "Bulgarian": "bg",
             "Chinese (S)": "zh-CN",
             "Chinese (T)": "zh-TW",
             "Croatian": "hr",
             "Czech": "cs",
             "Danish": "da",
             "Dutch": "nl",
             "English": "en",
             "Finnish": "fi",
             "French": "fr",
             "German": "de",
             "Greek": "el",
             "Hebrew": "he",
             "Hindi": "hi",
             "Hungarian": "hu",
             "Irish": "ga",
             "Indonesian": "id",
             "Italian": "it",
             "Japanese": "ja",
             "Korean": "ko",
             "Latin": "la",
             "Polish": "pl",
             "Punjabi": "pa",
             "Russian": "ru",
             "Romanian": "ro",
             "Swedish": "sv",
             "Spanish": "es"}

options = ["Albanian",
           "Arabic",
           "Armenian",
           "Bengali",
           "Bosnian",
           "Bulgarian",
           "Chinese (S)",
           "Chinese (T)",
           "Croatian",
           "Czech",
           "Danish",
           "Dutch",
           "English",
           "Finnish",
           "French",
           "German",
           "Greek",
           "Hebrew",
           "Hindi",
           "Hungarian",
           "Irish",
           "Indonesian",
           "Italian",
           "Japanese",
           "Korean",
           "Latin",
           "Punjabi",
           "Russian",
           "Romanian",
           "Polish",
           "Swedish",
           "Spanish"]


def open():
    global img_label
    global img
    global result

    root.filename = filedialog.askopenfilename(initialdir="D:/Pictures", title="Choose an Image!",
                                               filetypes=(('Images', '*.png'), (('JPG files', '*.jpg'),
                                                                                ('All files', '*.*'))))

    img = ImageTk.PhotoImage(Image.open(root.filename))

    if img.width() > 750:
        messagebox.showwarning("Error: Image Width too Large",
                               "Image's width is greater than 750px, please choose a smaller file.")
    elif img.height() > 750:
        messagebox.showwarning("Error: Image Height too Large",
                               "Image's Height is greater than 750px, please choose a smaller file.")
    else:
        img_label.destroy()
        img_label = Label(root, image=img, borderwidth=3, relief="raised")
        img_label.place(relx=0.5, rely=0.48, anchor=CENTER)

        transcribe_button.configure(state=ACTIVE)
        translate_button.configure(state=ACTIVE)
        languages.config(state=ACTIVE)

        result = pytesseract.image_to_string(Image.open(root.filename))


def transcribe():
    global result

    if result == "":
        messagebox.showwarning("Error: Unable to be Transcribed",
                               "Image is unable to be transcribed, please try another image.")
    else:
        top = Toplevel()

        text_label = Label(top, text=result, font=("Times New Roman", 10))
        text_label.grid(row=0, column=0, padx=20, pady=20)

        input = Entry(top, width=50)
        input.insert(0, result)
        input.grid(row=1, column=0, padx=20, pady=20)


def translate():
    global result
    global clicked
    global lang_dict

    if result == "":
        messagebox.showwarning("Error: Unable to be Translated",
                               "Image is unable to be translated, please try another image.")
    else:
        top = Toplevel()

        translator = EasyGoogleTranslate(source_language='en', target_language=(lang_dict[clicked.get()]))
        translated = translator.translate(result)

        text_label = Label(top, text=translated, font=("Times New Roman", 10))
        text_label.grid(row=0, column=0, padx=20, pady=20)

        input = Entry(top, width=50)
        input.insert(0, translated)
        input.grid(row=1, column=0, padx=20, pady=20)


upload_button = Button(root, text="Choose File...", command=open)

img_label = Label(root, text="Upload an image to get started!\n (Image must be smaller than 750x750)", borderwidth=3.5,
                  relief="ridge", width=55,
                  height=30, font=("Arial Rounded MT Bold", 15))

transcribe_button = Button(root, text="Transcribe", command=transcribe, state=DISABLED)

translate_button = Button(root, text="Translate", command=translate, state=DISABLED)

languages = OptionMenu(root, clicked, *options)
languages.config(state=DISABLED)

img_label.place(relx=0.5, rely=0.48, anchor=CENTER)
upload_button.place(relx=0.5, rely=0.96, anchor=CENTER)
transcribe_button.place(relx=0.65, rely=0.96, anchor=CENTER)
translate_button.place(relx=0.35, rely=0.96, anchor=CENTER)
languages.place(relx=0.25, rely=0.96, anchor=CENTER)

root.mainloop()
