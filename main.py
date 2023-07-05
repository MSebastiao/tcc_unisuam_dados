from playwright.sync_api import sync_playwright
from time import sleep
import string
import random
import re
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

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
        for y in range(100):
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

def copiar_elementos(lista_original, posicoes_desejadas):
    lista_copiada = []
    for posicao in posicoes_desejadas:
        if posicao < len(lista_original):
            lista_copiada.append(lista_original[posicao])
    return lista_copiada

def main():
    bot_pega_sentenca()
    # iniciamos uma lista vazia e uma lista com stop words que iremos remover
    palavras_sem_lixo_nltk = []
    palavras_sem_lixo_def = []
    stopwords_juridico = ['1', 'meses', 'ausência', 'ainda', 'fatos','paciente','denúncia', 'forma', 'nº', 'além', 'assim', 'lei', '¿', 'pena', 'penal', 'crime', 'acusado', 'código', 'recurso', 'autos', 'art', 'artigo', 'réu', '33', '1134306', 'anos', 'prova', 'policiais', 'regime', 'anos', 'prática', 'juízo', 'criminal', 'apelante', 'quanto', 'sendo', 'processo', 'reclusão', 'delito', 'sentença', 'associação', 'autoria', 'apelação', 'razão', 'legal','caso','material','qualquer','crime','crimes','criminosa','circunstâncias','liberdade','local','policial','vítima','mínimo','defensivo','diasmulta']
    
    # abrimos em modo leitura o arquivo que criamos anteriormente
    with open('sentencas.txt', 'r', encoding='UTF-8') as f:
        texto = f.read()

    # removemos pontuação, transformamos tudo em minusculo e splitamos o texto
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    texto = texto.lower()
    lista_palavras = texto.split()

    # dentro de um loop, vamos removendo as stopwords da lingua portuguesa
    #nltk.download('stopwords')
    palavra_lixo = stopwords.words('portuguese')
    # vamos adicionando dentro da nossa lista as palavras dentro do arquivo exceto as stop words da biblioteca nltk
    for palavra in lista_palavras:
        if palavra.lower() not in palavra_lixo:
            palavras_sem_lixo_nltk.append(palavra)

    # adicionamos dentro de uma string todas as palavras que formam um texto sem as stop words e a partir disso, removemos uma lista de stopwords da área juridica
    texto_sem_lixo = ' '.join(palavras_sem_lixo_nltk)
    lista_palavras = texto_sem_lixo.split()
    for palavra in lista_palavras:
        if palavra.lower() not in stopwords_juridico:
            palavras_sem_lixo_def.append(palavra)
    
    # adicionamos nosso texto limpo definitivo dentro de um arquivo e salvamos
    texto_sem_lixo = ' '.join(palavras_sem_lixo_def)
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

    # geramos um gráfico com as palavras mais utilizadas
    y_pos = range(len(top_palavras))
    plt.bar(y_pos, [frequencias[palavra] for palavra in top_palavras])
    plt.xticks(y_pos, top_palavras)
    plt.ylabel('Número de ocorrências')
    plt.title('Palavras mais frequentes')
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

    indices = [0, 2, 6]
    top_palavras = copiar_elementos(sentencas_ordenadas, indices)

    y_pos = range(len(top_palavras))
    plt.bar(y_pos, [frequencias[palavra] for palavra in top_palavras])
    plt.xticks(y_pos, top_palavras)
    plt.ylabel('Número de ocorrências')
    plt.title('Recursos mais frequentes')
    plt.show()

    arquivo_txt = open('sentencas_ordenadas.txt', 'w', encoding='UTF-8')
    arquivo_txt.write(sentencas_ordenadas_txt)
    arquivo_txt.close()
    
main()