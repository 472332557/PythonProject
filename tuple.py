# 元组，是一个有序不可改变的集合，使用()构建
tuple1 = ("dog","cat","sheep")
print("元组类型：",type(tuple1))
print("获取元组第一个元素：",tuple1[0])
# 修改元组元素,虽然元组元素不可被修改，但可以转换为list列表后，修改，再转换为元组
print("修改元组元素,虽然元组元素不可被修改，但可以转换为list列表后，修改，再转换为元组")
print("未修改前元组元素：",tuple1)
list1 = list(tuple1)
list1[1] = "fish"
tuple1 = tuple(list1)
print("修改后元组元素：",tuple1)

#创建元组，如果元组中只有一个元素，则创建元组时，需要在元素后加一个逗号，否则python无法识别为元组
t2 = ("apple",)
print(type(t2))
t3 = ("apple")
print(type(t3))

# count:返回元组中指定元素出现的次数
print("dog出现的次数：",tuple1.count("dog"))

# index：返回元组中指定元素的位置
print("dog的位置：",tuple1.index("dog"))
