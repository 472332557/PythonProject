import numpy as np
import pandas as pd

print("--------------------------------Series-------------------------------------------------")
# 使用数组转换为Series
print("------使用数组转换为Series------")
a1 = np.array([1,2,3])
s1 = pd.Series(a1)
print("s1:",s1)

#使用字典转换Series，字典的key成为了Series的索引，值成为了元素
print("------使用字典转换Series------")
data = {"a":1,"b":2,"c":3}
s2 = pd.Series(data)
print("s2:",s2)

# 使用标量转换为Series
print("------使用标量转换Series------")
s3 = pd.Series(6,index=["a","b","c"])
print("s3:",s3)

# 访问Series数据
# 通过索引访问
s4 = pd.Series([1,2,3,4,5],index=["a","b","c","d","e"])
print("s4:",s4)
# 索引下标,指定非数字索引后，只允许索引切片访问，不能单独索引访问
print("s4-1:",s4[0:1])
print("索引下标切片访问:\n",s4[0:3])
# 标签下标
print("s4-b:",s4['b'])
print("s4-a-b-c:",s4[['a','b','c']])

# Series的常用属性
print("索引列表:",s4.axes)
print("数据类型:",s4.dtype)
print("判断是否为空:",s4.empty)
print("大小：",s4.size)
print("返回值:",s4.values)
print("索引值:",s4.index)

# Series常用方法
# head()、tail()，查看Series的部分数据
print("------------head、tail、------------------")
print("查看前2个：",s4.head(2))
print("查看后2个：",s4.tail(2))
# isnull() 、nonull()
# 是空值返回true
print(pd.isnull(s4))
# 不是空值返回true
print(pd.notnull(s4))

print("--------------------------------DataFrame-------------------------------------------------")
# DataFrame是一个二维列表，可以想象成Excel表格，也是多个Series构建得到的数据结构，然后拼接得到的这些列组成的行，共用了一个索引
# 通过列表构建DataFrame
print("通过列表构建DataFrame")
data = [['jim',20],['Marry',18],['John',28]]
# columns=['name','age']列要指定名称，由于构建的data列表中没有表明表头的字段
df = pd.DataFrame(data,columns=['name','age'])
print(df)

# 通过字典构建DataFrame
print("通过字典构建DataFrame")
dataDict = {"Name":['Tom','Jack','Mic','Marry','John'],"Age":[21,25,30,26,29]}
df1 = pd.DataFrame(dataDict)
print(df1)
# 通过Series构建DataFrame
print("通过Series构建DataFrame")
s1 = pd.Series([1,2,3])
s2 = pd.Series([4,5,6])
df2 = pd.DataFrame({'A':s1,'B':s2})
print(df2)

# 访问DataFrame,可以按行或者按列访问，因为构建的DataFrame数据，都会有表头（列名），所以可根据列名去直接访问
print("按列访问：",df1['Name'])
# 按行访问，可以根据标签或者位置访问

df3 = pd.DataFrame(dataDict,index=['a','b','c','d','e'])
print("按行访问，基于标签：",df3.loc['a'])
print("按行访问，基于索引",df3.iloc[0])

# 新增
print("DataFrame新增，一个series")
df1['Score'] = [85,67,87,90,95]
print(df1)

# 删除
print("DataFrame删除Score")
df1.pop('Score')
print(df1)

# DataFrame的属性
# 转置，也就是将列转为行，行转为列，行索引转为列索引
print("df1转置")
print(df1.T)

print("--------------------------------pandas CSV文件处理-------------------------------------------------")

# 读取csv文件
print("读取csv文件")
df2 = pd.read_csv('../data.csv')
print(df)
print("获取列Name:",df2['Name'])
print("读取前1行：",df2.head(1))
print("读取后1行：",df2.tail(1))
print("info信息：",df2.info())

# 写csv文件
# 三个字段name，site，age
print("写csv文件")
name = ["Google","Runoob","Taobao","Wiki"]
site = ["www.google.com","www.runoob.com","www.taobao.com","www.wikipedia.org"]
age = [90, 40, 80, 98]
# 字典
dict1 = {"name":name,"age":age,"site":site}
df3 = pd.DataFrame(dict1)
print(df3)
df3.to_csv("../data_out.csv")

print("--------------------------------pandas Excel输入与输出-------------------------------------------------")
# Excel输出
print("------执行Excel写------")
write = pd.ExcelWriter('../data_out.xlsx')
df3.to_excel(write)
write.close()
print("output success")

# 写多个sheet页
print("------执行Excel写多个sheet页------")
user_df = pd.DataFrame({"username":['user1','user2','user3'],"password":['111','222','333']})
writeMulti = pd.ExcelWriter('../data_multi_out.xlsx')
# 分别写入不同的sheet页
df3.to_excel(writeMulti,sheet_name='网站信息',index=False)
user_df.to_excel(writeMulti,sheet_name="用户信息",index=False)
# 关闭write ,必须关闭，否则文件会损坏
writeMulti.close()
print("多sheet页写成功！")

# 读Excel
print("读Excel")
df_read = pd.read_excel('../data_out.xlsx')
print(type(df_read))
print(df_read)

print("--------------------------------pandas的数据清洗-------------------------------------------------")
# 缺失值、空值处理
print("-----处理空值-------")
sales_data = {
    '订单ID': [1001, 1002, 1003],
    '客户': ['张三', np.nan, '王五'],
    '金额': ['5999元', '8999', ''],
    '日期': ['2024-01-15', '2024/01/16', 'NA']
}

df = pd.DataFrame(sales_data)
print(df)
# 构建空值的定义，意味着以下列表出现的值，都为空值，需要处理
missValue = ['na','n/a','NA','']

# df_new = df.dropna(how='any')
print("清理后的数据")
# print(df_new)
# 修改源数据，不用重新定义新的DataFrame
df.dropna(inplace=True)
print(df)

# 数据填充
print("替换空值")
sales_data = {
    '订单ID': [1001, 1002, 1003],
    '客户': ['张三', np.nan, '王五'],
    '金额': ['5999元', '8999', ''],
    '日期': ['2024-01-15', '2024/01/16', 'NA']
}
df_rep = pd.DataFrame(sales_data)
df_rep.fillna("李四",inplace=True)
print(df_rep)

# 统一日期格式/格式化日期
print("-------替换日期格式------")
data = {"Date":['2020/12/01','2020/12/02','20201226'],
        "duration":[40,50,999]}
df_date = pd.DataFrame(data)
# 强制转换为日期格式,mixed 表示上述几种格式都包含
df_date['Date'] = pd.to_datetime(df_date['Date'],format='mixed')
print(df_date)

# 直接替换
# 修改数据
print("----修改数据------")
df_date.loc[2,'duration'] = 55
print(df_date)

# 删除行
print("----删除行----")
for x in df_date.index:
    if df_date.loc[x,'duration'] > 50:
        df_date.drop(x,inplace=True)
print(df_date)

# 处理重复的数据
print("---处理重复的数据---")
student_data = {
    '姓名': ['张三', '李四', '张三', '王五'],
    '数学': [85, 92, 85, 150],  # 150是异常值，张三重复
    '英语': [90, 88, 90, 89]
}
df_dup = pd.DataFrame(student_data)
print(df_dup)
print(df_dup.duplicated())
# 删除重复的值
print("删除重复的值")
df_dup.drop_duplicates(inplace=True)
print(df_dup)

print("--------------------------------pandas的数据聚合和排序-------------------------------------------------")

# 原始数据：销售记录
sales_data = {
    '产品': ['手机', '笔记本', '手机', '平板', '笔记本', '手机', '平板'],
    '地区': ['北京', '上海', '北京', '广州', '上海', '广州', '北京'],
    '销售额': [5000, 8000, 6000, 3000, 9000, 5500, 3500],
    '数量': [2, 1, 3, 2, 1, 2, 1]
}

df_sales = pd.DataFrame(sales_data)
print(df_sales)

# 排序
print("---按值排序---")
df_sorted = df_sales.sort_values(by='销售额',ascending=False)
print(df_sorted)

# 数据聚合
print("按产品分组后，销售额求平均")
group = df_sales.groupby('产品').agg({'销售额':'mean'})
print(group)

# 多重聚合
print("按产品分组后，销售额求平均、总和")
group_sum = df_sales.groupby('产品').agg({'销售额':['mean','sum']})
print(group_sum)

