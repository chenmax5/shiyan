import pandas as pd
import numpy as np
import random
from tqdm import tqdm
from gensim.models.word2vec import Word2Vec
import time
random.seed(2022)


# 数据分组
def split_list(split_list, rates=[]):
    split_target = split_list.copy()
    assert np.array(rates).sum() == 1
    split_len = [int(r * len(split_list)) for r in rates]
    split_result = list()
    for index, length in enumerate(split_len):
        if index >= len(split_len) - 1:
            split_result.append(split_target)
            continue
        split_ = random.sample(split_target, length)
        split_result.append(split_)
        split_target = [data for data in split_target if data not in split_]
    return split_result


def prepare_sst_data():
    sst_datasets = list()
    data_sentence_name = r"SST-2/original/datasetSentences.txt"
    data_sentence = pd.read_csv(data_sentence_name, delimiter="\t", header=0)
    dictionary_name = r"SST-2/original/dictionary.txt"
    dic = pd.read_csv(dictionary_name, delimiter="|", header=None)
    dic_maps = {k: v for k, v in zip(dic[0], dic[1])}
    label_file = r"SST-2/original/sentiment_labels.txt"
    label_info = pd.read_csv(label_file, delimiter="|", header=0)
    label_map = {
        k: v for k, v in zip(label_info["phrase ids"], label_info["sentiment values"])
    }
    for sentence in tqdm(data_sentence["sentence"]):
        if sentence not in dic_maps:
            continue
        label = label_map[dic_maps[sentence]]
        label = 0 if float(label) < 0.5 else 1
        sst_datasets.append({"sentence": sentence, "label": label})
    [train, test] = split_list(sst_datasets, [0.8, 0.2])

    return sst_datasets, train, test


sst_datasets, train_data, test_data = prepare_sst_data()

dataset_radio = lambda dataset: round(
    np.array([label["label"] for label in dataset]).sum() / len(dataset), 4
)

print(
    f"postive in sst datasets = {dataset_radio(sst_datasets)}, total = {len(sst_datasets)}"
)
print(f"postive in train = {dataset_radio(train_data)}, total = {len(train_data)}")
print(f"postive in test = {dataset_radio(test_data)}, total = {len(test_data)}")
print(f"train data[0] = {train_data[0]}")


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
