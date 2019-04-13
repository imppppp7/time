class Person:
    def __init__(self,name,job,pay):
        # name,job,pay 都是局部变量 用赋值将它赋值给self.name,self.job,self.pay属性
        # 这样就可以在实例中保存传入的name job pay已供以后使用
        # 所以要有赋值的这一步骤
        self.name = name
        self.job = job
        self.pay = pay
    #     添加行为方法

    def lastname(self):
        return self.name.split()[-1]

    def giveraise(self,percent):
        self.pay = int(self.pay*(1 + percent))

    #     运算符重载
    def __str__(self):
        return '[person : %s,%s]' % (self.name,self.pay)


class Manager(Person):
    def __init__(self,name,pay):
        Person.__init__(self,name,'may',pay)

    def giveraise(self,percent,bouns = .10):
        Person.giveraise(self,percent+bouns)

# 把不同的多个类组合起来


class Department:
    def __init__(self,*args):
        self.members = list(args)

    def addmembers(self,person):
        self.members.append(person)

    def giveraises(self,percent):
        for person in self.members:
            person.giveraise(percent)

    def showAll(self):
        for person in self.members:
            print(person)


# mian 只有当文件时顶层脚本的时候才运行
if __name__ == '__main__':
    bob = Person('Bob smith','last',100)
    fan = Person('Fan zhang','coding',100)
    tom = Manager(' zhang',100)
    development = Department(bob,fan)
    development.addmembers(tom)
    development.giveraises(.10)
    development.showAll()
# print(fan.lastname())
# fan.giveraise(0.1)
# print(fan)
#
#
# fan2 = Manager('ff',10)
# fan2.giveraise(0.1)
# print(fan2)


