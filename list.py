# 列表是有序可重复且可更改的一个集合，使用[]号创建
print("--------------列表-------------------")
list1 = ["dog","cat","sheep"]
# 获取
print("----获取元素-----",list1)
print(type(list1))
print("获取第一个元素：",list1[0])
print("获取第二个元素：",list1[1])

print("获取索引0到1：",list1[0:1])
print("获取索引0到2：",list1[0:2])
print("负数索引从后往前，获取索引-1，：",list1[-1])
# 修改
print("----修改元素-----")
list1[2] = "fish"
print(list1)
# 增加
print("----增加元素-----")
print("添加到尾部：",list1.append("cow"))
print(list1)
print("指定位置添加：",list1.insert(1,"pig"))
print(list1)
# 删除
print("----删除元素-----")
print("指定元素删除：dog",list1.remove("dog"))
print(list1)
print("基于索引删除：1",list1.pop(0))
print(list1)
print("del 指定元素0删除")
del list1[0]
print(list1)
# 复制列表
print("复制列表list2")
list2 = list1.copy()
print(list2)

print("clean清空列表 删除元素但保留列表")
list1.clear()
print(list1)
print("del 删除整个列表")
del list1
print(list1)