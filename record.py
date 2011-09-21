import pyaudio # download in: http://people.csail.mit.edu/hubert/pyaudio/
import audioop
import wave
import sys, time
from time import time
import Queue

def record(RECORD_SECONDS=3,WAVE_OUTPUT_FILENAME="",q=0):
	chunk = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	failCount = 0
	failFlag = False
	
	p = pyaudio.PyAudio()

	stream = p.open(format = FORMAT,
		             channels = CHANNELS,
		             rate = RATE,
		             input = True,
		             frames_per_buffer = chunk)

	print "Gravando..."
	all = []
	for i in range(0, RATE / chunk * RECORD_SECONDS):
		 data = stream.read(chunk)
		 rms = audioop.rms(data, 2)

		 if(rms < 1750):# debounce
		 	if(failFlag == True):
				if((time() - failTime) < 1): #um segundo de diferenca
					failCount += 1
			 		print "\n {0}".format(failCount)
				elif((time() - failTime) > 1): #estabilizado dentro de um segundo, esta ok
					failFlag = False
					print "\n estabilizado dentro de um segundo..."
			else: #Primeira falha
				failTime = time()
				failFlag = True
				print "\n Primeira vez que falhou"

		 all.append(data)
	print "Gravacao concluida."

	stream.close()
	p.terminate()

	if(WAVE_OUTPUT_FILENAME):#Salva em arquivo WAV
		data = ''.join(all)
		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(data)
		wf.close()

		q.put(failCount) # return


if __name__ == '__main__':
	WAVE_OUTPUT_FILENAME = "Record.wav"
	print "Voce executou o modulo de gravacao. Gerando o arquivo {0}".format(WAVE_OUTPUT_FILENAME)
	#print "\n {0}".format(rms)
	# write data to WAVE file
	data = ''.join(all)
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(data)
	wf.close()

