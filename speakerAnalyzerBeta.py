#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# ==============================================
# ------------- Speaker Analyzer ---------------
# --------------- Ice Version ------------------
#
# O Speaker Analyzer é um programa para testes
# do microfone e dos auto-falates. Esta versão
# possibilita que a análise seja realizada em 
# qualquer plataforma que suporte python.
#
# Créditos:
# -----------------= Créditos =-----------------
# ------------ Lucas L. Fernandes --------------
# ---------------- Fabio Reina -----------------
# --------- Antônio Carlos D. Grande Jr --------
# ----------- Douglimar D. de Moraes -----------
# ==============================================

#Definindo o main
__name__ = '__main__'

#import's
import time as Time
import math, sys, wav
from time import time
import toneGenerator as tom
import record as rec
import analisadorFreq as analisador
import threading
from threading import Thread
import Queue

#Setup
freq = 1000 #Hz
fr = 44100 #frame rate
duration = 5 #seconds
fileTone = 'tom.wav'
fileRec = 'record.wav'
toleranciaMic = 2 # Falhas durante o processo
toleranciaFreq = 10 # porcentagem da diferênça tolerada
errors = ""

#default
nc=1
nf = (fr * (duration + 1))
sig = [ math.cos( 2.0 * math.pi * freq * x / fr ) for x in range(nf) ]
a = 0

#Threads
qRec = Queue.Queue()
qPlayTone = Queue.Queue()
thRec = Thread(target=rec.record, args = (duration, fileRec, qRec)) #Thread Record
thPlayTone = Thread(target=wav.playWav, args=(fileTone, nc, fr, qPlayTone)) #Thread Play

def calcTolerancia(vlBase, tolerancia):
	return ((vlBase * tolerancia) / 100) + vlBase

def isWithinTolRange(value):
	maxi = calcTolerancia(freq, toleranciaFreq)
	mini = calcTolerancia(freq, -toleranciaFreq)
	if(value > maxi or value < mini):
		print "{0} - {1} - {2}".format(maxi, mini, value)
		return False
	return True

#Init do Main
if __name__ == '__main__':
	tom.genTom(sig, 1, fr, nf, fileTone, freq) #Talvez nao precisa fazer isto toda a vez	
	try:
		print "* Iniciando o teste..."
		start_time = time()#Hora que se iniciou o teste
		
		thPlayTone.start() #Inicia a thread do Tom
		Time.sleep(0.100) # Aguarda 100ms
		thRec.start() #Inicia a thread de gravação

		while (threading.active_count() > 1): # Enquanto as threads estiverem em execução...
			pass #Aguarda o fim das threads

		# Finalizou? então vamos obter resultados

		#Analiza o microfone e o volume do alto-falante
		recReturn = qRec.get() # Obtem a quantidade de falha(s) (cortes) encontrada(s) na captação pelo microfone
		PlayToneReturn = qPlayTone.get()

		if(PlayToneReturn is False): # Conseguiu reproduzir o áudio?
			errors += "*** Falha: Não foi possível reproduzir o arquivo.\n"

		if(recReturn > toleranciaMic): # A quantidade de falhas (cortes) é tolerável?
			errors += "*** Falha no microfone.\nO microfone apresentou muitas falhas ao tentar capturar o áudio ({0} falhas por segundo).\n".format(recReturn)

		#Analiza a frequência do áudio captado pelo mic
		freqReturn = analisador.checkFreq(fileRec) # Obtem a frequência do áudio de entrada
		if(isWithinTolRange(freqReturn) is False): # A frequência capturada está dentro do range de tolerância?
			errors += "*** Falha: Nível de frequência fora do permitido.\nFrequência do áudio capturado: {0}. Objetivo: {1} (+/- {2}%)\n".format(freqReturn, freq, toleranciaFreq)
		
		if (errors):
			print errors
			print "\n O teste apresentou falhas.  ------ Reprovado ------"
		else:
			print "\n*** Aprovado! ***\n"
		
		print 'Tempo total do teste: %.3f segundos\n' % (time() - start_time)
		sys.exit()

	except IOError as (errno, strrror):
		print "Ocorreu um erro ao realizar o teste.\nErro num:{0} - {1}\nfindMe $0001".format(errno, strerror)
		













