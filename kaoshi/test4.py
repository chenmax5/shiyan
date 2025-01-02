import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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


# 特征提取：TF-IDF
def extract_features(df):
    # 使用TF-IDF算法对文本进行向量化
    tfidf_vectorizer = TfidfVectorizer(max_features=1000, max_df=0.9, min_df=5, ngram_range=(1, 2))  # 可以使用1-gram和2-gram
    X_tfidf = tfidf_vectorizer.fit_transform(df['processed_content'])  # 生成TF-IDF矩阵
    return X_tfidf


# 提取特征矩阵
X_tfidf = extract_features(df)


# 计算余弦相似度并获取与第一篇新闻最相似的10篇新闻
def find_similar_news(X_tfidf, top_n=10):
    # 计算第一篇新闻与其他新闻的余弦相似度
    cosine_similarities = cosine_similarity(X_tfidf[0:1], X_tfidf)  # 计算第一篇新闻与所有其他新闻的相似度

    # 获取与第一篇新闻最相似的10篇新闻
    similar_indices = cosine_similarities[0].argsort()[-(top_n + 1):-1]  # 排除第一篇新闻本身
    similar_news = df.iloc[similar_indices]

    return similar_news


# 获取与第一篇新闻最相似的10篇新闻
similar_news = find_similar_news(X_tfidf)

# 显示相似新闻的标题和相似度
similar_news['similarity'] = cosine_similarity(X_tfidf[0:1], X_tfidf[similar_news.index])[0]
print(similar_news[['title', 'similarity']])
