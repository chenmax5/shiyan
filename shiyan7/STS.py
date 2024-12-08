from gensim.models.word2vec import Word2Vec
import pandas as pd
import time


# 分词并去停用词
def split_words(sentences: str):
    stop_words = [
        "",
        "the",
        ",",
        "a",
        "of",
        "an",
        "at",
        "is",
        "it",
        "in",
        "as",
        "'s",
        ".",
        "(",
        ")",
        "'",
        "...",
        "--",
        "``",
        "''",
        "''",
    ]
    words = sentences.split(" ")
    return [word.lower() for word in words if word.lower() not in stop_words]


all_sentences = [split_words(data["sentence"]) for data in sst_datasets]
print(f"all_sentences[0:2l={all_sentences[0:2]}")

# 训sword2vector词统入模型
print(f"{time.ctime()}: 开始训练word2vector英型")
word2vector = Word2Vec(all_sentences, vector_size=100, min_count=5, epochs=200, sg=0)
print(f"{time.ctime()}:word2vector模型训练结束")

# 保存词向量辕垫
W2V_TXT_FILE = "word2vector_23.txt"
word2vector.wv.save_ord2vec_format(W2V_TXT_FILE)

# 根指word2vector模型查看和movie,相近的词
print(f"和movie相近的词如下:")
for i in word2vector.wv.most_similar("movies"):
    print("--->", i[0], i[1])
