#-*- coding: utf-8 -*-
#使用ID3决策树算法预测销量高低
# 代码需要统一安装pydot graphviz
import pandas as pd
import os
import pydot
from io import StringIO
os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'
# os.chdir(u'./')
#参数初始化
# inputfile ='sales_data.xls'
data = pd.read_excel('sales_data.xls', index_col = u'序号') #导入数据
print(data)
#数据是类别标签，要将它转换为数据
#用1来表示“好”、“是”、“高”这三个属性，用-1来表示“坏”、“否”、“低”
data[data == u'好'] = 1
data[data == u'是'] = 1
data[data == u'高'] = 1
data[data != 1] = -1
# DataFrame.as_matrix（列=无）[来源]
# 将帧(DataFrame表格)转换为Numpy(行列式)数组表示。
# 前行后列
x = data.iloc[:,:3].as_matrix().astype(int)
print(x)
y = data.iloc[:,3].as_matrix().astype(int)
print(y)
import sklearn.tree as tree
# 决策树的方法(相当于实例化)                                        最小叶子节点
clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=8, min_samples_split=5)
# 调用类方法,传入数据
"""
# fit()可以说是调用的通用方法。
fit(X)，表示用数据X来训练某种模型。 
函数返回值一般为调用fit方法的对象本身。
fit(X,y=None)为无监督学习算法，fit(X,Y)为监督学习算法
"""
tree1=clf.fit(x, y) #训练模型(用训练数据拟合分类器模型)

dot_data = StringIO()
with open('a.txt','a+') as f:
    f.write(dot_data)
print(dot_data)
tree.export_graphviz(tree1,out_file="tree.doc")
###################################################
