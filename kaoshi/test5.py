import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
plt.rcParams["font.family"] = "SimHei"
plt.rcParams["axes.unicode_minus"] = False
def load_stopwords():
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords = set(f.read().splitlines())
    return stopwords
def clean_text(text):
    import re
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
def process_text(text, stopwords):
    words = jieba.cut(text)
    filtered_words = [word for word in words if word not in stopwords]
    return ' '.join(filtered_words)

def process_file(csv_file):
    df = pd.read_csv(csv_file)
    stopwords = load_stopwords()
    df['cleaned_content'] = df['content'].apply(lambda x: clean_text(str(x)))

    df['processed_content'] = df['cleaned_content'].apply(lambda x: process_text(x, stopwords))
    return df

df = process_file('news.csv')

def extract_features(df):

    tfidf_vectorizer = TfidfVectorizer(max_features=1000, max_df=0.9, min_df=5, ngram_range=(1, 2))
    X_tfidf = tfidf_vectorizer.fit_transform(df['processed_content'])
    return tfidf_vectorizer, X_tfidf

tfidf_vectorizer, X_tfidf = extract_features(df)

def get_keywords_for_article(tfidf_vectorizer, X_tfidf, index=0):
    feature_names = tfidf_vectorizer.get_feature_names_out()
    article_tfidf = X_tfidf[index].toarray().flatten()
    keywords = [(feature_names[i], article_tfidf[i]) for i in range(len(article_tfidf)) if article_tfidf[i] > 0]
    keywords = sorted(keywords, key=lambda x: x[1], reverse=True)  #
    return [keyword[0] for keyword in keywords]

keywords = get_keywords_for_article(tfidf_vectorizer, X_tfidf, index=0)
print(f"第一篇新闻的关键词：{keywords[:10]}")
def build_cooccurrence_matrix(df, tfidf_vectorizer, X_tfidf, window_size=5):
    cooccurrence_matrix = defaultdict(lambda: defaultdict(int))
    for idx, row in df.iterrows():
        article_keywords = get_keywords_for_article(tfidf_vectorizer, X_tfidf, index=idx)
        for i in range(len(article_keywords)):
            for j in range(i + 1, len(article_keywords)):
                keyword1, keyword2 = article_keywords[i], article_keywords[j]
                cooccurrence_matrix[keyword1][keyword2] += 1
                cooccurrence_matrix[keyword2][keyword1] += 1
    return cooccurrence_matrix
cooccurrence_matrix = build_cooccurrence_matrix(df, tfidf_vectorizer, X_tfidf)

def build_network_graph(cooccurrence_matrix, threshold=1):
    G = nx.Graph()
    for keyword1 in cooccurrence_matrix:
        G.add_node(keyword1)
        for keyword2 in cooccurrence_matrix[keyword1]:
            weight = cooccurrence_matrix[keyword1][keyword2]
            if weight >= threshold:
                G.add_edge(keyword1, keyword2, weight=weight)
    return G
G = build_network_graph(cooccurrence_matrix, threshold=1)
def plot_network_graph(G):
    pos = nx.spring_layout(G, k=0.3, iterations=50)
    plt.figure(figsize=(12, 12))
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='skyblue', alpha=0.6)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.6, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
    plt.title("新闻关键词共现网络图")
    plt.axis('off')
    plt.show()
plot_network_graph(G)
