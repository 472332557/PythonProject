from cProfile import label

import numpy as np
import matplotlib.pyplot as plt
from fontTools.diff import color

# 解决中文乱码
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']
# 解决负号显示异常
plt.rcParams['axes.unicode_minus'] = False

print("-----------------------折线图绘制--------------------------------")
x = [1,2,3,4,5]
y = [3,4,5,6,7]

# 绘制折线图
plt.plot(x,y,label="线性增长")
plt.title("第一个图表")
# 设置x轴标签
plt.xlabel("x 轴")
# 设置y轴标签
plt.ylabel("y 轴")
# 开关，使label="线性增长"显示图例
plt.legend()
# 显示网格
plt.grid(True)
# 显示图表
plt.show()

# 折线图深入学习
months = ['1月','2月','3月','4月','5月','6月']
sales = [1200,1500,1300,1800,2000,2300]
salesB = [800,1100,1300,1600,1900,2100]

plt.plot(months,sales,label="a部门每月销售额度",color="red",linestyle="--",marker="o")
plt.plot(months,salesB,label="b部门每月销售额度",color="blue",linestyle="--",marker="o")
plt.title("a/b部门上半年月销售额度趋势图")
plt.xlabel("月份")
plt.ylabel("销售额(万)")
plt.legend()
plt.show()
print("-----------------------散点图绘制--------------------------------")
# 散点图是适合展示两个变量之间的关系
# 随机展示50个人的身高、体重关系数据
print("-------------随机展示50个人的身高、体重散点图数据")
height = np.random.randint(155,190,50)
# 正负5Kg范围内，np.random.randn(50)是正负 -1 到 1，50个是指定生成50个数
weight = height * 0.45 + np.random.randn(50) * 5
print(np.random.randn(50))
plt.scatter(height,weight,s=60,c='red',alpha=1,label='样本数据')
plt.title("身高与体重关系图")
plt.xlabel("身高（cm）")
plt.ylabel("体重（kg）")
plt.legend() # 显示图例
plt.grid(True) # 展示网格
plt.show()
print("-----------------------柱状图绘制--------------------------------")
cities = ['北京','上海','广州','深圳']
q1_sales = [3200,2900,2600,2800] # Q1销售额
q2_sales =[3500,3100,2400,3000]  # Q2销售额

# 单个的垂直柱状图
print("单个的垂直柱状图")
plt.bar(cities,q1_sales,width=0.4,color='red',label='Q1')
plt.show()

print("单个的水平柱状图")
plt.barh(cities,q1_sales,height=0.4,color='red',label='Q1')
plt.show()

print("Q1、Q2对比的垂直柱状图")
# 如果X都写cities的话，就会重合，此时需要区分开来Q1、Q2
x = np.arange(1,len(cities)+1)
width = 0.4
plt.bar(x,q1_sales,width=0.4,color='red',label='Q1')
plt.bar(x+width,q2_sales,width=0.4,color='blue',label='Q2')
# 构造X轴的名称到柱状图的中间
plt.xticks(x+width/2,cities)
plt.title("各城市Q1 VS Q2销售额")
plt.xlabel("城市")
plt.ylabel("销售额（万元）")
plt.legend()
plt.show()
print("-----------------------饼图绘制--------------------------------")
print("饼状图的绘制")
sizes = [3200, 3000, 1000, 1500, 1000]
labels = ['餐饮','房租','交通','娱乐','其他']
plt.pie(sizes,labels=labels,autopct='%1.1f%%',explode=(0.2,0,0,0,0),startangle=90)
plt.show()

print("-----------------------直方图绘制--------------------------------")
print("直方图的绘制")
#设置随机种子，保证每次运行生成的随机数完全相同(便于复现结果)
np.random.seed(42)
# 创建数据，模拟200个学生的考试成绩（正态分布，均值75、标准差10）
scores = np.random.normal(loc=75,scale=15,size=200)
print("scores:",scores)
# 限制成绩在 0 到 100之间
scores = np.clip(scores,0,100)
# 绘制图,bins：数据分为多少个区间，
plt.hist(scores,bins=15,color='red',edgecolor='white',alpha=0.8)
plt.title('学生成绩分布')
plt.xlabel("分数")
plt.ylabel("人数")
# 只显示y轴方向的网格，避免干扰x轴
plt.grid(axis='y')
plt.show()
print("-----------------------箱线图绘制--------------------------------")
print("箱线图绘制")
np.random.seed(42)
#创建数据，模拟三个班的数学成绩
class_a =np.random.normal(loc=80, scale=10, size=50) #A班：均值80
class_b =np.random.normal(loc=70,scale=15, size=50) # B班：均值70
class_c = np.random.normal(loc=85, scale=5, size=50) #C班：均值85
# 添加进一个列表
data = [class_a,class_b,class_c]
#绘制箱线图
plt.boxplot(data,vert=True,patch_artist=True,showmeans=True,labels=['A班','B班','C班'])
plt.title("三个班级数据成绩对比")
plt.xlabel("分数")
plt.grid(axis='x',alpha=1)
plt.show()
print("-----------------------子图绘制--------------------------------")
print("子图绘制")
#定义数据:X轴为月份，Y轴为销售额
months =['1月','2月','3月','4月','5月','6月']
sales = [1200,1500,1300,1800,2100,1900]
# 创建1行2列的子图布局，设置画布大小为宽12英寸、高4英寸
#fig:整个画布对象;axes:子图数组(axes[e]是第一个子图，axes[1]是第二个子图)
fig ,axes = plt.subplots(1,2,figsize=(12,4))

# 第一个子图(左侧):折线图(展示趋势)
axes[0].plot(months,sales,color='red',marker='o',label='每月销售数据')
axes[0].set_title('折线图：销售趋势')
axes[0].set_xlabel('月份')
axes[0].set_ylabel('销售额')
axes[0].grid(True)
axes[0].legend()

# 第二个子图(右侧):柱状图(展示对比)
axes[1].bar(months,sales,width=0.4,color='blue',label='每月销售数据')
axes[1].set_title('柱状图：销售趋势')
axes[1].set_xlabel('月份')
axes[1].set_ylabel('销售额')
axes[1].grid(axis='y')
axes[1].legend()
# 自动调整子图间距
plt.tight_layout()
plt.show()



