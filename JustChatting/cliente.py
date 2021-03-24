import threading
import socket

ip = input('Insira o IP: ')
nickname = input('Escolha um nickname: ')

cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cliente.connect((ip,25143))

def receive():
    while True:
        try:
            mensagem = cliente.recv(1024).decode('utf-8')
            if mensagem == 'NICK':
                cliente.send(nickname.encode('utf-8'))
            else:
                print(mensagem)
        except:
            print('Ocorreu um erro!')
            cliente.close()
            break

def write():
    while True:
        mensagem = f'{nickname}: {input("")}'
        cliente.send(mensagem.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()