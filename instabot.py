# importa o método webdriver do módulo selenium
from selenium import webdriver

# importa o método sleep do módulo time
from time import sleep

# importa o módulo random
import random

# declara variáveis de nome de usuário e senha
username = ""
password = ""

# declara classe
class InstaBot:

    # declara método construtor
    def __init__(self):

        # abre o navegador
        self.driver = webdriver.Chrome(r"chromedriver.exe")

        # maximiza a janela do navegador
        self.driver.maximize_window()

        # acessa o endereço do Instagram
        self.driver.get("https://instagram.com")

        # faz uma pausa de dois segundos (para terminar de carregar a página)
        sleep(2)

        # encontra o input do nome de usuário na página e insere a variável username
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        
        # encontra o input de senha e insere a variável password
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(password)
        
        # encontra o botão de Log In e clica nele
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        
        # faz uma pausa de quatro segundos (para terminar de carregar a página)
        sleep(4)
        
        # encontra o botão "Agora não" para salvar informações de login e clica nele
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        
        # faz uma pausa de dois segundos (para terminar de carregar a página)
        sleep(2)

        # encontra o botão "Agora não" para ativar notificações e clica nele
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        
        # faz uma pausa de dois segundos (para terminar de carregar a página)
        sleep(2)

    # declara método para buscar quem nosso perfil segue e não o segue
    def buscar_unfollowers(self):
        
        # encontra o link para o seu perfil e clica nele
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}/')]".format(username))\
            .click()
        
        # faz uma pausa de dois segundos (para terminar de carregar a página)
        sleep(2)
        
        # encontra o link de pessoas que nosso perfil está seguindo e clica nele
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()
        
        # declara uma variável para armazenar o resultado do método "_pegar_nomes" (que é uma lista com o nome de todas as pessoas seguidas por nosso perfil)
        seguindo = self._pegar_nomes()
        
        # encontra o link de pessoas que seguem nosso perfil e clica nele
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        
        # declara uma variável para armazenar o resultado do método "_pegar_nomes" (que é uma lista com o nome de todas as pessoas que seguem nosso perfil)
        seguidores = self._pegar_nomes()
        
        # declara uma variável para armazenar os usuários que nosso perfil segue, mas que não seguem nosso perfil
        not_following_back = [user for user in seguindo if user not in seguidores]
        
        # imprime na tela os usuários que nosso perfil segue, mas que não seguem nosso perfil
        print("Galera que não te segue: ", not_following_back)

        # cria e abre um arquivo "unfollow.txt" com permissão de escrita
        with open('unfollow.txt', 'w') as f:
            
            # inicia loop para incluir no arquivo "unfollow.txt" todos os perfis que nosso perfil segue, mas que não seguem nosso perfil
            for nome in not_following_back:
                
                # escreve o nome do perfil no arquivo "unfollow.txt"
                f.write("%s\n" % nome)
            
            # fecha o arquivo "unfollow.txt" ao finalizar o loop
            f.close()
        
        # retorna lista com nomes de usuário que nosso perfil segue, mas que não seguem nosso perfil
        return not_following_back

    # declara método para capturar os nomes de usuário
    def _pegar_nomes(self):
        
        # faz uma pausa de dois segundos (para terminar de carregar a página)
        sleep(2)
        
        # declara uma variável para armazenar XPath da div que contém o scroll
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
        
        # declara variáveis de controle para o loop
        last_ht, ht = 0, 1
        
        # inicia loop para dar scroll na div que contém os perfis
        while last_ht != ht:
            
            # altera variável de controle
            last_ht = ht
            
            # faz uma pausa de um segundo (para terminar de carregar a página)
            sleep(1)
            
            # altera variável de controle e executa javascript para mover o scroll até o final da div
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)
        
        # declara uma variável para armazenar o resultado da busca pelas tags "a" que contém o nome dos perfis que nosso perfil segue, mas que não seguem nosso perfil
        links = scroll_box.find_elements_by_tag_name("a")
        
        # declara uma variável para armazenar o resultado de um loop para ober a lista dos nomes dos perfis que nosso perfil segue, mas que não seguem nosso perfil
        nomes = [name.text for name in links if name.text != ""]
        
        # encontra o botão para fechar a janela e clica nele
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button")\
            .click()
        
        # retorna lista com nomes de usuário
        return nomes

    # declara método para deixar de seguir os perfis que nosso perfil segue, mas que não seguem nosso perfil
    def unfollow_unfollowers(self):

        # declara variável que armazena lista de perfis que nosso perfil segue, mas que não seguem nosso perfil, utilizando o resultado do método "buscar_unfollowers"
        unfollow_essa_galera = self.buscar_unfollowers()
        
        # impõe condição para continuar a execução (ter algum nome de usuário na lista)
        if len(unfollow_essa_galera) > 0:
            
            # imprime mensagem na tela
            print("Iniciando unfollow...")
            
            # encontra o link de pessoas que nosso perfil está seguindo e clica nele
            self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
                .click()

            # faz uma pausa de dois segundos (para terminar de carregar a página)
            sleep(2)
            
            # variável de controle para loop
            i = 0

            # inicia loop para dar unfollow nos perfis da lista limitado a 90 perfis
            for user in unfollow_essa_galera:
                
                # encontra o nome do perfil da lista
                elemento = self.driver.find_element_by_xpath("//a[contains(@href,'/{}/')]".format(user))
                
                # move o scroll até o nome do perfil da lista para que fique visível na tela
                self.driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
                
                # imprime mensagem na tela
                print("Encontrei o usuário")
                
                # encontra o botão "Seguindo" e clica nele para dar unfollow
                elemento.find_element_by_xpath("./following::button[contains(text(), 'Following')]")\
                    .click()
                
                # encontra o botão "Deixar de seguir" e clica nele
                self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]")\
                    .click()
                
                # imprime mensagem na tela
                print("Dei unfollow")

                # faz uma pausa de dois a quatro segundos aleatoriamente para quebrar o padrão e deixar o ato de unfollow menos robótico
                sleep(random.randint(2, 4))

                # incrementa variável de controle
                i += 1

                # condição para finalizar o loop
                if i == 90:
                    break
            
        # encontra o botão para fechar a janela e clica nele
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button")\
            .click()
        
        # imprime mensagem na tela
        print("Chega de unfollow por hoje!")

# executa método para deixar de seguir os perfis que nosso perfil segue, mas que não seguem nosso perfil
InstaBot().unfollow_unfollowers()