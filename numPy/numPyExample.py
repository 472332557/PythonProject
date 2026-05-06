import numpy as np

print('--------------------------------1、数组初始------------------------------------------')
# numpy是Python当中进行科学计算的软件工具包,基础库
a = [1,2,3,4,5]
arr = np.array(a)
print(arr)
print(type(arr))
# 访问,也就是通过索引下标
print(arr[3])

# 一些函数
# 创建一个二维数组
print("创建一个二维数组")
b = [[1,2,3,4,5],[6,7,8,9,10]]
arr2 = np.array(b)
print(arr2)
print(type(arr2))
#
print(arr2[1][3])
# 维度 ，
print("维度:",arr2.ndim)
# 形状
print("形状：",arr2.shape)
# 元素个数
print("元素个数：",arr2.size)
# 元素类型
print("元素类型：",arr2.dtype)

# 常用创建数组的函数
# zeros()
print("创建一个全为0的数组,数组形状为3行3列")
zeroArr = np.zeros((3,3))
print(zeroArr)
# ones()
print("创建一个全为1的数组,数组形状为3行3列")
onrArr = np.ones((3,3))
print(onrArr)

# empty()，创建一个内容随机的数组
print("创建一个随机的数组")
emArr = np.empty(3)
print(emArr)

# arange()函数，将序列转换为数组
print("将序列转换为数组")
ranArr = np.arange(0,10,2)
print(np.array(ranArr))

# linspace(),均分函数，将创建均分数组（均匀间隔数组），区别于range和序列，是一个左闭右闭的区间盘[]
print("创建均分数组，0开始，10结束，均分为5个")
lineArr = np.linspace(0,10,5)
print(lineArr)

print('--------------------------------2、排序、连接、数组形状调整、索引和切片------------------------------------------')
a1 = np.array([5,2,6,1,9,3])
print("原始数组：",a1)
# 升序
a2 = np.sort(a1)
print("升序后：",a2)

# 降序
a3 = np.sort(a1)[::-1]
print("降序后：",a3)

# 拼接
a4 = np.array([1,2,3])
a5 = np.array([4,5,6])
a6 = np.concatenate((a4,a5))
print("拼接后：",a6)

# 重塑数组 reshape
a7 = np.array([1,2,3,4,5,6,7,8])
print("重塑数组：",a7)
a8 = a7.reshape(8,1)
print(type(a8))
print("重塑后为一个二维数组，8行1列：",a8)
print(a8.ndim,a8.shape,a8.size,a8.dtype)

# 数组的扩维，增加新的维度，意味着从一维数组到二维数组，二维数组到三维数组
a9 = np.array([1,2,3,4,5,6])
# np.newaxis,插入一个轴,放在第一位就是插入一行，a10就是（1,6）1行6列的二维数组
a10 = a9[np.newaxis,:]
print("a9[np.newaxis,:]",a10.ndim,a10.shape,a10.size,a10.dtype,a10)
# 放在第二位，a11就是（6,1）6行1列的二维数组
a11 = a9[:,np.newaxis]
print("a9[:,np.newaxis]",a11.ndim,a11.shape,a11.size,a11.dtype,a11)
# np.expand_dims(),也是数组的扩维
# axis=1,意思为列增加一个轴，也就是（6,1）6行1列
a12 = np.expand_dims(a9,axis=1)
print("np.expand_dims(a9,axis=1)",a12.ndim,a12.shape,a12.size,a12.dtype,a12)
# axis=0,意思为行增加一个轴，也就是（1,6）1行6列
a13 = np.expand_dims(a9,axis=0)
print("np.expand_dims(a9,axis=0)",a13.ndim,a13.shape,a13.size,a13.dtype,a13)

# 索引和切片
# 一维数组获取元素和列表list类似，直接获取或者范围获取一样
print("获取a9数组索引下标为1的元素：",a9[1])
print("获取a9数组索引下标为1到3的元素：",a9[1:3])
a14 = np.array([[1,2,3],[4,5,6],[7,8,9]])
# 二维数组获取元素稍有差别，a14[行索引，列索引]
print("获取第1行的第2列：",a14[1,1])
# 获取二维数组的切片，也就是范围数据[:,0:2],:表示所有行，0:2表示获取第1、2列
# 获取所有行的第1、2列
print("获取所有行的第1、2列:",a14[:,0:2])
print("获取第2行的第1、2列:",a14[1,0:2])
print("获取第2、3行的第1、2列:",a14[1:3,0:2])

print('--------------------------------3、堆叠、拆分、计算[注意：不管是堆叠还是计算， 都要处于同一个维度和形状]---------------------------------------')
# 垂直堆叠,np.vstack()
print("------垂直堆叠------")
a15 = np.array([[1,2,3],[4,5,6]])
a16 = np.array([[7,8,9],[10,11,12]])
a17 = np.vstack((a15,a16))
print("数组垂直堆叠后：",a17)
# 水平堆叠,np.hstack()
print("------水平堆叠------")
a18 = np.hstack((a15,a16))
print("数组水平堆叠后：",a18)
# 拆分，np.hsplit(arr,x),arr：要拆分的数组，x：指定拆分为x个数组
# 构建一个数组，从1 - 25,2行12列
print("------拆分------")
print("[[ 1  2  3  4  5  6  7  8  9 10 11 12] [13 14 15 16 17 18 19 20 21 22 23 24]]")
a19 = np.arange(1,25).reshape(2,12)
print("2行12列的数组：",a19)
# 拆分为2个形状相同的数组
a20 = np.hsplit(a19,2)
print("拆分为2个形状相同的数组：",a20,type(a20))

# 拆分，指定范围的拆分 np.hsplit(arr,(x,y)),arr：要拆分的数组,元组(x,y)，则意味着需要拆分的列分为3部分，x以左的，（x，y）之间的，y以右的
a21 = np.hsplit(a19,(3,5))
print("拆分为以列（3,5）分隔的数组：",a21)

# 数组的计算，遵循按位进行 加、减、乘、除，arr1 = [1,2]，arr2=[3,4],arr1 + arr2 = [1+3,2+4] = [4,6]，就是1和3对应，2和4对应
print("------数组的加、减、乘、除")
a22 = np.array([1,2])
a23 = np.array([3,4])
a24 = a22 + a23
print("数组相加：",a24)
a25 = a22 - a23
print("数组相减：",a25)
a26 = a22 * a23
print("数组相乘：",a26)
a27 = a22 / a23
print("数组相除：",a27)

print('--------------------------------4、数组聚合与矩阵变形---------------------------------------')
# 聚合函数
a28 = np.array([1,2,3])
print("数组：",a28)
print("最小值：",a28.min())
print("最大值：",a28.max())
print("求和：",a28.sum())
print("平均值：",a28.mean())
print("乘积：",a28.prod())
print("标准差：",a28.std())

#多维数组指定列、行 ，列：axis = 0，行：axis = 1
a29 = np.arange(1,7).reshape(2,3)
print("二维数组：",a29)
print("列最小值：",a29.min(axis=0))
print("行最大值：",a29.max(axis=1))
print("列求和：",a29.sum(axis=0))
print("行平均值：",a29.mean(axis=1))
print("列乘积：",a29.prod(axis=0))
print("列标准差：",a29.std(axis=0))

# 矩阵就是一个二维数组，跟创建一个二维数组没啥区别，索引、切片也一样[行索引,列索引]

# 转置和重塑
# 转置，比如一个3行2列的数组，转置以后就是2行3列，行变列、列变行。使用arr.T操作
# 比如：[[1,2],[3,4],[5,6]]3行2列的数组 转置以后：[[1,3,5],[2,4,6]]成了2行3列
a30 = np.arange(1,7).reshape(3,2)
print("a30:",a30)
a31 = a30.T
print("转置后：",a31)
# 重塑，关键点就是数组元素个数保持不变，使用reshape()
print('--------------------------------5、数学公式的实现与均方误差公式MSE ---------------------------------------')
# 使用数学公式计算,MeanSquareError = 1/n * np.sum(np.square(Y_prediction - Y))
# 预测值
y_pred = np.array([1,2,3])
print("y_pred:",y_pred)
n = len(y_pred)
print("n:",n)
# 真实值
y = np.array([1,1,1])
print("y:",y)
error = 1/n * np.sum(np.square(y_pred - y))
print("均方误差值：",error)
