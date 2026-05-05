# 字典是一个无序、可变和有索引的集合。用{}表示，使用key、value键值对
dict1 = {"name":"apple","price":10,"color":"red"}
# 获取元素
print("------获取元素------")
print(dict1)
print("获取元素name：",dict1['name'])
print("获取元素price：",dict1.get("price"))

# 更改元素
print("------更改元素------")
dict1["price"] = 15
print(dict1)

# 遍历元素
print("------遍历元素------")
# 直接遍历字典，获取到的是key
for x in dict1:
    print(x)
# 遍历字典，获取value
print("遍历字典，获取value")
for x in dict1:
    print(dict1[x])
# 使用values函数获取value
print("------使用values获取------")
for x in dict1.values():
    print(x)

#遍历字典，获取key、value
print("------获取key、value------")
for x,y in dict1.items():
    print(x,y)

# 判断是否存在key
print("------判断key是否存在------")
print("name" in dict1)

# 添加对象元素
print("------添加对象元素------")
dict1["from"] = "甘肃"
print(dict1)

# 删除对象元素
print("------删除对象元素------")
dict1.pop("from")
print(dict1)

# 复制字典
print("------复制字典------")
dict2 = dict1.copy()
print(dict2)

# 嵌套字典
print("------嵌套字典------")
dict3 = {
    "fruit1":{
        "name":"apple",
        "price":10,
        "color":"red"
    },
    "fruit2":{
        "name":"banana",
        "price":20,
        "color":"green"
    },
    "fruit3":{
        "name":"mango",
        "price":30,
        "color":"blue"
    }
}
print(dict3)

# 构造函数
print("------构造函数------")
dict14 = dict(name="watermelon",price="20",color="green")
print(dict14)





