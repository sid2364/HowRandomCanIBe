'''
pip install SpeechRecognition
yum install portaudio-devel portaudio-19
pip install pyaudio
'''
import speech_recognition

recogizer = speech_recognition.Recognizer()

with speech_recognition.Microphone() as mic:
	print("Speak now, I'm listening!")
	audio = recogizer.listen(mic)

	try:
		print("Did you say: " + recogizer.recogize_google(audio))
	except Exception, e:
		print("There was an error. " + e)