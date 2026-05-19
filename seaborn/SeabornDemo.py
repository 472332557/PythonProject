import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
%matplotlib inline

# 解决中文乱码
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']
# 解决负号显示异常
plt.rcParams['axes.unicode_minus'] = False

def seabornFun(flip = 1):
    x = np.linspace(0,14,100)
    for i in range(1,7):
        plt.plot(x,np.sin(x+i*.5)*(7-i)*flip)

seabornFun()

# 使用seaborn构造
print("------使用seaborn渲染------")
sns.set()
seabornFun()

sns.set_style("darkgrid")
seabornFun()
