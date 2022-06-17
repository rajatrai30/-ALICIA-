from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from pynput.keyboard import Key, Controller
import userHandler
from userHandler import UserData

u = UserData()
u.extractData()
avatarChoosen = u.getUserPhoto()

def closeWindow():
	keyboard = Controller()
	keyboard.press(Key.alt_l)
	keyboard.press(Key.f4)
	keyboard.release(Key.f4)
	keyboard.release(Key.alt_l)

def SavePhoto():
	userHandler.UpdateUserPhoto(avatarChoosen)
	closeWindow()

def selectAVATAR(avt=0):
	global avatarChoosen
	avatarChoosen = avt

	i=1
	for avtr in (avtb1,avtb2):
		if i==avt:
			avtr['state'] = 'disabled'
		else:
			avtr['state'] = 'normal'
		i+=1

if __name__ == "__main__":

	background = '#F6FAFB'
	avtrRoot = Tk()
	avtrRoot.title("Choose Avatar")
	avtrRoot.configure(bg=background)
	w_width, w_height = 500, 450
	s_width, s_height = avtrRoot.winfo_screenwidth(), avtrRoot.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	avtrRoot.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30))

	Label(avtrRoot, text="Choose Your Avatar", font=('arial bold', 15), bg=background, fg='#303E54').pack(pady=10)

	avatarContainer = Frame(avtrRoot, bg=background)
	avatarContainer.pack(pady=10, ipadx=50, ipady=20)
	size = 100

	#create a main frame
	main_frame = Frame(avatarContainer)
	main_frame.pack(fill=BOTH, expand=1)

	#create a canvas
	my_canvas = Canvas(main_frame, bg=background)
	my_canvas.pack(side=LEFT, expand=1, fill=BOTH)

	#add a scrollbar to the canvas
	my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
	my_scrollbar.pack(side=RIGHT, fill=Y)

	#configure the canvas
	my_canvas.configure(yscrollcommand=my_scrollbar.set)
	my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox('all')))

	#create another frame inside the canvas
	second_frame = Frame(my_canvas)
	
	#add that new frame to a window in the canvas
	my_canvas.create_window((0,0), window=second_frame, anchor='nw')

	avtr1 = ImageTk.PhotoImage(Image.open('extrafiles/images/avatars/a1.png').resize((size, size)), Image.ANTIALIAS)
	avtr2 = ImageTk.PhotoImage(Image.open('extrafiles/images/avatars/a2.png').resize((size, size)), Image.ANTIALIAS)
	
	
	avtb1 = Button(second_frame, image=avtr1, bg=background, activebackground=background, relief=FLAT, bd=0, command=lambda:selectAVATAR(1))
	avtb2 = Button(second_frame, image=avtr2, bg=background, activebackground=background, relief=FLAT, bd=0, command=lambda:selectAVATAR(2))
	
	

	avtb1.grid( row=0, column=0, ipadx=25, ipady=10)
	avtb2.grid( row=0, column=1, ipadx=25, ipady=10)


	BottomFrame = Frame(avtrRoot, bg=background)
	BottomFrame.pack(pady=10)
	Button(BottomFrame, text='         Update         ', font=('Montserrat Bold', 15), bg='#01933B', fg='white', bd=0, relief=FLAT, command=SavePhoto).grid(row=0, column=0, padx=10)
	Button(BottomFrame, text='         Cancel         ', font=('Montserrat Bold', 15), bg='#EDEDED', fg='#3A3834', bd=0, relief=FLAT, command=closeWindow).grid(row=0, column=1, padx=10)

	avtrRoot.iconbitmap("extrafiles/images/changeProfile.ico")
	avtrRoot.mainloop()
