# importa o método webdriver do módulo selenium
from selenium import webdriver

from selenium.webdriver.common.keys import Keys

# importa o método sleep do módulo time
from time import sleep

# importa o módulo random
import random

# declara classe
class InstaBot:

    # declara método construtor
    def __init__(self, usuario, senha):

        # declara variável com as opções do Google Chrome
        options = webdriver.ChromeOptions()
        
        # altera o idioma do Google Chrome para Português
        options.add_argument("--lang=pt")
        
        # abre o navegador com as definições de idioma
        self.driver = webdriver.Chrome(r"chromedriver.exe", chrome_options=options)

        # maximiza a janela do navegador
        self.driver.maximize_window()

        # declara variáveis de nome de usuário e senha
        self.usuario = usuario
        self.senha = senha

    # declara método de login
    def login(self):

        # acessa o endereço do Instagram
        self.driver.get("https://instagram.com")

        # faz uma pausa de dois segundos (para terminar de carregar a página)
        sleep(2)

        # encontra o input do nome de usuário na página e insere a variável usuario
        self.driver.find_element_by_xpath("//input[@name=\'username\']")\
            .send_keys(self.usuario)
        
        # encontra o input de senha e insere a variável senha
        self.driver.find_element_by_xpath("//input[@name=\'password\']")\
            .send_keys(self.senha)
        
        # encontra o botão de Log In e clica nele
        self.driver.find_element_by_xpath("//button[@type='submit']")\
            .click()
        
        # faz uma pausa de quatro segundos (para terminar de carregar a página)
        sleep(4)

    # declara método para capturar lista de seguidos
    def capturar_seguidos(self):
        
        # acessa o endereço do perfil
        self.driver.get('https://www.instagram.com/'+self.usuario)
        
        ### esta é uma outra maneira de chegar ao mesmo resultado navegando pela página
        #
        ### encontra o botão "Agora não" para salvar informações de login e clica nele
        # self.driver.find_element_by_xpath("//button[contains(text(), 'Agora Não')]")\
        #     .click()
        #
        ### faz uma pausa de dois segundos (para terminar de carregar a página)
        # sleep(2)
        #
        ### encontra o botão "Agora não" para ativar notificações e clica nele
        # self.driver.find_element_by_xpath("//button[contains(text(), 'Agora Não')]")\
        #     .click()
        #
        ### faz uma pausa de dois segundos (para terminar de carregar a página)
        # sleep(2)
        #
        ### encontra o link para o seu perfil e clica nele
        # self.driver.find_element_by_xpath("//a[contains(@href,'/{}/')]".format(self.usuario))\
        #     .click()

        # faz uma pausa de dois segundos (para terminar de carregar a página)
        sleep(2)
        
        # encontra o link de pessoas que nosso perfil está seguindo e clica nele
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()
        
        # declara uma variável para armazenar o resultado do método "capturar_nomes_usuarios" (que é uma lista com o nome de todas as pessoas seguidas por nosso perfil)
        seguindo = self.capturar_nomes_usuarios()

        # método retorna lista de seguidos
        return seguindo

    # declara método para capturar lista de seguidores
    def capturar_seguidores(self):
        
        # acessa o endereço do perfil
        self.driver.get('https://www.instagram.com/'+self.usuario)
        
        # faz uma pausa de dois segundos (para terminar de carregar a página)
        sleep(2)
        
        # encontra o link de pessoas que seguem nosso perfil e clica nele
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        
        # declara uma variável para armazenar o resultado do método "capturar_nomes_usuarios" (que é uma lista com o nome de todas as pessoas que seguem nosso perfil)
        seguidores = self.capturar_nomes_usuarios()

        # método retorna lista de seguidores
        return seguidores

    # declara método para buscar quem nosso perfil segue e não o segue
    def identificar_unfollowers(self):

        # declara lista de seguidos
        seguindo = self.capturar_seguidos()

        # declara lista de seguidores
        seguidores = self.capturar_seguidores()

        # declara lista para armazenar os usuários que nosso perfil segue, mas que não seguem nosso perfil
        nao_te_segue = [user for user in seguindo if user not in seguidores]
        
        # imprime na tela os usuários que nosso perfil segue, mas que não seguem nosso perfil
        print("Galera que não te segue: ", nao_te_segue)

        # cria e abre um arquivo ".txt" com permissão de escrita
        with open(self.usuario + '.txt', 'w') as f:
            
            # inicia loop para incluir no arquivo ".txt" todos os perfis que nosso perfil segue, mas que não seguem nosso perfil
            for nome in nao_te_segue:
                
                # escreve o nome do perfil no arquivo ".txt" com o nome do nosso perfil
                f.write("%s\n" % nome)
            
            # fecha o arquivo ".txt" ao finalizar o loop
            f.close()
        
        # retorna lista com nomes de usuário que nosso perfil segue, mas que não seguem nosso perfil
        return nao_te_segue

    # declara método para capturar os nomes de usuário
    def capturar_nomes_usuarios(self):
        
        # faz uma pausa de dois segundos (para terminar de carregar a página)
        sleep(2)
        
        # declara uma variável para armazenar XPath da div que contém o scroll
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")

        # realiza a rolagem da div de seguidos ou de seguidores
        self.scroll()
        
        # declara uma variável para armazenar o resultado da busca pelas tags "a" que contém o nome dos perfis que nosso perfil segue, mas que não seguem nosso perfil
        links = scroll_box.find_elements_by_tag_name("a")
        
        # declara uma variável para armazenar o resultado de um loop para ober a lista dos nomes dos perfis que nosso perfil segue, mas que não seguem nosso perfil
        nomes = [name.text for name in links if name.text != ""]
        
        # encontra o botão para fechar a janela e clica nele
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button")\
            .click()
        
        # retorna lista com nomes de usuário
        return nomes

    # declara método para rolar toda a div de seguidos ou seguidores (como forma de agilizar os processos de busca de usuários)
    def scroll(self):

        # faz uma pausa de um segundo (para terminar de carregar a página)        
        sleep(1)

        # declara uma variável para armazenar XPath da div que contém o scroll
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        
        # declara variáveis de controle para o loop
        last_ht, ht = 0, 1
        
        # inicia loop para dar scroll na div que contém os perfis
        while last_ht != ht:
            
            # altera variável de controle
            last_ht = ht
            
            # faz uma pausa de um segundo (para terminar de carregar a página)
            sleep(1)
            
            # altera variável de controle e executa script para mover o scroll até o final da div
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)

    # declara método para deixar de seguir os perfis que nosso perfil segue, mas que não seguem nosso perfil
    def unfollow_unfollowers(self):

        # abre um arquivo ".txt" com permissão de atualização
        with open(self.usuario + '.txt', 'r') as f:
            
            # armazena o conteúdo do arquivo ".txt" em uma lista, usando rsstrip() para retirar a quebra (\n) do final dos elementos do arquivo
            unfollow_essa_galera = [line.rstrip() for line in f]

            # fecha o arquivo ".txt" ao finalizar o loop
            f.close()
  
        # impõe condição para continuar a execução (ter algum nome de usuário na lista)
        if len(unfollow_essa_galera) > 0:

            # imprime mensagem na tela
            print("Iniciando unfollow...")
            
            # acessa o endereço do perfil
            self.driver.get('https://www.instagram.com/'+self.usuario)
            
            # faz uma pausa de dois segundos (para terminar de carregar a página)
            sleep(2)

            # encontra o link de pessoas que nosso perfil está seguindo e clica nele
            self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
                .click()

            # faz uma pausa de dois segundos (para terminar de carregar a página)
            sleep(2)
            
            # realiza a rolagem da div de seguidos
            self.scroll()

            # variável de controle para loop "while"
            rep = 0

            # inicia loop para repetir a ação pelas próximas 9 horas
            while rep < 10:

                # variável de controle para loop "for"
                i = 0

                # inicia loop para dar unfollow nos perfis da lista limitado a 8 perfis
                for user in unfollow_essa_galera:
                    
                    # faz uma pausa de dois segundos (para terminar de carregar a página)
                    sleep(2)
                    
                    # encontra o nome do perfil da lista
                    elemento = self.driver.find_element_by_xpath("//a[contains(@href,'/{}/')]".format(user))
                    
                    # move o scroll até o nome do perfil da lista para que fique visível na tela
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
                    
                    # faz uma pausa de dois segundos (para terminar de carregar a página)
                    sleep(2)

                    # imprime mensagem na tela
                    print(i, "- Encontrei o usuário", user)
                    
                    # encontra o botão "Seguindo" e clica nele para dar unfollow
                    elemento.find_element_by_xpath("./following::button[contains(text(), 'Seguindo')]")\
                        .click()
                    
                    # faz uma pausa de dois segundos (para terminar de carregar a página)
                    sleep(2)
                    
                    # encontra o botão "Deixar de seguir" e clica nele
                    self.driver.find_element_by_xpath("//button[contains(text(), 'Deixar de seguir')]")\
                        .click()
                    
                    # imprime mensagem na tela
                    print(i, "- Dei unfollow em", user)

                    unfollow_essa_galera.remove(user)

                    # faz uma pausa de um a dois segundos aleatoriamente para quebrar o padrão e deixar o ato de unfollow um pouco menos robótico
                    sleep(random.randint(1, 2))

                    # incrementa variável de controle
                    i += 1
                    
                    # condição para finalizar o loop
                    if i == 8:
                        break
                
                # incrementa variável de controle
                rep += 1

                # abre um arquivo ".txt" com permissão de atualização
                with open(self.usuario + '.txt', 'w+') as f:

                    # inicia loop para incluir no arquivo ".txt" todos os perfis que nosso perfil segue, mas que não seguem nosso perfil
                    for nome in unfollow_essa_galera:
                        
                        # escreve o nome do perfil no arquivo ".txt" com o nome do nosso perfil
                        f.write("%s\n" % nome)

                    # fecha o arquivo ".txt" ao finalizar o loop
                    f.close()

                # faz uma pausa de uma hora e dois minutos para iniciar novamente
                sleep(3720)
            
            # encontra o botão para fechar a janela e clica nele
            self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button")\
                .click()
        
            # imprime mensagem na tela
            print("Chega de unfollow por hoje!")

        # caso condição imposta não seja verdadeira
        else:

            # imprime mensagem na tela
            print("Ninguém para dar unfollow!")

# inicia o bot inserindo nome de usuário e senha
bot = InstaBot("USUARIO", "SENHA")

# executa método para fazer login na conta
bot.login()

# executa método para buscar os perfis que nosso perfil segue, mas que não seguem nosso perfil
bot.identificar_unfollowers()

# executa método para deixar de seguir os perfis que nosso perfil segue, mas que não seguem nosso perfil
bot.unfollow_unfollowers()