# Gerador de Senhas com Armazenamento Seguro

Este projeto é uma aplicação de interface gráfica que gera senhas aleatórias e armazena essas senhas de forma segura em um arquivo criptografado. A interface foi desenvolvida utilizando o `customtkinter`, uma biblioteca que permite a criação de GUIs modernas e personalizadas para Python.

## Funcionalidades

- **Geração de Senhas:** Gera senhas aleatórias de acordo com o número de caracteres definido pelo usuário.
- **Armazenamento Seguro:** As senhas geradas, juntamente com as informações do site/aplicativo e login, são armazenadas de forma criptografada em um arquivo local.
- **Visualização de Senhas:** Permite ao usuário visualizar as senhas armazenadas de forma segura.
- **Exclusão de Senhas:** Oferece a funcionalidade de excluir senhas previamente armazenadas.

## Tecnologias Utilizadas

- **Python:** Linguagem de programação utilizada para desenvolvimento do projeto.
- **customtkinter:** Biblioteca utilizada para criar a interface gráfica.
- **cryptography (Fernet):** Utilizada para criptografia e decriptografia dos dados armazenados.

## Como Funciona

### Carregamento da Chave de Criptografia

O programa tenta carregar uma chave de criptografia de um arquivo chamado `chave.key`. Caso o arquivo não exista, uma nova chave é gerada e armazenada neste arquivo para uso futuro.

```python
try:
    with open("chave.key", "rb") as chave_arquivo:
        chave = chave_arquivo.read()
except FileNotFoundError:
    chave = Fernet.generate_key()
    with open("chave.key", "wb") as chave_arquivo:
        chave_arquivo.write(chave)

fernet = Fernet(chave)
```

### Geração de Senha

O usuário pode gerar uma senha selecionando o número de caracteres desejado. A senha gerada é exibida na interface e armazenada juntamente com o nome do site/aplicativo e o login fornecido.

```python
def gerarsenha():
    itens = string.ascii_letters + string.digits
    senha = ''.join(secrets.choice(itens) for i in range(int(menu_opcoes.get())))
    # [continua...]
```

### Armazenamento Seguro

As informações geradas (site/aplicativo, login e senha) são criptografadas e armazenadas em um arquivo chamado `dados_armazenados_criptografados.txt`.

```python
dados_criptografados = fernet.encrypt(dados.encode())
with open("dados_armazenados_criptografados.txt", "ab") as arquivo:
    arquivo.write(dados_criptografados + b"\n")
```

### Visualização e Exclusão de Senhas

O usuário pode visualizar as senhas armazenadas e, se desejar, excluir entradas específicas. As senhas são descriptografadas antes de serem exibidas.

```python
def visualizar_senhas():
    with open("dados_armazenados_criptografados.txt", "rb") as arquivo:
        linhas = arquivo.readlines()

    dados_descriptografados = [fernet.decrypt(linha).decode() for linha in linhas]

    # [continua...]
```

## Interface Gráfica

A interface gráfica foi desenvolvida utilizando a biblioteca `customtkinter`. O layout é composto por uma janela principal com abas que permitem ao usuário gerar senhas e visualizar os dados armazenados.

## Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Tiagolsilva/Gerador-de-Senhas-Criptografado.git
   ```

2. **Instale as dependências:**
   Certifique-se de que você tenha o Python instalado. Em seguida, instale as bibliotecas necessárias:
   ```bash
   pip install customtkinter
   pip install cryptography
   ```

3. **Execute o script:**
   ```bash
   python nome_do_arquivo.py
   ```

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.
