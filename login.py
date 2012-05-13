# File name: tkinterEntryWidget.py
# Author: S.Prasanna

from Tkinter import *
import tkMessageBox
from main_window import mainWindow

def displayText():
    """ Display the Entry text value. """

    global entryWidget

    if entryWidget.get().strip() == "":
        tkMessageBox.showerror("Login", "Fill all the fields")
    else:
      	chatApp = mainWindow(entryWidget.get().strip(), passWidget.get().strip(),  skillWidget.get().strip(), genreWidget.get().strip())

if __name__ == "__main__":

    root = Tk()
    
    root.title("Login")
    root["padx"] = 40
    root["pady"] = 20       

    # Create a text frame to hold the text Label and the Entry widget
    textFrame = Frame(root)
    passFrame = Frame(root)
    genreFrame = Frame(root)
    skillFrame = Frame(root)

    #Create a Label in textFrame
    entryLabel = Label(textFrame)
    entryLabel["text"] = "Username:"
    entryLabel.pack(side=LEFT)

    # Create an Entry Widget in textFrame
    entryWidget = Entry(textFrame)
    entryWidget["width"] = 50
    entryWidget.pack(side=LEFT)

	#Create a Label in textFrame
    passLabel = Label(passFrame)
    passLabel["text"] = "Password: "
    passLabel.pack(side=LEFT)

	# Create an Entry Widget in textFrame
    passWidget = Entry(passFrame, show="*")
    passWidget["width"] = 50
    passWidget.pack(side=LEFT)

	#Create a Label in textFrame
    genreLabel = Label(genreFrame)
    genreLabel["text"] = "Genre:      "
    genreLabel.pack(side=LEFT)

	# Create an Entry Widget in textFrame
    genreWidget = Entry(genreFrame)
    genreWidget["width"] = 50
    genreWidget.pack(side=LEFT)

	#Create a Label in textFrame
    skillLabel = Label(skillFrame)
    skillLabel["text"] = "Skill out of 10:"
    skillLabel.pack(side=LEFT)

	# Create an Entry Widget in textFrame
    skillWidget = Entry(skillFrame)
    skillWidget["width"] = 50
    skillWidget.pack(side=LEFT)

    textFrame.pack()
    passFrame.pack()
    genreFrame.pack()
    skillFrame.pack()
    button = Button(root, text="Submit", command=displayText)
    button.pack() 
    
    root.mainloop()
