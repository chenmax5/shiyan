import re
import jieba
import pandas as pd


def load_stopwords():
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords = set(f.read().splitlines())
    return stopwords


def clean_text(text):
    # 去除 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)
    # 去除特殊符号
    text = re.sub(r'[^\w\s]', '', text)
    # 去除多余的空格
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def process_text(text, stopwords):
    # 使用结巴分词
    words = jieba.cut(text)
    # 过滤停用词
    filtered_words = [word for word in words if word not in stopwords]
    return ' '.join(filtered_words)


def process_file(csv_file):
    df = pd.read_csv(csv_file)
    stopwords = load_stopwords()

    df['cleaned_content'] = df['content'].apply(lambda x: clean_text(str(x)))  # 清理内容
    df['processed_content'] = df['cleaned_content'].apply(lambda x: process_text(x, stopwords))  # 分词和去停用词

    return df


df = process_file('news.csv')

print(df[['title', 'processed_content']].head())
