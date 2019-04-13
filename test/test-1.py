import math
# for (a,*b,c) in [(1,2,3,7),(4,5,6,8)]:
#     print((a,*b,c))
# D = {'A':'1','B':'2','C':'3'}
# for key,value in D.items():
#     print(key,value)
L1 = [1,2,3,4,5,8]
L2 = [5,6,7,8]
# for (x,y) in zip(L1,L2):
#     print(x,y)
# for i in range(len(L1)):
#     print(L1[i]+10)
# print(list(i+10 for i in L1))
#

# def cal(x,y):
#     for x1 in x:
#         if x1 in y:
#             print(x1)
# cal(L1,L2)

# def f(a):
#
#
# b = 88
# f(b)
# print(b)
# a,b = (1,[1,2])
# print(a,b)
# def multiple(x,y):
#     x = 2
#     y[0] = 'spam'
#     return x,y[0]
# X = 1
# Y = [3,4]
# print(multiple(X,Y))
# print(X,Y)

# L = [1,2,3]
# L = L[1:]
# print(L)

# def my(L):
#     if not L:
#         return 0
#     else:
#         return L[0]+my(L[1:])

# def my(L):
#     first,*rest = L
#     return first if not rest else first + my(rest)
# print(my([1,2,3]))
# def my(L):
#     a = 0
#     for i in L:
#         if not isinstance(i,list):
#             a += i
#         else:
#             a += my(i)
#     return a
# print(my([1,2,[1,[1,2]]]))
# f = lambda x,y,z : x+y+z
# print(f(1,2,3))
# def func(x):
#     return x+10
# L = [1,2,3,4,5]
# print(list(map(func,L)))
'''
内置的一些函数要比循环来的更快 map filter reduce
推导表达式比内置函数来得更快

要写简单的循环时候，先考虑一下内置函数和列表推导表达式
'''
# res = [ x+y for x in [1,2,3] for y in [4,5,6] ]
# print(res)
def gensquares(N):
    for i in range(N):
        yield i**2
# print(gensquares(4))
# print(next(x))
# print(next(x))
'''
列表推导表达式一次生成全部结果[x for x in y]
生成器表达式 （x for x in y) 一部分一部分地产生结果

'''
p = math.pi
# print(p)
# def luan(i):
#     for x in range(len(i)):
#         yield i[x:]+i[:x]
# F = list(luan('spam'))
F = lambda seq: (seq[i:]+seq[:i] for i in range(len(seq)))
# print(list(F('sqam')))

# def saver(x = []):
#     x.append(1)
#     print(x)
# print(saver([2]))
# print(saver())
list = [1,2,3]
list.append(4)
# print(list)

from test import alien,ylien
x = 42
ylien[0] = 12
print(ylien)

