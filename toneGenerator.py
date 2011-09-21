
# Programa sombibstd3.py

import wave, struct, ossaudiodev

# Definindo uma funcao. Esta pode ser utilizada pelo nome,
# Ou, quando importarmos este script como um modulo,
# Pode ser chamada como um metodo do modulo.
# Ao definir uma funcao, voce deve especificar quais parametros ela precisa receber
# para ser inicializada, no caso:
# sig (sinal), fr (taxa de amostragem)
# nc (numero de canais), nf (numero de amostras)
# Poderiamos tambem incluir a resolucao de cada amostra,
# Mas resolvemos fazer sons somente com 16 bits.
# Quem estiver ja sendo especificado, e' opcional quando a funcao for chamada
# e recebe o valor que esta' na sua criacao (com o '=')
# Quem nao estiver sendo especificado na criacao, deve ser especificado quando a funcao for chamada
# ou causara' erro e a interrupcao do programa

def genTom(sig, nc=1, fr=44100, nf=88200, fileName='temp.wav', freq=1000):

	print "Gerando um tom de {0}Hz...".format(freq)
	# se o objeto sig for uma lista:
	if type(sig) == list:
		# valores maximos e minimos da lista
		min_sig = min(sig)
		max_sig = max(sig)
		
		# ambito
		ambit = 2.0 * max(max_sig, -min_sig)
		

		# Achando a escala dos valores de sig para 16 bits
		# Caso o ambito seja menor do que 2
		# Que e' o maximo em medida RMS ou Peak para audio digital em computadores
		# Preservar a proporcao de aplitude
		if ambit < 2:
			scale = ( 2**16 - 1 ) * (ambit / 2)
		
		# Caso contrario, ou seja, o ambito seja menor do que 2
		# Fazer a escala para normalizar
		# Normalizar e' fazer com que o sinal varie em amplitude por
		# todo o ambito permitido
		else:
			scale = ( 2**16 - 1 ) / ( ambit )

		# sinal em 16 bits
		sig_16bit = [ int(scale*x) for x in sig ]

		# O sinal sera uma string (para o python) de variaveis C short signed por hora vazia
		data = ''

		# Escrever o sinal no objeto data, x += y e' o mesmo que x = x + y
		# O que, para strings no Python, e' o mesmo que adicionar y no final
		for i in range( len(sig_16bit) ):
			data += struct.pack('h',sig_16bit[i])
	else:
		# Caso o sinal 'sig' nao seja uma lista, vamos aceita-lo como nosso 'data'
		# na sorte de que seja uma string de variaveis short-signed C
		data=sig

        # Escrevendo o arquivo de som (veja o script anterior a este)
	try:
		sound = wave.open(fileName,'w')
		sound.setnchannels(nc)
		sound.setframerate(fr)
		sound.setsampwidth(2)
		sound.writeframes(data)
		print "Arquivo {0} gerado com sucesso!".format(fileName)
	except IOError:
		print "**** Falha: Erro ao gerar o arquivo."

# vai aqui um truque. A variavel global __name__ so' sera' __main__ se rodarmos o 
# programa noo como um modulo, mas como o programa principal. Assim podemos
# testar nosso script sem ter que fazer outro script para importa'-lo como um modulo.

# Se '__name__' for a string '__main__'
if __name__ == '__main__':
	# Abra um som e o rode, veja os 2 scripts anteriores a este
	#sound = wave.open('/home/satux/Music/Kalimba.wav' , 'rb')
	#fr = sound.getframerate()
	#nc = sound.getnchannels()
	#nf = sound.getnframes()
	#data = sound.readframes(nf)
	#sound.close()
	# testando a nossa funcao 'player' definida acima
	#player(data, nc, fr, nf)
	print "Isto e um modulo..."
