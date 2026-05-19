# 集合set，无序不可重复，并且元素本身无法修改 ，使用 {}大括号表示
s1 = {"dog","cat","sheep",'cat'}
print(s1)
print(type(s1))
# 无法通过索引下标获取，因为set集合是无序的
# print(s1[1])

# 遍历集合
print("------遍历集合------")
for x in s1:
    print(x)
# 判断元素是否在集合
print("------判断元素是否在集合------")
print("dog" in s1)
# 添加元素
print("------添加元素------")
print("添加一个add:",s1.add("fish"))
print(s1)

print("添加多个update:",s1.update(["bird","lion"]))
print(s1)

# 删除元素,romve和discard，区别remove删除不存在的会报错，而discard不会报错
print("------删除元素------")
print("remove:",s1.remove("bird"))
print(s1)
print("discard：",s1.discard("dog"))
print(s1)

# s1.remove("dsds")
# print(s1)
s1.discard("dsds")
print(s1)

# 随机获取一个元素并且移除，会修改集合本身
print("----- pop使用 ------")
print("随机获取一个元素：",s1.pop())
print("原集合：",s1)




# 合并
print("------合并元素------")
s2 = {"apple","pear","banana"}
print(s2)
s1.update(s2)
print(s1)

s3 = s1.union(s2)
print("s3:",s3)



