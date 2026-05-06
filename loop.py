# 循环
# while循环必须满足判断条件才可以进行
i = 1
while i < 6:
    print(i)
    i+=1

a = int(input("请输入密码："))
while a != 123456:
    print("密码错误，请重新输入密码！")
    a = int(input())
print("密码正确")

# break语句，即使条件为真的情况下，也能使循环停止
print("------break语句------")
b = 1
while b < 10:
    print(b)
    if b == 5:
        print("此时b=",b,"break循环")
        break
    b+=1
# continue语句
print("------continue语句------")
c = 0
while c < 10:
    c += 1
    if c == 5:
        continue
    print(c)

print("------------for循环------------")
# for循环用于迭代序列（列表、元组、集合、字典、字符串）
pets = ['dog','cat','bird']
for pet in pets:
    print(pet)
print('------break------')
for pet in pets:
    print(pet)
    if pet == "cat":
        break
print('------continue------')
for pet in pets:
    if pet == "cat":
        continue
    print(pet)

# range函数，循环一组代码指定的次数，range()函数返回一个数字序列，默认情况下从0开始，并递增1（默认），并以指定的数字结束
# range(a,b,c) a:起始，b：结束，c：步长
print('------range函数------')
for x in range(5):
    print(x)

print('------range函数,0开始、5结束、步长为1------')
for y in range(0,5,1):
    print(y)

print('------range函数,0开始、5结束、步长为2------')
for z in range(0,5,2):
    print(z)

# 嵌套循环,外循环每迭代一次，内层循环完整的执行一次循环
fruit = ['apple','banana','mango']
for f in fruit:
    for p in pets:
        print(f,p)

# pass语句，for循环由于某种原因暂时没有内容， 则可以写pass语句，防止报错
print('------pass语句------')
for x in range(0,5):
    pass