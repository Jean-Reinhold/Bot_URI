from selenium import webdriver
import numpy as np

class Uri_bot: 
    def __init__(self):
        self.webdriver = webdriver.Chrome()
    
        #Le ids de todos os alunos 
        with open('competidores_id.txt', "r") as leitor: 
            self.ids_competidores = leitor.read()
            self.ids_competidores = self.ids_competidores.split('\n')
        self.url_URI = "https://www.urionlinejudge.com.br/judge/pt/profile/"

    def get_competidores_data(self): 
        self.dados_competidores = list()

        for id_competidor in self.ids_competidores: 
            self.webdriver.get(self.url_URI + id_competidor)
            self.webdriver.implicitly_wait(2)  

            nome_competidor = self.webdriver.find_element_by_xpath('//*[@id="profile-bar"]/div[3]/p/a').text
            pontos = self.webdriver.find_element_by_xpath('//*[@id="profile-bar"]/ul/li[5]').text
            resolvidos = self.webdriver.find_element_by_xpath('//*[@id="profile-bar"]/ul/li[6]').text
            tentados = self.webdriver.find_element_by_xpath('//*[@id="profile-bar"]/ul/li[7]').text
            submisoes = self.webdriver.find_element_by_xpath('//*[@id="profile-bar"]/ul/li[8]').text

            lista_competidor = [nome_competidor, pontos[8:], int(resolvidos[11:]), int(tentados[9:]), int(submisoes[12:])]
            self.dados_competidores.append(lista_competidor)

    def salvar_original(self, path): 
        with open(path, "w") as arquivo: 
            for competidor in self.dados_competidores: 
                arquivo.write("Nome: {}; Pontos: {}; Resolvidos: {}; Tentados: {}; Submissões".format
                         (competidor[0], competidor[1], competidor[2], competidor[3], competidor[4])) 
                arquivo.write("\n")
            arquivo.close 

    def salvar_sortido_resolvidos(self, path):  
        resolvidos = list()
        for pontuacao in self.dados_competidores: 
            resolvidos.append(pontuacao[2])

        enderecos_organizados = np.argsort(resolvidos)
        enderecos_organizados = enderecos_organizados[::-1]

        with open(path, "w") as arquivo: 
            for endereço in enderecos_organizados: 
                arquivo.write("Nome: {}; Pontos: {}; Resolvidos: {}; Tentados: {}; Submissões".format
                         (self.dados_competidores[endereço][0], self.dados_competidores[endereço][1], self.dados_competidores[endereço][2],
                         self.dados_competidores[endereço][3], self.dados_competidores[endereço][4])) 
                arquivo.write("\n")
            arquivo.close 

bot = Uri_bot()
bot.get_competidores_data()
bot.salvar_sortido_resolvidos("ranking/OrdemResolvidos.txt")
bot.salvar_original("ranking/OrdemAleatoria.txt")