
import flet as ft
import serial
import serial.tools.list_ports

from controllers import user_controller, speed_controller
from models import user_model, speed_model

# Inicializa as tabelas
user_model.create_user_table()
speed_model.create_speed_table()

def main(page: ft.Page):
    page.title = "App MVC com SQLite"
    page.window_width = 400
    page.window_height = 600

    def mostrar_tela_login():
        page.views.clear()
        page.views.append(view_login)
        page.update()

    def mostrar_tela_cadastro():
        page.views.clear()
        page.views.append(view_cadastro)
        page.update()

    def mostrar_tela_home(user):
        velocidade = ft.Ref[ft.Slider]()
        conteudo = ft.Column()

        bt_serial = None
        conectado_bt = False
        status_bt = ft.Text("Bluetooth: Desconectado", color=ft.Colors.GREY)

        def on_nav_change(e):
            atualizar_conteudo_visivel()

        def conectar_bluetooth(e):
            nonlocal bt_serial, conectado_bt
            try:
                if not conectado_bt:
                    ports = serial.tools.list_ports.comports()
                    for port in ports:
                        if "HC-05" in port.description or "Bluetooth" in port.description:
                            bt_serial = serial.Serial(port.device, 9600, timeout=1)
                            conectado_bt = True
                            break
                    if conectado_bt:
                        status_bt.value = "Bluetooth: Conectado"
                        status_bt.color = ft.Colors.BLUE
                    else:
                        status_bt.value = "HC-05 não encontrado"
                        status_bt.color = ft.Colors.RED
                else:
                    if bt_serial:
                        bt_serial.close()
                    conectado_bt = False
                    status_bt.value = "Bluetooth: Desconectado"
                    status_bt.color = ft.Colors.GREY
            except Exception as ex:
                status_bt.value = f"Erro: {ex}"
                status_bt.color = ft.Colors.RED
            if status_bt.page:
                status_bt.update()


        def run_clicked(e):
            valor = int(velocidade.current.value)
            print(f"Velocidade selecionada: {valor}")
            user_id = user_controller.buscar_id_usuario(user)
            if user_id:
                speed_controller.registrar_velocidade(valor, user_id[0])

            if conectado_bt and bt_serial:
                try:
                    bt_serial.write(f"{valor}\n".encode())
                except Exception as ex:
                    status_bt.value = f"Erro ao enviar: {ex}"
                    status_bt.color = ft.Colors.RED
                    status_bt.update()

        def atualizar_conteudo_visivel():
            conteudo.controls.clear()
            idx = nav_bar.selected_index
            if idx == 0:
                conteudo.controls.append(ft.Text("Você está logado com sucesso!"))
            elif idx == 2:
                conteudo.controls.append(ft.Text(f"Perfil do usuário: {user}"))
                historico = speed_controller.obter_velocidades(user)
                if historico:
                    conteudo.controls.append(ft.Text("Velocidades usadas:"))
                    for i, (v, data) in enumerate(historico):
                        conteudo.controls.append(ft.Text(f"{i+1}º uso: {v} em {data}"))
                else:
                    conteudo.controls.append(ft.Text("Nenhum uso registrado ainda."))
            elif idx == 1:
                conteudo.controls.extend([
                    ft.Text("Velocidade:"),
                    ft.Slider(ref=velocidade, min=0, max=100, divisions=10, value=0),
                    ft.ElevatedButton("Run", on_click=run_clicked),
                    status_bt
                ])
            conteudo.update()

        nav_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Início"),
                ft.NavigationBarDestination(icon=ft.Icons.SPEED, label="Speed"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Perfil"),
            ],
            on_change=on_nav_change
        )

        page.views.clear()
        page.views.append(
            ft.View(
                "/home",
                controls=[
                    ft.AppBar(
                        title=ft.Text("Bem-vindo, " + user),
                        actions=[
                            ft.IconButton(
                                icon=ft.Icons.BLUETOOTH,
                                tooltip="Conectar Bluetooth",
                                on_click=conectar_bluetooth
                            )
                        ]
                    ),
                    conteudo,
                    nav_bar
                ]
            )
        )
        page.update()
        atualizar_conteudo_visivel()

    def login(e):
        user = user_login.value
        senha = senha_login.value
        if user_controller.autenticar_usuario(user, senha):
            mostrar_tela_home(user)
        else:
            msg_login.value = "Email ou senha inválidos."
            msg_login.update()

    def cadastrar(e):
        user = email_cadastro.value
        senha = senha_cadastro.value
        sucesso = user_controller.cadastrar_usuario(user, senha)
        if sucesso:
            msg_cadastro.value = "Cadastro realizado com sucesso!"
        else:
            msg_cadastro.value = "Usuário já existe."
        msg_cadastro.update()

    # View Login
    user_login = ft.TextField(label="Usuário")
    senha_login = ft.TextField(label="Senha", password=True)
    msg_login = ft.Text(value="", color=ft.Colors.RED)
    view_login = ft.View(
        "/login",
        [
            ft.Text("Login", size=30),
            user_login,
            senha_login,
            ft.ElevatedButton("Entrar", on_click=login),
            msg_login,
            ft.TextButton("Cadastrar", on_click=lambda _: mostrar_tela_cadastro())
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # View Cadastro
    email_cadastro = ft.TextField(label="Usuário")
    senha_cadastro = ft.TextField(label="Senha", password=True)
    msg_cadastro = ft.Text(value="", color=ft.Colors.GREEN)
    view_cadastro = ft.View(
        "/cadastro",
        [
            ft.Text("Cadastro", size=30),
            email_cadastro,
            senha_cadastro,
            ft.ElevatedButton("Cadastrar", on_click=cadastrar),
            msg_cadastro,
            ft.TextButton("Voltar ao Login", on_click=lambda _: mostrar_tela_login())
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    mostrar_tela_login()

ft.app(target=main)
