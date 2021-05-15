import threading
import socket
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

host = input('Insira o IP: ')
port = 3001
# host = 'localhost'
# port = 3001

class Cliente:
    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((host,port))

        mensagem = tkinter.Tk()
        mensagem.withdraw()

        self.nickname = simpledialog.askstring('Nickaname','Escolha um nickname',parent=mensagem)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg='#1C1C1C')

        self.lblChat = tkinter.Label(self.win, text='Chat:', bg='#1C1C1C')
        self.lblChat.config(font=('Arial',12), fg='white')
        self.lblChat.pack(padx=20,pady=5)

        self.txtHistorico = tkinter.scrolledtext.ScrolledText(self.win, bg='#363636', fg='white')
        self.txtHistorico.pack(padx=20,pady=5)
        self.txtHistorico.config(state='disabled')

        self.lblMensagem = tkinter.Label(self.win, text='Menssagem:', bg='#1C1C1C')
        self.lblMensagem.config(font=('Arial',12), fg='white')
        self.lblMensagem.pack(padx=20,pady=5)

        self.txtMensagem = tkinter.Text(self.win, height=3, bg='#363636', fg='white')
        self.txtMensagem.pack(padx=20, pady=5)

        self.btnEnviar = tkinter.Button(self.win, text='Enviar', bg='#1C1C1C', fg='white', command=self.write)
        self.btnEnviar.config(font=('Arial',12))
        self.btnEnviar.pack(padx=20,pady=5)

        self.gui_done = True
        self.win.protocol('WM_DELETE_WINDOW',self.stop)

        self.win.mainloop()

    def write(self):
        mensagem = f"{self.nickname}: {self.txtMensagem.get('1.0','end')}"
        self.sock.send(mensagem.encode('utf-8'))
        self.txtMensagem.delete('1.0','end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                mensagem = self.sock.recv(1024).decode('utf-8')
                if mensagem == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.txtHistorico.config(state='normal')
                        self.txtHistorico.insert('end',mensagem)
                        self.txtHistorico.yview('end')
                        self.txtHistorico.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print('Erro')
                self.sock.close()
                break

cliente = Cliente(host,port)