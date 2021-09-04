#Para rodar o teste de stress na máquina:
#curl -o stress.rpm ftp://fr2.rpmfind.net/linux/dag/redhat/el7/en/x86_64/dag/RPMS/stress-1.0.2-1.el7.rf.x86_64.rpm
#sudo yum install stress.rpm
#stress -c 2 -i 1 -m 1 --vm-bytes 128M -t 10s

#TODO: liberar recursos quando diminuir a carga da rede
#TODO: não adianta uma máquina estar exaurida e a outra estar livre usando round robin
#TODO: no ciclo que uma máquina nova está subindo ele pode subir outra instância, tem que dar um jeito de aguardar
#TODO: corrigir output do CURL e do iniciar_instancia.sh (não deve aparecer)
#TODO: salvar diagnósticos para aplicar Machine Learning

import os
import time

nomeProcurado = "eredes32_33"
usoMaximoCPU = 0.8
usoMaximoMemoria = 0.8

def listaIPInstancias(nomeInstancia):
	listaIP = []
	stream = os.popen("openstack server list")
	output = stream.read()
	linhas = output.split("\n")
	for linha in linhas:
		campos = linha.split("|")
		#Para mostrar os campos e indices
		#for iCampo in range(len(campos)):
		#	valor = campos[iCampo]	
		#	print('%s-%s' %(iCampo, valor))
		#print ('\n');
		if (len(campos) == 8):
			nomeInstancia = campos[2]
			linhaIP = campos[4]
			#print (nomeInstancia)
			if nomeInstancia.find(nomeProcurado) > -1:
				camposLinhaIP = linhaIP.split("=")
				rede = camposLinhaIP[0]
				camposIP = camposLinhaIP[1].split(",")
				ip6 = camposIP[0].strip()
				ip4 = camposIP[1].strip()
				#print(ip4)
				listaIP.append(ip4)
	return listaIP


def maquinaSaudavel(ip):

	percentualMemoriaDisponivel = 0
	cpu = 0

	url = ip + "/diagnostico.php"
	comando = "curl " + url
	stream = os.popen(comando)
        output = stream.read()
        linhas = output.split("\n")
	for linha in linhas:
		#print (linha)
		if (linha.find("Percentual") > -1):
			percentualMemoriaDisponivel = linha.split(": ")[1]
		elif (linha.find("CPU") > -1):
			cpu = linha.split(": ")[1].split("-")[0]
	
	print ('Percentual Memoria Disponivel: %s' % percentualMemoriaDisponivel)
	print ('Uso de CPU instantaneo: %s' % cpu)

	percentualMemoriaUtilizada = 1 - float(percentualMemoriaDisponivel)
	if (float(cpu) > usoMaximoCPU) or (float(percentualMemoriaUtilizada) > usoMaximoMemoria):
		return False
	else:
		return True

def redeSaudavel():
	listaIP = listaIPInstancias(nomeProcurado)
	qtdMaquinasSaudaveis = len(listaIP)

	for ip in listaIP:
		resultado = maquinaSaudavel(ip)
		if (not resultado):
			print ("ATENCAO: a maquina %s nao esta saudavel!" % ip)		
			qtdMaquinasSaudaveis -= 1

	#Caso nao existam maquinas saudaveis na rede
	if qtdMaquinasSaudaveis == 0:
		return False
	else:
		return True

def criarInstancia():
	print ("********************* CRIANDO UMA NOVA INSTANCIA NA REDE")
	os.system('./iniciar_instancia_2.sh')

try:
	while True:
		if not redeSaudavel():
			print ("A REDE NAO ESTA SAUDAVEL!!!!")
			criarInstancia()
		time.sleep(10)
except KeyboardInterrupt:
	print ('Programa finalizado pelo usuario')

