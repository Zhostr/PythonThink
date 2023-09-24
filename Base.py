""" Python 基础语法 """

from math import pi
tau = 2 * pi

a = 1
b = 2
# Execution rule for assignment statements:
#   1. Evalute all expressions to the right of = from left to right.
#   2. Bind all names to the left of = to the resulting values in the current frame.
b, a = a + b, b
print('a =', a)
print('b =', b)


#############################################
f = min
f = max
g, h = min, max
max = g
print(max(f(2, g(h(1, 5), 3), 3), 4))


# global frame 与 local frame（全局变量与局部变量）
# Every expression is evaluted in the context of an environment.
# The current environment is either the global frame alone, or a local frame followed by the global frame.
# Looking Up Names in Environments
#   Look for that name in the local frame.
#   If not found, look for it in the global frame.(Build-in names like 'max' are in the global frame.)
# 
# A call expression and the body of the function being called are evaluated in diff environments.
from operator import mul
def square(square):
    return mul(square, square)

print(square(10))


# / true division uses thr slash.
x = 2011 / 10
y = 2011 // 10
print(x, y)

def custom_div(x, y=10):
    ''' 如果没有给 y 传值，y will use the default value 10. '''
    return x + y, x - y

x , y = custom_div(100)
print('x:', x)
print('y:', y)


#############################################
# conditional statement
# False values in Python: False, 0, '', None, [], {}, ()
def absolute_value(x):
    ''' Use `python -i Base.py` to have a try. '''
    if x < 0:
        return -x
    elif x == 0:
        return 0
    else:
        return x

# while statement:
# Execution Rule for While Statements:
#   1. Evalutate the header's expression.
#   2. If it is a true value, execute the whole suite, then return to step 1.
i , total = 0, 0
while i < 3:
    i = i + 1
    total += i
print('i=', i)
print('total=', total)


    


