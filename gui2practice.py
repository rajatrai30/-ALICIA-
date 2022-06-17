from tkinter import *
from PIL import ImageTk, Image

root = Tk()

root.title('assistant')
root.geometry('520x320')

img = ImageTk.PhotoImage(Image.open('assistant.png'))
panel = Label(root, image=img)
panel.pack(side='right', fill='both', expand='no')
compText = StringVar()
userText = StringVar()
userText.set('Your Virtual Assistant')
userFrame = LabelFrame(root, text='Lena', font=('Railways', 24, 'bold'))
userFrame.pack(fill='both', expand='yes')
top = Message(userFrame, textvariable=userText, bg='black', fg='white')
top.config(font=("Century Gothic", 15, 'bold'))
top.pack(side='top', fill='both', expand='yes')
btn = Button(root, text='Speak', font=('railways', 10, 'bold'),bg='red', fg='white',).pack(fill='x', expand='no')
btn2 = Button(root, text='Close', font=('railways', 10, 'bold'), bg='yellow', fg='black',).pack(fill='x', expand='no')
root.mainloop()