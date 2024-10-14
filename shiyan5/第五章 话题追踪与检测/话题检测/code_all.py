from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble
import pandas, xgboost, numpy, textblob, string
from keras.preprocessing import text, sequence
from keras import layers, models, optimizers
import os
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

def train_model(classifier, feature_vector_train, label, feature_vector_valid, is_neural_net=False):
    # fit the training dataset on the classifier
    classifier.fit(feature_vector_train, label)
    # predict the labels on validation dataset
    predictions = classifier.predict(feature_vector_valid)
    if is_neural_net:
        predictions = predictions.argmax(axis=-1)
    return metrics.accuracy_score(predictions, valid_y)


def create_model_architecture(input_size):
    # create input layer
    input_layer = layers.Input((input_size,), sparse=True)
    # create hidden layer
    hidden_layer = layers.Dense(100, activation="relu")(input_layer)
    # create output layer
    output_layer = layers.Dense(1, activation="sigmoid")(hidden_layer)
    classifier = models.Model(inputs=input_layer, outputs=output_layer)
    classifier.compile(optimizer=optimizers.Adam(), loss='binary_crossentropy')
    return classifier

if __name__ == '__main__':
    # 加载数据集
    path_data = './tc-corpus-answer/answer/'
    dir_names = os.listdir(path_data)
    labels, texts = [], []
    for dir_name in dir_names:
        file_names = os.listdir(path_data + dir_name + '/')
        for file_name in file_names:
            f = open(path_data + dir_name + '/' + file_name, encoding='gb18030', errors='ignore')
            content = f.read()
            f.close()
            labels.append(dir_name)
            texts.append(content)
    # 创建一个dataframe，列名为text和label
    trainDF = pandas.DataFrame()
    trainDF['text'] = texts
    trainDF['label'] = labels
    # print texts[:10],labels[:10]
    # 将数据集分为训练集和验证集
    train_x, valid_x, train_y, valid_y = model_selection.train_test_split(trainDF['text'], trainDF['label'])
    # print(trainDF,train_x,valid_x)
    # label编码为目标变量
    encoder = preprocessing.LabelEncoder()
    train_y = encoder.fit_transform(train_y)
    valid_y = encoder.fit_transform(valid_y)

    # 创建一个向量计数器对象
    count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
    count_vect.fit(trainDF['text'])
    # 使用向量计数器对象转换训练集和验证集
    xtrain_count = count_vect.transform(train_x)
    xvalid_count = count_vect.transform(valid_x)
    # 词语级tf-idf
    tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=5000)
    tfidf_vect.fit(trainDF['text'])
    xtrain_tfidf = tfidf_vect.transform(train_x)
    xvalid_tfidf = tfidf_vect.transform(valid_x)
    # ngram 级tf-idf
    tfidf_vect_ngram = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(2, 3), max_features=5000)
    tfidf_vect_ngram.fit(trainDF['text'])
    xtrain_tfidf_ngram = tfidf_vect_ngram.transform(train_x)
    xvalid_tfidf_ngram = tfidf_vect_ngram.transform(valid_x)
    # 词性级tf-idf
    tfidf_vect_ngram_chars = TfidfVectorizer(analyzer='char', token_pattern=r'\w{1,}', ngram_range=(2, 3),
                                             max_features=5000)
    tfidf_vect_ngram_chars.fit(trainDF['text'])
    xtrain_tfidf_ngram_chars = tfidf_vect_ngram_chars.transform(train_x)
    xvalid_tfidf_ngram_chars = tfidf_vect_ngram_chars.transform(valid_x)


    # 特征为计数向量的朴素贝叶斯
    accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_count, train_y, xvalid_count)
    print("NB, Count Vectors: ", accuracy)
    # 特征为词语级别TF-IDF向量的朴素贝叶斯
    accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_tfidf, train_y, xvalid_tfidf)
    print("NB, WordLevel TF-IDF: ", accuracy)
    # 特征为多个词语级别TF-IDF向量的朴素贝叶斯
    accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram)
    print("NB, N-Gram Vectors: ", accuracy)
    # 特征为词性级别TF-IDF向量的朴素贝叶斯
    accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_tfidf_ngram_chars, train_y, xvalid_tfidf_ngram_chars)
    print("NB, CharLevel Vectors: ", accuracy)
    # 特征为计数向量的线性分类器
    accuracy = train_model(linear_model.LogisticRegression(), xtrain_count, train_y, xvalid_count)
    print("LR, Count Vectors: ", accuracy)
    # 特征为词语级别TF-IDF向量的线性分类器
    accuracy = train_model(linear_model.LogisticRegression(), xtrain_tfidf, train_y, xvalid_tfidf)
    print("LR, WordLevel TF-IDF: ", accuracy)
    # 特征为多个词语级别TF-IDF向量的线性分类器
    accuracy = train_model(linear_model.LogisticRegression(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram)
    print("LR, N-Gram Vectors: ", accuracy)
    # 特征为词性级别TF-IDF向量的线性分类器
    accuracy = train_model(linear_model.LogisticRegression(), xtrain_tfidf_ngram_chars, train_y,
                           xvalid_tfidf_ngram_chars)
    print("LR, CharLevel Vectors: ", accuracy)

    # 特征为多个词语级别TF-IDF向量的SVM
    accuracy = train_model(svm.SVC(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram)
    print("SVM, N-Gram Vectors: ", accuracy)

    # 特征为计数向量的RF
    accuracy = train_model(ensemble.RandomForestClassifier(), xtrain_count, train_y, xvalid_count)
    print("RF, Count Vectors: ", accuracy)
    # 特征为词语级别TF-IDF向量的RF
    accuracy = train_model(ensemble.RandomForestClassifier(), xtrain_tfidf, train_y, xvalid_tfidf)
    print("RF, WordLevel TF-IDF: ", accuracy)

    # 特征为计数向量的Xgboost
    accuracy = train_model(xgboost.XGBClassifier(), xtrain_count.tocsc(), train_y, xvalid_count.tocsc())
    print("Xgb, Count Vectors: ", accuracy)
    # 特征为词语级别TF-IDF向量的Xgboost
    accuracy = train_model(xgboost.XGBClassifier(), xtrain_tfidf.tocsc(), train_y, xvalid_tfidf.tocsc())
    print("Xgb, WordLevel TF-IDF: ", accuracy)
    # 特征为词性级别TF-IDF向量的Xgboost
    accuracy = train_model(xgboost.XGBClassifier(), xtrain_tfidf_ngram_chars.tocsc(), train_y,
                           xvalid_tfidf_ngram_chars.tocsc())
    print("Xgb, CharLevel Vectors: ", accuracy)

    #浅层神经网络
    classifier = create_model_architecture(xtrain_tfidf_ngram.shape[1])
    accuracy = train_model(classifier, xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram, is_neural_net=True)
    print("NN, Ngram Level TF IDF Vectors", accuracy)

