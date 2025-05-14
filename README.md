
# 🚀 Projeto de Controle de Velocidade com Interface Flet (MVC + SQLite + Bluetooth)

Este projeto é uma aplicação de controle de velocidade com interface gráfica feita em [Flet](https://flet.dev), utilizando padrão **MVC**, banco de dados **SQLite**, e comunicação com módulo **Bluetooth HC-05** (ou similar).

---

## 🧩 Estrutura do Projeto

```
project/
├── main.py                     # Ponto de entrada da aplicação
├── models/
│   ├── user_model.py           # Acesso ao banco para usuários
│   └── speed_model.py          # Acesso ao banco para histórico de velocidades
├── controllers/
│   ├── user_controller.py      # Lógica de login e cadastro
│   └── speed_controller.py     # Lógica de registro e listagem de velocidades
├── database.db                 # Banco de dados SQLite (criado automaticamente)
└── README.md                   # Documentação
```

---

## 📦 Dependências

Instale as bibliotecas necessárias com:

```bash
pip install flet pyserial
```

---

## ⚙️ Como Rodar

1. **Clone ou baixe o repositório**
2. **Execute o arquivo principal:**

```bash
python main.py
```

3. A interface será aberta com tela de **login/cadastro** e navegação para:
   - **Início:** Confirmação de login
   - **Speed:** Controle e envio da velocidade via Bluetooth
   - **Perfil:** Histórico das velocidades usadas

---

## 🧠 Funcionalidades

- Login e cadastro de usuários com persistência via SQLite
- Envio de velocidade para dispositivos Bluetooth (ex: HC-05)
- Registro de histórico de velocidades por usuário
- Navegação intuitiva com abas
- Estrutura em camadas (MVC)

---

## 🔌 Conexão Bluetooth

O app tenta se conectar automaticamente a dispositivos com nome ou descrição `HC-05` ou `Bluetooth`. Verifique:

- O módulo HC-05 está pareado com seu computador
- A porta COM esteja disponível
- Baudrate padrão: `9600`

---

## 🧱 Banco de Dados

As tabelas são criadas automaticamente no arquivo `database.db`:

- **user(id, login, senha, created_at)**
- **speed(id, speed, created_at, id_user)**

---

## 📋 Licença

Este projeto é livre para uso educacional e pessoal.

---

## 🙋‍♂️ Autor

Desenvolvido com ❤️ usando Flet + Python 3.
