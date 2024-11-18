import re
import jieba
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_yahei_consolas = fm.FontProperties(fname="C:\Windows\Fonts\simhei.ttf")
import networkx as nx
import csv


# 文本预处理
jieba.load_userdict("name_dict.txt")  # 自定义词典

# 读取剧情梗概
summary_fr = open("drama_list.txt", "r", encoding="utf-8")
summary_text = summary_fr.read()
# 按句号分句，分词后写入文件
with open("content.txt", "w", encoding="utf-8") as f:
    sentences = summary_text.split("。")  # 按句号分句
    for sentence in sentences:
        s = re.sub(r"，|。|？|：|“|”|!", "", sentence.strip())  # 去掉特殊字符
        words = list(jieba.cut(s))  # 分词
        out_str = " ".join(words)  # 将词列表转换为字符串输出
        f.write(out_str + "\n")  # 写入文件

# 人物出场次数统计
# 读取分词后的剧情和人物名字
with open("content.txt", "r", encoding="utf-8") as f:
    data_summary = f.read()  # 剧情梗概读取为字符串类型
with open("name_dict.txt", "r", encoding="utf-8") as f:
    data_name = [line.strip("\n") for line in f.readlines()]  # 人名读取为列表
data_name
# 统计各个人物在剧情梗概中出现的次数
count = []  # 记录人名及其出现的次数[[name， count],[]]
for name in data_name:
    count.append([name, data_summary.count(name)])
count.sort(key=lambda x: x[1], reverse=True)  # 按出现次数多少降序排序

# 画图
_, ax = plt.subplots()
names = [x[0] for x in count[:10]]  # 纵坐标
numbers = [x[1] for x in count[:10]]  # 横坐标
ax.barh(range(10), numbers, color=["peru", "coral"], align="center")
ax.set_title("人物出场次数", fontsize=14, fontproperties=font_yahei_consolas)
ax.set_yticks(range(10))
ax.set_yticklabels(names, fontsize=14, fontproperties=font_yahei_consolas)
plt.show()

# 社交网络分析
with open("name_dict.txt", "r", encoding="utf-8") as f:
    ata_name = [line.strip("\n") for line in f.readlines()]  # 人名读取为列表
with open("content.txt", "r", encoding="utf-8") as f:
    data_summary = f.readlines()
graph = nx.Graph()

# 初始化图
# 添加节点及其权值
for item in count:
    graph.add_node(item[0], weight=item[1])
name_count = len(data_name)  # 总人数
edges = []  # 记录边的信息
# 如果两个人在同一句话中出现，边的权重+1
for colindex in range(name_count):
    for rowindex in range(name_count):
        weight = 0  # 边的权值， 如果为0， 说明俩人之间没有交集
        for sentence in data_summary:
            if data_name[colindex] in sentence and data_name[rowindex] in sentence:
                weight += 1
        if weight != 0 and data_name[colindex] != data_name[rowindex]:
            edges.append([data_name[colindex], data_name[rowindex], weight])
            graph.add_edge(
                data_name[colindex], data_name[rowindex], weight=weight
            )  # 添加边

# 将关系图的信息存储到csv文件中
nodes = []  # 记录点的信息
for node in count:
    nodes.append([node[0], node[0], node[1]])
with open("node.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Id", "label", "weight"])
    writer.writerows(nodes)
edges = []  # 记录边的信息
for edge in graph.edges(data=True):
    edges.append([edge[0], edge[1], edge[2]["weight"], "undirected"])
with open("edge.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["source", "target", "weight", "Type"])
    writer.writerows(edges)
