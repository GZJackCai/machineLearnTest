# -*- coding: utf-8 -*-
'''
demo came from http://www.52nlp.cn/
'''

from gensim import corpora,models,similarities
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
documents=["Shipment of gold damaged in a fire",
           "Delivery of silver arrived in a silver truck",
           "Shipment of gold arrived in a truck"]

texts=[[word for word in document.lower().split()] for document in documents]
print  texts

#将文档抽取为词袋
dictionary=corpora.Dictionary(texts)
print  dictionary
#将文档的token映射为id
print  dictionary.token2id
#用字符串表示的文档转换为id表示的文档向量
corpus=[dictionary.doc2bow(text) for text in texts]
print  corpus
#训练文档，计算tf-idf模型
tfidf=models.TfidfModel(corpus)
#基于模型，用词频表示文档向量为一个tf-idf值表示文档的向量
corpus_tfidf=tfidf[corpus]
for doc in corpus_tfidf:
    print doc
print tfidf.dfs
print tfidf.idfs

#训练LSI模型,将文档矩阵SVD分解，并做了一个秩为2的近似SVD分解，将文档映射到二维的topic空间中
lsi=models.LsiModel(corpus_tfidf,id2word=dictionary,num_topics=2)
lsi.print_topic(2)

#看出文档1，3和topic 1更相关，文档2和topic2更相关
corpus_lsi=lsi[corpus_tfidf]
for doc in corpus_lsi:
    print  doc

#lda模型,每个主题单词有概率意思，加和为1，值越大权重越大
lda=models.LdaModel(corpus_tfidf,id2word=dictionary,num_topics=2)
lda.print_topics(2)

#基于lsi ,计算文档相似度
index=similarities.MatrixSimilarity(lsi[corpus])
query="gold silver trunk"
query_bow=dictionary.doc2bow(query.lower().split())
print  query_bow
#再用之前训练好的LSI 模型映射到二维的topic空间
query_lsi=lsi[query_bow]
print  query_lsi

#最后计算和idnex中doc 的余弦相似度
sims=index[query_lsi]
print  list(enumerate(sims))

#按相似度进行排序
sort_sims=sorted(enumerate(sims),key=lambda  item:-item[1])
print sort_sims




