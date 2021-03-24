import threading
import socket

ip = input('Insira o IP: ')
nickname = input('Escolha um nickname: ')

cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cliente.connect((ip,3001))

def receive():
    while True:
        try:
            mensagem = cliente.recv(1024).decode('ascii')
            if mensagem == 'NICK':
                cliente.send(nickname.encode('ascii'))
            else:
                print(mensagem)
        except:
            print('Ocorreu um erro!')
            cliente.close()
            break

def write():
    while True:
        mensagem = f'{nickname}: {input("")}'
        cliente.send(mensagem.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()