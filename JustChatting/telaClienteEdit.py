import PySimpleGUI as sg


class layout:
    def __init__(self):
        sg.theme = sg.theme_background_color("#1C1C1C")

        layoutLogin = [
            [sg.Text('NickName:', size=(10, 1), background_color="#1C1C1C")],
            [sg.Multiline(key='nick', size=(10, 1),
                          enter_submits=False, do_not_clear=False, border_width=False, autoscroll=True, no_scrollbar=True, auto_size_text=True, background_color="#363636", text_color="#DCDCDC"), sg.Button('Login', button_color="#1C1C1C", key='EnviarLogin')]
        ]
        self.login = sg.Window(
            'Login', layoutLogin)

        layoutBase = [
            [sg.Text('Chat', size=(10, 1), background_color="#1C1C1C")],
            [sg.Multiline(size=(50, 30), background_color="#363636",
                          text_color="#DCDCDC", disabled=True, border_width=False, reroute_stdout=True, no_scrollbar=True, autoscroll=True)],
            [sg.Multiline(key='mensagem', size=(41, 3),
                          enter_submits=False, do_not_clear=False, border_width=False, autoscroll=True, no_scrollbar=True, auto_size_text=True, background_color="#363636", text_color="#DCDCDC"), sg.Button('', button_color="#1C1C1C", key='Enviar', border_width=False, image_filename="./images/enviar1.png")]
        ]

        self.janela = sg.Window(
            'APS', layoutBase, enable_close_attempted_event=True)

    def Iniciar(self):
        nick = f'{self.IniciarLogin()}'
        nick = nick.replace("\n", "")
        while True:
            evento, valores = self.janela.read()
            if (evento == sg.WINDOW_CLOSE_ATTEMPTED_EVENT) and sg.popup_yes_no('Certeza que deseja sair?', background_color="#1C1C1C") == 'Yes':
                break
            if evento == 'Enviar':
                inputMsg = self.enviar_mensagem(valores)
                mensagem = f"{nick}:\n{inputMsg}"
                print(mensagem)

    def IniciarLogin(self):
        eventoLogin, valoresLogin = self.login.read()
        if eventoLogin == "EnviarLogin":
            return valoresLogin['nick']
        self.login.close()

    def enviar_mensagem(self, valores):
        return valores['mensagem']


gen = layout()
gen.Iniciar()
