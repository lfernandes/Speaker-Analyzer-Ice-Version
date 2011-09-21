# -*- coding: UTF-8 -*-
from __future__ import division
from numpy.fft import rfft
from numpy import argmax, mean, diff, log, fromstring
from matplotlib.mlab import find
from scipy.signal import fftconvolve, kaiser
from time import time
import sys
import wave, Queue

def parabola(data,x):

	v1=1/2*(data[x-1]-data[x+1])/(data[x-1]-2*data[x]+data[x+1])+x
	v2=data[x]-1/4*(data[x-1]-data[x+1])*(v1 - x)
	return (v1, v2)

def Fundamental_Frequency_autocorrelation(signal, fs):

	correlacao = fftconvolve(signal, signal[::-1], mode='full')
	correlacao = correlacao[len(correlacao)/2:]
	d = diff(correlacao)
	inicio = find(d > 0)[0]
	pico = argmax(correlacao[inicio:]) + inicio
	picox, picoy = parabola(correlacao, pico)
	return fs / picox

def checkFreq(filename):
	spf = wave.open(filename,'r')
	signal = spf.readframes(-1)
	signal = fromstring(signal, 'Int16')
	fs = spf.getframerate()
	print 'Iniciando a analize de frequência do arquivo: “%s”\n' % filename
	print 'Calculando a Frequencia por autocorrelação:',
	start_time = time()
	freq  = Fundamental_Frequency_autocorrelation(signal, fs)
	print '%f Hz' % freq
	freq = int(freq)
	#print 'Tempo: %.3f s\n' % (time() - start_time)

	return freq

#def checkRMS(filename):
	













