""" Python 基础语法 """

from math import pi
tau = 2 * pi

a = 1
b = 2
# Execution rule for assignment statements:
#   1. Evaluate all expressions to the right of = from left to right.
#   2. Bind all names to the left of = to the resulting values in the current frame.
b, a = a + b, b
print('a =', a) #2
print('b =', b) #3

# fibonacci num
def fibonacci(n: int) -> int:
    '''n >= 1'''
    pre, curr = 0, 1
    num = 1
    while(num < n):
        pre, curr = curr, pre + curr
        num += 1
    return curr

#############################################
f = min
f = max
g, h = min, max
max = g
print(max(f(2, g(h(1, 5), 3), 3), 4))


# global frame 与 local frame（全局变量与局部变量）
# Every expression is evaluated in the context of an environment.
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
print(x ** y) # x的y次方

def custom_div(x, y=10):
    ''' 如果没有给 y 传值，y will use the default value 10. '''
    return x + y, x - y

x , y = custom_div(100)
print('x:', x)
print('y:', y)


#############################################
# conditional statement
# False values in Python: False, 0, '', "", None, [], {}, ()
# not:
#   - returns the opposite boolean value of the following expression
#   - will always return either True or False
#
# and:
#   - evaluates expressions in order
#   - stops evaluating (short-circuits) at the first falsy value and returns it
#   - if all values evaluate to a truthy value, the last value is returned
#
# or:
#   - evaluates expressions in order
#   - short-circuits at the first truthy value and returns it
#   - if all values evaluate to a falsy value, the last value is returned
#
def absolute_value(x):
    ''' Use `python -i Base.py` to have a try. '''
    if x < 0:
        return -x
    elif x == 0:
        return 0
    else:
        return x

print(-1 and 0 and 1)           # -1 is true, 0 is false, so return 0
print(False or 999 or 1/0)      # 999 is true, return it
print("i" and "love" and "u")   # "i" "love" "u" is true, return the last  value "u"

# xxx will wear a jacket outside if it is below 60 degrees or it is raining.
# Write a function that takes in the current temperature and a boolean value telling if it is raining.
# The function should return True if xxx will wear a jacket and False otherwise.
def wears_jacket(temperature, is_raining):
    if temperature < 60 or is_raining:
        return True
    else: 
        return False


# while statement:
# Execution Rule for While Statements:
#   1. Evaluate the header's expression.
#   2. If it is a true value, execute the whole suite, then return to step 1.
i , total = 0, 0
while i < 3:
    i = i + 1
    total += i
print('i=', i)
print('total=', total)

# Write a function that returns the number of unique digits in a positive integer.
def unique_digit(n):
    '''Return the num of unique digits in a positive integer.'''
    unique_count = 1
    while n != 0:
        remainder = n % 10
        if not has_digit(n//10, remainder):
            unique_count += 1
    return unique_count

def unique_digit2(n):
    '''Return the num of unique digits in a positive integer.'''
    num = 0
    unique_count = 0
    while num <= 9:
        if has_digit(n, num):
            unique_count += 1
        num += 1
    return unique_count

def has_digit(n: int, k: int) -> bool:
    '''Return where k is a digit in n.'''
    if not isinstance(n, int) or not isinstance(k, int):
        raise ValueError('Both n and k must be integers.')
    if n < 0 or k < 0:
        raise ValueError('Both n and k must be non-negative.')
    if k > 9:
        raise ValueError('k must be a single digit.')

    while n > 0:
        remainder = n % 10
        if remainder == k:
            return True
        n = n // 10
    return False

    
# Prime Factorization 质因数分解
# computational process
def prime_factors(num):
    '''Print the prime factor of n in non-decreasing order.
    >>> prime_factors(858)
    2
    3
    11
    13
    '''
    assert num > 0, 'num must be positive'
    while(num > 1):
        smallest_prime = smallest_prime_factor(num)
        print(smallest_prime)
        num = num / smallest_prime

def smallest_prime_factor(n):
    i = 2
    while(n % i != 0):
        i += 1
    return i


