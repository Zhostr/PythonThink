# 高阶函数
# Higher-order Function: A function that takes a function as an argument value or returns a function as a return value.
# map, filter 是内置高阶函数
numbers = [1, 2, 3, 4, 5]
doubled = map(lambda x:x**2, numbers)
print(list(doubled))

odds = filter(lambda x:x%2==1, numbers)
print(list(odds))

# lambda 表达式可以接受多个参数，但只能有一个表达式（可以返回基本类型/函数等）
lb1 = lambda x, y: x+y
lb2 = lambda n: (lambda x: x*n)
print(lb1(10,1))
print(lb2(10)(20))



def cube(n):
    return pow(n, 3)
def square(x):
    return x * x

# function as parameter
def sum(n, fun):
    total, k = 0, 1
    while k <= n:
        total, k = total + fun(k), k + 1
    return total
print(sum(10, cube)) # 1**3 + 2**3 +……+10**3

# function as return value
# Return a function that takes one argument k and returns k + n
def add(n):
    def add_n(k):
        return k + n
    return add_n
add_three = add(3)
print(add_three(10) == 13)

def apply_twice(f, x):
    return f(f(x))
print(apply_twice(square, 3)) #81

def compose(f, g):
    def h(x):
        return f(g(x))
    return h
print(compose(square, add(2))(10))
