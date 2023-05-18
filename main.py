from playwright.sync_api import sync_playwright
from time import sleep
import string
import random
import re
import matplotlib.pyplot as plt

def bot_pega_sentenca():
    # inicia a vairavel como uma string vazia
    texto_sentencas = ''

    with sync_playwright() as p:
        # abre um novo browser baseado no chromium
        browser = p.chromium.launch(headless=False)
        # abre uma nova pagina em branco no navegador que foi aberto
        page = browser.new_page()
        page.set_default_timeout(0)
        # redireciona a pagina aberta para o link passado
        page.goto('http://www4.tjrj.jus.br/ejuris/ConsultarJurisprudencia.aspx')
        page.wait_for_timeout(1000 +random.randint(0,3000))
        # Executa várias ações simulando uma pessoa navegando (clica, digita, pesquisa, seleciona opções e etc)
        page.locator('//*[@id="ContentPlaceHolder1_txtTextoPesq"]').click()
        page.wait_for_timeout(1000 +random.randint(0,3000))
        page.locator('//*[@id="ContentPlaceHolder1_txtTextoPesq"]').fill('homicidio ou assalto ou feminicidio ou trafico ou tortura ou terrorismo ou estupro')
        page.wait_for_timeout(1000 +random.randint(0,3000))
        page.locator('//*[@id="ContentPlaceHolder1_cmbAnoInicio"]').select_option(index=1)
        page.wait_for_timeout(1000 +random.randint(0,3000))
        page.locator('//*[@id="ContentPlaceHolder1_cmbAnoFim"]').select_option(index=1)
        page.wait_for_timeout(1000 +random.randint(0,3000))
        page.locator('//*[@id="ContentPlaceHolder1_cmbCompetencia"]').select_option(index=1)
        page.wait_for_timeout(1000 +random.randint(0,3000))
        page.locator('//*[@id="ContentPlaceHolder1_btnPesquisar"]').click()
        # um loop para pegar os 10 processos de cada página, no exemplo em questão estamos pegando 5 páginas, totalizando 50 sentenças
        for y in range(20):
            for x in range(10):
                # a variavel texto_sentencas vai concatenando o valor dela mesmo + o texto de cada sentença
                texto_sentencas += page.inner_text(f'//*[@id="placeholder"]/span/table/tbody/tr[6]/td/table[{x+1}]/tbody/tr[10]/td')
                texto_sentencas += ('\n--------------------------\n\n')
            # avança de pagina
            page.locator('//*[@id="avanca"]').click()
            page.wait_for_timeout(3000 +random.randint(1000,5000))
        #fecha o browser
        browser.close()

    # criamos um arquivo txt e escrevemos nele o conteúdo da variavel texto_sentencas
    arquivo_txt = open('sentencas.txt', 'w', encoding='UTF-8')
    arquivo_txt.write(texto_sentencas)
    arquivo_txt.close()


def main():
    #bot_pega_sentenca()
    # iniciamos uma lista vazia e uma lista com stop words que iremos remover
    palavras_sem_lixo = []
    palavras_lixo = ['33', '1134306', 'a', 'à', 'adeus', 'agora', 'aí', 'ainda', 'além', 'algo', 'alguém', 'algum', 'alguma', 'algumas', 'alguns', 'ali', 'ampla', 'amplas', 'amplo', 'amplos', 'ano', 'anos', 'ante', 'antes', 'ao', 'aos', 'apenas', 'apoio', 'após', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aqui', 'aquilo', 'área', 'as', 'às', 'assim', 'até', 'atrás', 'através', 'baixo', 'bastante', 'bem', 'boa', 'boas', 'bom', 'bons', 'breve', 'cá', 'cada', 'catorze', 'cedo', 'cento', 'certamente', 'certeza', 'cima', 'cinco', 'coisa', 'coisas', 'com', 'como', 'conselho', 'contra', 'contudo', 'custa', 'da', 'dá', 'dão', 'daquela', 'daquelas', 'daquele', 'daqueles', 'dar', 'das', 'de', 'debaixo', 'dela', 'delas', 'dele', 'deles', 'demais', 'dentro', 'depois', 'desde', 'dessa', 'dessas', 'desse', 'desses', 'desta', 'destas', 'deste', 'destes', 'deve', 'devem', 'devendo', 'dever', 'deverá', 'deverão', 'deveria', 'deveriam', 'devia', 'deviam', 'dez', 'dezanove', 'dezasseis', 'dezassete', 'dezoito', 'dia', 'diante', 'disse', 'disso', 'disto', 'dito', 'diz', 'dizem', 'dizer', 'do', 'dois', 'dos', 'doze', 'duas', 'dúvida', 'e', 'é', 'ela', 'elas', 'ele', 'eles', 'decisão','em', 'embora', 'enquanto', 'entre', 'era', 'eram', 'éramos', 'és', 'r', 'essa', 'essas', 'esse', 'esses', 'esta', 'está', 'estamos', 'estão', 'estar', 'estas', 'estás', 'estava', 'estavam', 'estávamos', 'este', 'esteja', 'estejam', 'estejamos', 'estes', 'esteve', 'estive', 'estivemos', 'estiver', 'estivera', 'estiveram', 'estivéramos', 'estiverem', 'estivermos', 'estivesse', 'estivessem', 'estivéssemos', 'estiveste', 'estivestes', 'estou', 'etc', 'eu', 'exemplo', 'faço', 'falta', 'favor', 'faz', 'fazeis', 'fazem', 'fazemos', 'fazendo', 'fazer', 'fazes', 'feita', 'feitas', 'feito', 'feitos', 'fez', 'fim', 'final', 'foi', 'fomos', 'for', 'fora', 'foram', 'fôramos', 'forem', 'forma', 'formos', 'fosse', 'fossem', 'fôssemos', 'foste', 'fostes', 'fui', 'geral', 'grande', 'grandes', 'grupo', 'há', 'haja', 'hajam', 'hajamos', 'hão', 'havemos', 'havia', 'hei', 'hoje', 'hora', 'horas', 'houve', 'houvemos', 'houver', 'houvera', 'houverá', 'houveram', 'houvéramos', 'houverão', 'houverei', 'houverem', 'houveremos', 'houveria', 'houveriam', 'houveríamos', 'houvermos', 'houvesse', 'houvessem', 'houvéssemos', 'isso', 'isto', 'já', 'la', 'lá', 'lado', 'lhe', 'lhes', 'lo', 'local', 'logo', 'longe', 'lugar', 'maior', 'maioria', 'mais', 'mal', 'mas', 'máximo', 'me', 'meio', 'menor', 'menos', 'mês', 'meses', 'mesma', 'mesmas', 'mesmo', 'mesmos', 'meu', 'meus', 'mil', 'minha', 'minhas', 'momento', 'muita', 'muitas', 'muito', 'muitos', 'na', 'nada', 'não', 'naquela', 'naquelas', 'naquele', 'naqueles', 'nas', 'nem', 'nenhum', 'nenhuma', 'nessa', 'nessas', 'nesse', 'nesses', 'nesta', 'nestas', 'neste', 'nestes', 'ninguém', 'nível', 'no', 'noite', 'nome', 'nos', 'nós', 'nossa', 'nossas', 'nosso', 'nossos', 'nova', 'novas', 'nove', 'novo', 'novos', 'num', 'numa', 'número', 'nunca', 'o', 'obra', 'obrigada', 'obrigado', 'oitava', 'oitavo', 'oito', 'onde', 'ontem', 'onze', 'os', 'ou', 'outra', 'outras', 'outro', 'outros', 'para', 'parece', 'parte', 'partir', 'paucas', 'pela', 'pelas', 'pelo', 'pelos', 'pequena', 'pequenas', 'pequeno', 'pequenos', 'per', 'perante', 'perto', 'pode', 'pude', 'pôde', 'podem', 'podendo', 'poder', 'poderia', 'poderiam', 'podia', 'podiam', 'põe', 'põem', 'pois', 'ponto', 'pontos', 'por', 'porém', 'porque', 'porquê', 'posição', 'possível', 'possivelmente', 'posso', 'pouca', 'poucas', 'pouco', 'poucos', 'primeira', 'primeiras', 'primeiro', 'primeiros', 'própria', 'próprias', 'próprio', 'próprios', 'próxima', 'próximas', 'próximo', 'próximos', 'pude', 'puderam', 'quais', 'quáis', 'qual', 'quando', 'quanto', 'quantos', 'quarta', 'quarto', 'quatro', 'que', 'quê', 'quem', 'quer', 'quereis', 'querem', 'queremas', 'queres', 'quero', 'questão', 'quinta', 'quinto', 'quinze', 'relação', 'sabe', 'sabem', 'são', 'se', 'segunda', 'segundo', 'sei', 'seis', 'seja', 'sejam', 'sejamos', 'sem', 'sempre', 'sendo', 'ser', 'será', 'serão', 'serei', 'seremos', 'seria', 'seriam', 'seríamos', 'sete', 'sétima', 'sétimo', 'seu', 'seus', 'sexta', 'sexto', 'si', 'sido', 'sim', 'sistema', 'só', 'sob', 'sobre', 'sois', 'somos', 'sou', 'sua', 'suas', 'tal', 'talvez', 'também', 'tampouco', 'tanta', 'tantas', 'tanto', 'tão', 'tarde', 'te', 'tem', 'tém', 'têm', 'temos', 'tendes', 'tendo', 'tenha', 'tenham', 'tenhamos', 'tenho', 'tens', 'ter', 'terá', 'terão', 'terceira', 'terceiro', 'terei', 'teremos', 'teria', 'teriam', 'teríamos', 'teu', 'teus', 'teve', 'ti', 'tido', 'tinha', 'tinham', 'tínhamos', 'tive', 'tivemos', 'tiver', 'tivera', 'tiveram', 'tivéramos', 'tiverem', 'tivermos', 'tivesse', 'tivessem', 'tivéssemos', 'tiveste', 'tivestes', 'toda', 'todas', 'R$', '1ª','todavia', 'todo', 'todos', 'trabalho', 'três', 'treze', 'tu', 'tua', 'tuas', 'tudo', 'última', 'últimas', 'último', 'últimos', 'um', 'uma', 'umas', 'uns', 'vai', 'vais', 'vão', 'vários', 'vem', 'vêm', 'vendo', 'vens', 'ver', 'vez', 'vezes', 'viagem', 'vindo', 'vinte', 'vir', 'você', 'vocês', 'vos', 'vós', 'vossa', 'vossas', 'vosso', 'vossos', 'zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_', 'nº', '–', 'rio', 'de', 'janeiro', 'ricardo']
    
    # abrimos em modo leitura o arquivo que criamos anteriormente
    with open('sentencas.txt', 'r', encoding='UTF-8') as f:
        texto = f.read()

    # removemos pontuação, transformamos tudo em minusculo e splitamos o texto
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    texto = texto.lower()
    palavras = texto.split()

    # vamos adicionando dentro da nossa lista as palavras dentro do arquivo exceto as stop words que definimos
    for palavra in palavras:
        if palavra.lower() not in palavras_lixo:
            palavras_sem_lixo.append(palavra)

    # adicionamos dentro de uma string todas as palavras que formam um texto sem as stop words e criamos um arquivo
    texto_sem_lixo = ' '.join(palavras_sem_lixo)
    arquivo_txt = open('sentencas_limpo.txt', 'w', encoding='UTF-8')
    arquivo_txt.write(texto_sem_lixo)
    arquivo_txt.close()

    # abrimos o arquivo com o texto já limpo em modo leitura
    with open('sentencas_limpo.txt', 'r', encoding='UTF-8') as f:
        texto = f.read()

    # splitamos o texto para que possamos contar a frequencia das palavras
    palavras = texto.split()
    frequencias = {}
    for palavra in palavras:
        if palavra in frequencias:
            frequencias[palavra] += 1
        else:
            frequencias[palavra] = 1

    # ordenamos as palavras das mais frequentes para as menos frequentes
    palavras_ordenadas = sorted(frequencias, key=frequencias.get, reverse=True)
    palavras_ordenadas_txt = ''
    # mostramos as 10 palavras mais frequentes
    for palavra in palavras_ordenadas[:10]:
        palavras_ordenadas_txt += f'{str(palavra)} {frequencias[palavra]}\n'

    top_palavras = palavras_ordenadas[:10]

    y_pos = range(len(top_palavras))
    plt.barh(y_pos, [frequencias[palavra] for palavra in top_palavras])
    plt.yticks(y_pos, top_palavras)
    plt.xlabel('Número de ocorrências')
    plt.title('Palavras mais utilizadas')
    plt.show()

    arquivo_txt = open('palavras_ordenadas.txt', 'w', encoding='UTF-8')
    arquivo_txt.write(palavras_ordenadas_txt)
    arquivo_txt.close()

    with open('sentencas.txt', 'r', encoding='UTF-8') as f:
        texto_completo = f.read()
        textos = re.split('--------------------------', texto_completo)
    
    primeiras_frases = []
    for texto in textos:
        primeira_frase = re.split('\.|\!|\?|\¿|\-|\-', texto)[0]
        primeiras_frases.append(primeira_frase)

    lista_sem_n = [string.strip() for string in primeiras_frases]
    lista_sentencas_padronizada = [a.upper() for a in lista_sem_n]
    frequencias = {}

    for sentencas_padronizadas in lista_sentencas_padronizada:
        if sentencas_padronizadas in frequencias:
            frequencias[sentencas_padronizadas] += 1
        else:
            frequencias[sentencas_padronizadas] = 1

    sentencas_ordenadas = sorted(frequencias, key=frequencias.get, reverse=True)
    sentencas_ordenadas_txt = ''
    for x in sentencas_ordenadas:
        sentencas_ordenadas_txt += f'{str(x)} {frequencias[x]}\n'

    arquivo_txt = open('sentencas_ordenadas.txt', 'w', encoding='UTF-8')
    arquivo_txt.write(sentencas_ordenadas_txt)
    arquivo_txt.close()
    

main()