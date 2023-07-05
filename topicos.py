import nltk
from gensim import corpora, models
import re

# Faça o download dos recursos do NLTK (apenas na primeira execução)
#nltk.download('stopwords')
#nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

with open('sentencas.txt', 'r', encoding='UTF-8') as f:
        texto_completo = f.read()
        textos = re.split('--------------------------', texto_completo)


# Pré-processamento dos documentos
stop_words = set(stopwords.words('portuguese'))
stop_words_juridico = ['ii','index', 'meses', 'ausência', 'ainda', 'fatos','paciente','denúncia', 'forma', 'nº', 'além', 'assim', 'lei', '¿', 'pena', 'penal', 'crime', 'acusado', 'código', 'recurso', 'autos', 'art', 'artigo', 'réu', '33', '1134306', 'anos', 'prova', 'policiais', 'regime', 'anos', 'prática', 'juízo', 'criminal', 'apelante', 'quanto', 'sendo', 'processo', 'reclusão', 'delito', 'sentença', 'associação', 'autoria', 'apelação', 'razão', 'legal','caso','material','qualquer','crime','crimes','criminosa','circunstâncias','liberdade','local','policial','vítima','mínimo','defensivo','diasmulta']
texts = []

for document in textos:
    tokens = word_tokenize(document.lower())  # Tokenização
    tokens = [token for token in tokens if token.isalpha()]  # Remoção de pontuações e números
    tokens = [token for token in tokens if token not in stop_words]  # Remoção de stopwords
    tokens = [token for token in tokens if token not in stop_words_juridico]
    texts.append(tokens)


# Crie o dicionário a partir dos textos
dictionary = corpora.Dictionary(texts)

# Crie o corpus (representação vetorizada dos documentos)
corpus = [dictionary.doc2bow(text) for text in texts]


# Crie o modelo LDA
lda_model = models.LdaModel(corpus, num_topics=4, id2word=dictionary, passes=10)

# Imprima os tópicos gerados
for idx, topic in lda_model.print_topics(num_words=4):
    print(f'Tópico {idx+1}: {topic}\n')
