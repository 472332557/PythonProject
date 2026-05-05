# Python是面向对象的编程语言，拥有属性和方法
# class 声明类，类是一个定义，说明，模板，对象是类的具体实现
class Person:
    name = 'person'
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def display(self):
        print("hello my name is ",self.name)

# 对象创建
p1 = Person("Michael",18)
p2 = Person("Jack",22)
print(p1.name)
print(p2.name)
p1.display()
p2.display()

# 继承：允许一个类去继承另一个类的所有方法和属性
class Student(Person):
    def __init__(self,name,age,tel):
        #显式调用父类的_init_来保留原功能
        # Person.__init__(self,name,age)
        # 也可使用super（）函数
        super().__init__(name,age)
        self.tel = tel
        
    def sayHello(self):
        print("hello my name is ",self.name)

s1= Student("Aiden",18,12323432132)
s1.display()
print(s1.tel)
s1.sayHello()