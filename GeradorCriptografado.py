import customtkinter as ct
import secrets
import string
from cryptography.fernet import Fernet

# Carregando a chave de criptografia do arquivo/caso não haja arquivo,ira criar um.
try:
    with open("chave.key", "rb") as chave_arquivo:
        chave = chave_arquivo.read()
except FileNotFoundError:
    chave = Fernet.generate_key()
    with open("chave.key", "wb") as chave_arquivo:
        chave_arquivo.write(chave)

fernet = Fernet(chave)

# Função para gerar senha.
def gerarsenha():
    itens = string.ascii_letters + string.digits
    senha = ''.join(secrets.choice(itens) for i in range(int(menu_opcoes.get())))
    textbox_senhanova.delete(index1="1.0", index2="end")
    textbox_senhanova.insert(index="1.0", text=senha)

    site_aplicativo = entry_site.get()
    login = entry_login.get()

    if not site_aplicativo or not login:
        textbox_senhanova.delete(index1="1.0", index2="end")
        textbox_senhanova.insert(index="1.0", text="Preencha todos os campos.")
        return

    dados = f"Site/App: {site_aplicativo}\nLogin: {login}\nSenha: {senha}\n\n"
    dados_criptografados = fernet.encrypt(dados.encode())

    with open("dados_armazenados_criptografados.txt", "ab") as arquivo:
        arquivo.write(dados_criptografados + b"\n")

# Função para excluir senha
def excluir_senha(linha_excluir):
    with open("dados_armazenados_criptografados.txt", "rb") as arquivo:
        linhas = arquivo.readlines()

    with open("dados_armazenados_criptografados.txt", "wb") as arquivo:
        for i, linha in enumerate(linhas):
            if i != linha_excluir:
                arquivo.write(linha)

    # Atualiza a visualização após a exclusão
    visualizar_senhas()

# Função para visualizar senhas
def visualizar_senhas():
    with open("dados_armazenados_criptografados.txt", "rb") as arquivo:
        linhas = arquivo.readlines()

    dados_descriptografados = [fernet.decrypt(linha).decode() for linha in linhas]

    janela_senhas = ct.CTkToplevel(janela)
    janela_senhas.title("Dados Armazenados")
    janela_senhas.geometry("400x450")

    for i, dado in enumerate(dados_descriptografados):
        frame = ct.CTkFrame(janela_senhas)
        frame.pack(fill="x", padx=10, pady=5)

        label = ct.CTkLabel(frame, text=dado)
        label.pack(side="left", fill="x", expand=True)

        botao_excluir = ct.CTkButton(frame, text="Excluir", command=lambda i=i: excluir_senha(i))
        botao_excluir.pack(side="right")

# Configuração da interface
ct.set_appearance_mode("System")
ct.set_default_color_theme("dark-blue")

janela = ct.CTk()
janela.title("PASSWORD GENERATOR")
janela.resizable(False, False)
janela.geometry("400x450")
janela.iconbitmap('padlock.ico')


tabview = ct.CTkTabview(janela, width=400, height=360)
tabview.grid()
tabview.add("GERADOR DE SENHAS")
tabview.tab("GERADOR DE SENHAS").grid_columnconfigure([0, 1], weight=1)

label_site = ct.CTkLabel(tabview.tab("GERADOR DE SENHAS"), text="Site/App")
label_site.grid(row=0, column=0, padx=10, pady=5, sticky="w")

entry_site = ct.CTkEntry(tabview.tab("GERADOR DE SENHAS"))
entry_site.grid(row=0, column=1, padx=10, pady=5)

label_login = ct.CTkLabel(tabview.tab("GERADOR DE SENHAS"), text="Login")
label_login.grid(row=1, column=0, padx=10, pady=5, sticky="w")

entry_login = ct.CTkEntry(tabview.tab("GERADOR DE SENHAS"))
entry_login.grid(row=1, column=1, padx=10, pady=5)

label_texto1 = ct.CTkLabel(tabview.tab("GERADOR DE SENHAS"), text="Quantidade de Caracteres")
label_texto1.grid(row=2, column=0, padx=10, pady=5, sticky="w")

valores = [str(i) for i in range(1, 26)]
menu_opcoes = ct.CTkOptionMenu(tabview.tab("GERADOR DE SENHAS"), values=valores)
menu_opcoes.grid(row=2, column=1, padx=10, pady=5)

botao_gerarsenha = ct.CTkButton(tabview.tab("GERADOR DE SENHAS"), text="GERAR SENHA", command=gerarsenha)
botao_gerarsenha.grid(row=3, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)

label_senhagerada = ct.CTkLabel(tabview.tab("GERADOR DE SENHAS"), text="Senha Gerada")
label_senhagerada.grid(row=4, column=0, padx=10, pady=5, sticky="w", columnspan=2)

textbox_senhanova = ct.CTkTextbox(tabview.tab("GERADOR DE SENHAS"), width=280, height=50)
textbox_senhanova.grid(row=5, column=0, padx=10, pady=5, sticky='nsew', columnspan=2)

botao_visualizar = ct.CTkButton(tabview.tab("GERADOR DE SENHAS"), text="VISUALIZAR DADOS", command=visualizar_senhas)
botao_visualizar.grid(row=6, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)

janela.mainloop()
