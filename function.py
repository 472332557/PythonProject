# 函数
def add(param1,param2):
    return param1+param2

result = add(3,5)
print(result)

# pass语句，作为一个占位符，实现空函数，意思先这样声明函数，后期又想到具体的函数体再来补充,不写pass运行会报错
def cal(x):
    pass

#函数参数，分为位置参数（必填参数）、默认参数、可变参数、关键字参数
# 设置一个计算幂次方的函数,x ,n都是位置参数，必填的
print("------位置参数------")
def power(x,n):
    s = 1
    while n > 0:
        n = n-1
        s = s * x
    return s
print(power(3,4))

# 默认参数，必须放在必填参数的后边，默认参数一般是不常调用，简化函数
print("------默认参数------")
def powerInit(x,n=2):
    s = 1
    while n > 0:
        n = n-1
        s = s * x
    return s
print(powerInit(5))

# 可变参数 * + 参数 = 可变参数，*params，可变参数意味着定义函数时，不固定参数的个数，多少都可传递，python会将传入的可变参数封装为一个元组或者列表
# 计算 1^2 + 2^2 + 3^2
print("------可变参数------")
def calc(*params):
    sum = 0
    for x in params:
        sum = sum + x * x
    return sum
print(calc(1,2,3))

# 关键字参数，函数调用者可以传入任意不受限制的关键字参数，关键字参数也叫做带名字的参数，参数名=值
print("------关键字参数------")
def person(name,age,**kw):
    print("name:",name,"age:",age,"other:",kw)
person("Aiden",30,city="深圳",addr="宝安",tel=1980977232)

# 命名关键字参数，限制关键字参数传入的个数也叫范围吧
print("------命名关键字参数------")
def person2(name,age,*,city,addr):
    print("name:",name,"age:",age,"city:",city,"addr:",addr)
person2('Marry',20,city = 'Korea',addr = 'xxx')

# 如果有可变参数的时候，后边的命名关键字参数不需要使用*号隔开
def person3(name,age,*params,city,addr):
    print("name:",name,"age:",age,"params:",params,"city:",city,"addr:",addr)
person3("Jack",28,13280987647,175,city="日本",addr="京都")



