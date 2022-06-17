import qrcode
import speech_recognition as sr

r = sr.Recognizer()

#Asks for the URL
with sr.Microphone() as source:
	print('Say Link to the Website...')
	audio1 = r.listen(source)
	try:
		text1 = r.recognize_google(audio1)
		print('You said :{}'.format(text1))

	except:
		print('Cannot Listen')

#Asks the name to save the file 
with sr.Microphone() as source:
	print('What should be file name...')
	audio = r.listen(source)

	try:
		text = r.recognize_google(audio)
		print('Saving as :{}'.format(text),'.png')

	except:
		print('Cannot Listen')


img = qrcode.make('https://'+text1+'/in/') #Accepts the Users URL 
img.save(text+'.png') #Creates image in the form of QR code using URL


if 'generate qr code' in text:
                speak("Say Link to the Website...", True, True)
                audio1 =  record().lower()
                try:
                    text1 = r.recognize_google(audio1)
                    speak('You said :{}'.format(text1), True, True)
                except:
                    speak('Cannot Listen', True, True)
                speak('What should be file name...', True, True)
                
                audio = record().lower()
                try:
                    text = record().lower()
                    print('Saving as :{}'.format(text),'.png')
                except:
                    speak('Cannot Listen', True, True)
                img = qrcode.make('https://'+text1+'/in/') #Accepts the Users URL 
                img.save(text+'.png') #Creates image in the form of QR code using URL

