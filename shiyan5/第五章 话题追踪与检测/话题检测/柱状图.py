import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
if __name__ == '__main__':
    mpl.rcParams["font.sans-serif"] = ["SimHei"]
    mpl.rcParams["axes.unicode_minus"] = False
    classes = ['NB, Count Vectors','NB, WordLevel TF-IDF','NB, N-Gram Vectors','NB, CharLevel Vectors',
               'LR, Count Vectors','LR, WordLevel TF-IDF','LR, N-Gram Vectors','LR, CharLevel Vectors',
               'SVM, N-Gram Vectors','RF, Count Vectors','RF, WordLevel TF-IDF',
               'Xgb, Count Vectors','Xgb, WordLevel TF-IDF','Xgb, CharLevel Vectors','NN, Ngram Level TF IDF Vectors']
    accuracy = [77,73,80,80,84,82,84,89,15,68,80,88,87,94,6]
    plt.bar(classes, accuracy, color="lightcoral")
    plt.xticks(classes, classes, rotation=30)  # 这里是调节横坐标的倾斜度，rotation是度数
    plt.ylabel('accuracy(%)')  # 这里是调节横坐标的倾斜度，rotation是度数
    #plt.title('accuracy')
    # 显示柱坐标上边的数字
    for a, b in zip(classes, accuracy):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=17)  # fontsize表示柱坐标上显示字体的大小
    plt.show()