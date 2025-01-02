import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import numpy as np


# 停用词加载函数
def load_stopwords():
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords = set(f.read().splitlines())
    return stopwords


# 清理文本函数：去除HTML标签、特殊符号
def clean_text(text):
    import re
    # 去除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    # 去除特殊字符
    text = re.sub(r'[^\w\s]', '', text)
    # 去除多余的空格
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# 文本分词函数
def process_text(text, stopwords):
    words = jieba.cut(text)  # 使用结巴分词
    filtered_words = [word for word in words if word not in stopwords]  # 去除停用词
    return ' '.join(filtered_words)


# 加载数据并处理
def process_file(csv_file):
    # 读取CSV文件
    df = pd.read_csv(csv_file)

    # 加载停用词
    stopwords = load_stopwords()

    # 清理文本
    df['cleaned_content'] = df['content'].apply(lambda x: clean_text(str(x)))

    # 分词并去停用词
    df['processed_content'] = df['cleaned_content'].apply(lambda x: process_text(x, stopwords))

    return df


# 处理CSV文件
df = process_file('news.csv')


# 特征提取：词袋模型（BOW）+ TF-IDF
def extract_features(df):
    # 使用TF-IDF算法对文本进行向量化
    tfidf_vectorizer = TfidfVectorizer(max_features=1000, max_df=0.9, min_df=5, ngram_range=(1, 2))  # 可以使用1-gram和2-gram
    X_tfidf = tfidf_vectorizer.fit_transform(df['processed_content'])  # 生成TF-IDF矩阵

    # 输出TF-IDF的特征名（词汇表）
    feature_names = tfidf_vectorizer.get_feature_names_out()
    print("TF-IDF特征词汇表:", feature_names)

    # 返回特征矩阵
    return X_tfidf


# 获取特征矩阵
X_tfidf = extract_features(df)


# 如果需要进行降维，可以使用PCA等方法进行处理
def reduce_dimensions(X_tfidf, n_components=50):
    pca = PCA(n_components=n_components)
    X_reduced = pca.fit_transform(X_tfidf.toarray())
    print("降维后的数据维度:", X_reduced.shape)
    return X_reduced


# 降维后的特征矩阵
X_reduced = reduce_dimensions(X_tfidf)

# 如果你需要保存特征矩阵，可以使用numpy保存为文件
np.save('features.npy', X_reduced)
