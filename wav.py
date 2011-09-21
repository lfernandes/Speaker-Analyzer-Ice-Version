# Aqui tentamos tocar o som, pois /dev/dsp pode estar ocupada
# Isso causa um erro e o encerramento do programa
# Mas com esse try, o interpretador esta instruido a nao interromper a execussao
# No caso de erro, mas sim pular para o bloco que segue o 'except'
# Isso e' conhecido como Error Handling
import wave, ossaudiodev

def playWav(fileName, nc=1, fr=44100, q=False):
	print 'Iniciando a reproducao do audio...'
	mysound = wave.open(fileName , 'rb')

	# Atraves de metodos do objeto mysound, criado com o objeto 'wave.open',
	# extraimos as informacoes do arquivo de som:

	# 1- taxa de amostragem
	fr = mysound.getframerate()
	# 2- Numero de canais
	nc = mysound.getnchannels()
	# 3- Numero de amostras
	nf = mysound.getnframes()

	# lendo o arquivo, e guardando ele no objeto 'data'
	# Isto e, lendo todas as amostras do objeto 'mysound'
	data = mysound.readframes(nf)
	mysound.close()
	
	# Abrindo o /dev/dsp para escrita e ajeitando seus parametros
	# (veja o script anterior a este)
	try:
		dsp = ossaudiodev.open('/dev/dsp','w')
		dsp.setparameters(ossaudiodev.AFMT_S16_NE, nc, fr)
		# Escrevendo na /dev/dsp para tocar o som
		dsp.write(data)
		# Fechando a comundicacao com /dev/dsp
		dsp.close()
		q.put(True) #Reproduzido com sucesso
		#print "Finalizando a reproducao."
	except IOError as (errno, strrror):
		q.put(False) #Nao reproduziu
		print "Erro ao tentar reproduzir o arquivo {0}.\nErro num:{1} - {2}\nfindMe $0002".format(fileName, errno, strerror)

	

	
