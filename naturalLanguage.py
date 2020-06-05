import nltk
import gensim
import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize
import pandas as pd
from firebadminEu import get_info_db

def trataEmpreendimento(pesquisar):

	eList = get_info_db("PesquisasBot/Empreendimentos")
	empreendimentos = []

	for item in eList:
		empreendimentos.append(item)

	wordlist = [[word.lower() for word in word_tokenize(empreendimento)] for empreendimento in empreendimentos]
	dct = gensim.corpora.Dictionary(wordlist)
	corpus = [dct.doc2bow(word) for word in wordlist]
	tfIdf = gensim.models.TfidfModel(corpus)
	simi = gensim.similarities.Similarity('workdir/', tfIdf[corpus], num_features=len(dct))
	email = [pesquisar]
	wordSearch = [[w.lower() for w in word_tokenize(emp)] for emp in email]
	search = [dct.doc2bow(palavra) for palavra in wordSearch]

	cont = 0
	maior = 0.
	for i in simi[tfIdf[search]]:
		for x in i:
			if x > maior:
				contador = cont
				maior = x
			cont+=1
	
	try:
		empreendFinal = empreendimentos[contador]
	except:
		return False, False, False
	print(empreendFinal)
	semelhanca = maior * 100
	semelhanca = (np.around(semelhanca, decimals=2))
	print(pesquisar + " -> " + empreendFinal)
	print("Acertividade em: " + str(semelhanca) + "%")
	print("=========================\n")
	if semelhanca > 80.0:
		codEmpreend = eList[empreendFinal]['cod']
		construtora = eList[empreendFinal]['construtora']
		return empreendFinal, codEmpreend, construtora
	else:
		return False, False, False
