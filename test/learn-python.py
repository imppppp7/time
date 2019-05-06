import cv2


'''

OOP 继承 是 is-a的关系,大类套着小类 大类越抽象越好 小类来实现具体的功能 定义具体的人 

OOP 组合 是 has-a的关系,写一个类用来作为其他几个类的容器，容器中定义组合这些类的方法

'''


class Employee:
    def __init__(self, name, salary = 0):
        self.name = name
        self.salary = salary

    def giveraise(self, percent):
        self.salary = self.salary *(1 + percent)

    def work(self):
        print(self.name, 'does stuff')


class Chef(Employee):
    def __init__(self, name):
        Employee.__init__(self, name, 5000)

    def work(self):
        print(self.name, 'make food')


class Server(Employee):
    def __init__(self, name):
        Employee.__init__(self, name, 4000)

    def work(self):
        print(self.name, 'interfaces with customer')


class Pizzarobot(Chef):
    def __init__(self, name):
        Chef.__init__(self, name)

    def work(self):
        print(self.name, 'make pizza')


# bob = Pizzarobot('bob')
# bob.work()
# bob.giveraise(0.1)
# print(bob.salary)


class Customer:
    def __init__(self, name):
        self.name = name

    def order(self, server):
        print(self.name, 'order from', server)

    def pay(self, server):
        print(self.name, 'pays for item to', server)


class Oven:
    def bake(self):
        print('oven bakes')


class PizzaShop:
    def __init__(self):
        self.server = Server('pat')
        self.chef = Chef('Bob')
        self.oven = Oven()

    def order(self, name):
        customer = Customer(name)
        customer.order(self.server)
        self.chef.work()
        self.oven.bake()
        customer.pay(self.server)


scene = PizzaShop()
scene.order('Homer')


# 伪私有属性
class C1:
    def meth1(self): self.M = 88

    def meth2(self): print(self.M)


class C2:
    def metha(self): self.M = 99

    def methb(self): print(self.M)


class C3(C1, C2): ...


I = C3()
I.meth1()
I.meth2()
I.metha()
I.methb()
print(I.__dict__)
print(I.M)