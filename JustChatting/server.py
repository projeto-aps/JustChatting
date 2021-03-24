import threading
import socket

host = 'localhost'
port = 3001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clientes = []
nicknames = []

def broadcast(mensagem):
    for cliente in clientes:
        cliente.send(mensagem)

def handle(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024)
            broadcast(mensagem)
        except:
            index = clientes.index(cliente)
            clientes.remove(cliente)
            cliente.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} saiu do chat!\n'.encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        cliente, endereco = server.accept()
        print(f'Conectado com {str(endereco)}')

        cliente.send('NICK'.encode('utf-8'))
        nickname = cliente.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clientes.append(cliente)

        print(f'Nickname do cliente é {nickname}')
        broadcast(f'{nickname} entrou no chat!\n'.encode('utf-8'))
        cliente.send('Conectado ao servidor!\n'.encode('utf-8'))

        thread = threading.Thread(target=handle,args=(cliente,))
        thread.start()

print('Servidor ativo...')
receive()