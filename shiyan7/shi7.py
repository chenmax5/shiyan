import os
import pandas as pd
import re
import jieba.posseg as pseg
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from gensim import corpora, models


# 代码7-2 数据清洗
os.chdir('D:/2024_4/hujichao/pythonProject6/hu')
reviews = pd.read_csv('pinglun2.csv')
# 去除英文、数字等，去除京东、美的、电热水器、热水器等词语
strinfo = re.compile('[0-9a-zA-Z]|京东|美的|电热水器|热水器|')
reviews['评论内容'] = reviews['评论内容'].apply(lambda x: strinfo.sub('', x))

# 代码7-3 分词、词性标注、去除停用词代码
# 分词
worker = lambda s: [(x.word, x.flag) for x in pseg.cut(s)]  # 自定义简单分词函数
seg_word = reviews['评论内容'].apply(worker)

# 将词语转为数据框形式，一列是词，一列是词语所在的句子ID，最后一列是词语在该句子的位置
n_word = seg_word.apply(lambda x: len(x))  # 每一评论中词的个数
n_content = [[x + 1] * y for x, y in zip(list(seg_word.index), list(n_word))]
index_content = sum(n_content, [])  # 将嵌套的列表展开，作为词所在评论的id
seg_word = sum(seg_word, [])
word = [x[0] for x in seg_word]  # 词
nature = [x[1] for x in seg_word]  # 词性

# 由于原始数据中没有 content_type 列，这里先删除相关代码
# content_type = [[x]*y for x,y in zip(list(reviews['content_type']), list(n_word))]
# content_type = sum(content_type, [])  # 评论类型

result = pd.DataFrame({"index_content": index_content,
                       "word": word,
                       "nature": nature})

# 删除标点符号
result = result[result['nature']!= 'x']  # x表示标点符号

# 删除停用词
stop_path = open("../实验七/停用词.txt", 'r', encoding='UTF-8')
stop = stop_path.readlines()
stop = [x.replace('\n', '') for x in stop]
word = list(set(word) - set(stop))
result = result[result['word'].isin(word)]

# 构造各词在对应评论的位置列
n_word = list(result.groupby(by=['index_content'])['index_content'].count())
index_word = [list(np.arange(0, y)) for y in n_word]
index_word = sum(index_word, [])  # 表示词语在改评论的位置

# 合并评论id，评论中词的id，词，词性
result['index_word'] = index_word

# 代码7-4 提取含有名词的评论
# 提取含有名词类的评论
ind = result[['n' in x for x in result['nature']]]['index_content'].unique()
result = result[[x in ind for x in result['index_content']]]

# 代码7-5 绘制词云
frequencies = result.groupby(by=['word'])['word'].count()
frequencies = frequencies.sort_values(ascending=False)
backgroud_Image = plt.imread('../实验七/w700d1q75cms.jpg')
wordcloud = WordCloud(font_path="simhei.ttf",
                      max_words=100,
                      background_color='white',
                      mask=backgroud_Image)
my_wordcloud = wordcloud.fit_words(frequencies)
plt.imshow(my_wordcloud)
plt.axis('off')
plt.show()

# 将结果写出
result.to_csv("../word.csv", index=False, encoding='utf-8')

# 代码7-6 匹配情感词
word = pd.read_csv("../实验七/data/情感词.txt", sep=' ', names=['word', 'weight'])
pd.options.mode.chained_assignment = None

# 读入正面、负面情感评价词
pos_comment = pd.read_csv("../实验七/data/正面评价词语（中文）.txt", header=None)
neg_comment = pd.read_csv("../实验七/data/负面评价词语（中文）.txt", header=None)
pos_emotion = pd.read_csv("../实验七/data/正面情感词语（中文）.txt", header=None)
neg_emotion = pd.read_csv("../实验七/data/负面情感词语（中文）.txt", header=None)

# 合并情感词与评价词
positive = set(pos_comment.iloc[:, 0]) | set(pos_emotion.iloc[:, 0])
negative = set(neg_comment.iloc[:, 0]) | set(neg_emotion.iloc[:, 0])
intersection = positive & negative  # 正负面情感词表中相同的词语
positive = list(positive - intersection)
negative = list(negative - intersection)
positive = pd.DataFrame({"word": positive, "weight": [1] * len(positive)})
negative = pd.DataFrame({"word": negative, "weight": [-1] * len(negative)})
posneg = pd.concat([positive, negative], ignore_index=True)

#  将分词结果与正负面情感词表合并，定位情感词
# 假设 posneg 有 'word' 列，result 有 'index_content' 和 'index_word' 列
# 为了在合并后保留 'index_content' 和 'index_word' 列，我们使用左连接
data_posneg = posneg.merge(result[['word', 'index_content', 'index_word']], on='word', how='left')

# 代码7-7 修正情感倾向
# 根据情感词前时候有否定词或双层否定词对情感值进行修正
# 载入否定词表
try:
    notdict = pd.read_csv("../实验七/data/否定词.txt")
    if 'term' not in notdict.columns:
        # 如果文件中没有 'term' 列，手动指定列名
        notdict = pd.read_csv("../实验七/data/否定词.txt", names=['term'])
except FileNotFoundError:
    print("否定词文件未找到，请检查路径是否正确。")
    exit(1)


# 处理否定修饰词
data_posneg['amend_weight'] = data_posneg['weight']  # 构造新列，作为经过否定词修正后情感值
data_posneg['id'] = np.arange(0, len(data_posneg))
only_inclination = data_posneg.dropna()  # 只保留有情感值的词语
only_inclination.index = np.arange(0, len(only_inclination))
index = only_inclination['id']

for i in np.arange(0, len(only_inclination)):
    review = data_posneg[data_posneg['index_content'] ==
                         only_inclination['index_content'][i]]  # 提取第i个情感词所在的评论
    review.index = np.arange(0, len(review))
    affective = int(only_inclination['index_word'][i])
    if affective == 1:
        ne = sum([i in notdict['term'] for i in review['word'][:affective]])
        if ne == 1:
            data_posneg['amend_weight'][index[i]] = -\
                data_posneg['weight'][index[i]]
    elif affective > 1:
        ne = sum([i in notdict['term'] for i in review['word'][affective - 2:affective]])
        if ne == 1:
            data_posneg['amend_weight'][index[i]] = -\
                data_posneg['weight'][index[i]]

# 更新只保留情感值的数据
only_inclination = only_inclination.dropna()

# 计算每条评论的情感值
emotional_value = only_inclination.groupby(['index_content'], as_index=False)['amend_weight'].sum()

# 去除情感值为0的评论
emotional_value = emotional_value[emotional_value['amend_weight']!= 0]

# 代码7-8 查看情感分析效果
# 给情感值大于0的赋予评论类型（content_type）为pos,小于0的为neg
emotional_value.loc[emotional_value['amend_weight'] > 0, 'a_type'] = 'pos'
emotional_value.loc[emotional_value['amend_weight'] < 0, 'a_type'] = 'neg'

# 查看情感分析结果
result = emotional_value.merge(result[['index_content', 'word']], left_on='index_content', right_on='index_content', how='left')

# 确保保留 word 列
result = result[['index_content', 'a_type', 'word']].drop_duplicates()
confusion_matrix = pd.crosstab(result['a_type'].str.slice(0, 2), result['a_type'].str.slice(0, 2),
                               margins=True)
if confusion_matrix.shape[0] > 2 and confusion_matrix.shape[1] > 2:
    score = (confusion_matrix.iat[0, 0] + confusion_matrix.iat[1, 1]) / confusion_matrix.iat[2, 2]
else:
    print("交叉表的维度不符合预期，无法计算得分。")
    score = None

# 提取正负面评论信息
ind_pos = list(emotional_value[emotional_value['a_type'] == 'pos']['index_content'])
ind_neg = list(emotional_value[emotional_value['a_type'] == 'neg']['index_content'])
posdata = result[[i in ind_pos for i in result['index_content']]]
negdata = result[[i in ind_neg for i in result['index_content']]]

# 7-9绘制词云
# 正面情感词词云
freq_pos = posdata.groupby(by=['word'])['word'].count()
freq_pos = freq_pos.sort_values(ascending=False)
backgroud_Image = plt.imread('../实验七/w700d1q75cms.jpg')
wordcloud = WordCloud(font_path="simhei.ttf",
                      max_words=100,
                      background_color='white',
                      mask=backgroud_Image)
pos_wordcloud = wordcloud.fit_words(freq_pos)
plt.imshow(pos_wordcloud)
plt.axis('off')
plt.show()

# 检查 freq_neg 是否为空
if not negdata.empty:
    freq_neg = negdata.groupby(by=['word'])['word'].count()
    if not freq_neg.empty:
        neg_wordcloud = wordcloud.fit_words(freq_neg)
        plt.imshow(neg_wordcloud)
        plt.axis('off')
        plt.show()
    else:
        print("负面情感词频率为空，无法生成词云。")
else:
    print("negdata 为空，没有负面情感词数据。")

# 将结果写出,每条评论作为一行
posdata.to_csv("../实验七/tmp/posdata.csv", index=False, encoding='utf-8')
negdata.to_csv("../实验七/tmp/negdata.csv", index=False, encoding='utf-8')

# 代码7-10 建立词典及语料库
posdata = pd.read_csv("../实验七/tmp/posdata.csv", encoding='utf-8')
negdata = pd.read_csv("../实验七/tmp/negdata.csv", encoding='utf-8')

# 建立词典
pos_dict = corpora.Dictionary([[i] for i in posdata['word']])  # 正面
neg_dict = corpora.Dictionary([[i] for i in negdata['word']])  # 负面

# 建立语料库
pos_corpus = [pos_dict.doc2bow(j) for j in [[i] for i in posdata['word']]]  # 正面
neg_corpus = [neg_dict.doc2bow(j) for j in [[i] for i in negdata['word']]]  # 负面

# 代码7-11 主题数寻优
# 构造主题数寻优函数
def cos(vector1, vector2):  # 余弦相似度函数
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return (None)
    else:
        return (dot_product / ((normA * normB) ** 0.5))
