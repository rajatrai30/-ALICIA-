from tkinter import *
import ttkthemes
from tkinter import ttk


def select(value):
    if value== 'Space':
        textarea.insert(INSERT, " ")

    elif value== 'Enter':
        textarea.insert(INSERT,'\n')

    elif value=='Tab':
        textarea.insert(INSERT,'\t')

    elif value=='Del':
        textarea.delete(1.0,END) #This will delete everything on text area

    elif value=='Backs':
        prev=textarea.get(1.0,END)
        current=prev[:-2] #text\n  that's why we have used 2
        textarea.delete(1.0,END)  #deleting entire thing from textarea
        textarea.insert(INSERT,current)  #printing new textarea data with deleted alphabet or space

    elif value=='Shift ↑' :
        leftShiftButtons = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', 'Backs', 'Del',
                            'Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', ']', '7', '8', '9',
                            'Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':', 'Enter', '4', '5', '6',
                            'Shift ↑', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '<', '>', '?', '↑ Shift', '1', '2', '3',
                            'Space'

                            ]
        varRow=2
        varColumn=0
        for button in leftShiftButtons:
            command = lambda x=button: select(
                x)  # Lambda keyword helps to create a one line function  syntax lamda arguements:expression
            if button != 'space':
                ttk.Button(root, text=button, width=5, command=command).grid(row=varRow, column=varColumn)

            else:
                ttk.Button(root, text=button, width=30).grid(row=6, column=0, columnspan=15)  # columnspan not working

            varColumn += 1
            if varColumn > 14:  # Because we want only 14 buttons in each row
                varColumn = 0
                varRow += 1

    elif value=='↑ Shift':  #to set back keyboard to normal
        varRow=2
        varColumn=0
        for button in buttons:
            command = lambda x=button: select(
                x)  # Lambda keyword helps to create a one line function  syntax lamda arguements:expression
            if button != 'space':
                ttk.Button(root, text=button, width=5, command=command).grid(row=varRow, column=varColumn)

            else:
                ttk.Button(root, text=button, width=30).grid(row=6, column=0, columnspan=15)  # columnspan not working

            varColumn += 1
            if varColumn > 14:  # Because we want only 14 buttons in each row
                varColumn = 0
                varRow += 1

    elif value=='Caps':  #Converts alphabets in capital letters
        capsButtons = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backs', 'Del',
                       'Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', '7', '8', '9',
                       'CAPS', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', 'Enter', '4', '5', '6',
                       'Shift ↑', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', '↑ Shift', '1', '2', '3',
                       'Space']
        varRow=2
        varColumn=0
        for button in capsButtons:
            command = lambda x=button: select(
                x)  # Lambda keyword helps to create a one line function  syntax lamda arguements:expression
            if button != 'space':
                ttk.Button(root, text=button, width=5, command=command).grid(row=varRow, column=varColumn)

            else:
                ttk.Button(root, text=button, width=30).grid(row=6, column=0, columnspan=15)  # columnspan not working

            varColumn += 1
            if varColumn > 14:  # Because we want only 14 buttons in each row
                varColumn = 0
                varRow += 1

    elif value == 'CAPS': #sets keyboard back to normal
        varRow=2
        varColumn=0
        for button in buttons:
            command = lambda x=button: select(
                x)  # Lambda keyword helps to create a one line function  syntax lamda arguements:expression
            if button != 'space':
                ttk.Button(root, text=button, width=5, command=command).grid(row=varRow, column=varColumn)

            else:
                ttk.Button(root, text=button, width=30).grid(row=6, column=0, columnspan=15)  # columnspan not working

            varColumn += 1
            if varColumn > 14:  # Because we want only 14 buttons in each row
                varColumn = 0
                varRow += 1

    else:   #prints the value apart from the special keys 
        textarea.insert(INSERT,value)







    textarea.focus_set()  #helps to make cursor blink at all positions while typing


root = ttkthemes.ThemedTk() #creates the instances of class

root.get_themes()           #helps to get variety of themes from ttk
root.set_theme("radiance")  #radiance is a theme in ttk  2. kroc

root.title("On-Screen Keyboard")  #helps to re-write the window title
root.resizable(False,False)  #(width,height)  passing false value helps to stop maximize function of the window

#Title
title=Label(root, text = "Virtual Keyboard",font = ('arial',20))  #font ("Name of font",Height_font)
title.grid(row = 0 , column = 0, columnspan = 15)  #Grid is one type of method to display things on the window

#Text Area where text is going to be visible
textarea = Text(root,font=("arial",15,"bold"),height = 10, width = 100, border = 10,relief = SUNKEN)  #Text class   #font ("Name of font",Height_font, bold style) height = 10 reduces size of textarea
textarea.grid(row = 1, column = 0, columnspan = 15)
textarea.focus_set() #Makes the Cursor Blink on text area


varRow=2   #row = 2 because on row 1 we have textarea so the buttons should be displayed below text area
varColumn=0

#list of name button
buttons = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backs', 'Del',
           'Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', '7', '8', '9',
           'Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', 'Enter', '4', '5', '6',
           'Shift ↑', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '↑ Shift', '1', '2', '3',
           'Space']

for button in buttons:
    command = lambda x=button: select(x)   #Lambda keyword helps to create a one line function  syntax lamda arguements:expression
    if button != 'space' :
        ttk.Button(root,text=button,width = 5, command = command).grid(row = varRow , column = varColumn)

    else :
        ttk.Button(root, text = button,width = 30).grid( row = 6 , column = 0, columnspan = 15)  #  not working

    varColumn+=1
    if varColumn>14 :             #Because we want only 14 buttons in each row
        varColumn=0
        varRow+=1



root.mainloop()  #holds the output or window on the loop