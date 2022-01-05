# lambda  function
#from django.template.defaultfilters import upper
from itertools import count

listt = [2, 3, 5, 4]
res = map(lambda x: x * x, listt)
print(list(res))


# using function
def add(num):
    return num + num


listt = [3, 2, 1, 3, 4]
res = map(add, listt)
print(list(res))


def calculateSquare(n):
    return n * n


numbers = (1, 2, 3, 4)
result = map(calculateSquare, numbers)
print(set(result))

# using in built function
listt = [2.34, 4.33, 4.99, 3.21]
res = map(round, listt)
print(list(res))


def mystr(s):
    return s.upper()

strr="hello world"
res=map(mystr,strr)
print(res)
for i in res:
    print(i,end="")

def fun(s):
    return s.upper()

tup=('php','python','html','css')
res=map(fun,tup)
print(tuple(res))

#tup=('php','python','html','css')
#res=map(upper,tup)
#print(tuple(res))

tup=('php','python','html','css','bs4')
res=map(lambda x:x.upper(),tup)
print(tuple(res))

my_list=['a','b','c','d']
my_tuple=['php','python','html','java']
res=map(lambda x,y:x+"_"+y,my_list,my_tuple)
print(list(res))

tup=('php','python','html','css','bs4')
res=list(map(lambda x:x.lower(),tup))
print(res)


listt=('php','python','html','css','bs4')
res=list(map(len,listt))
print(res)
print(len(res))




listt=('php','python','html','css','bs4')
res=list(map(str.capitalize,listt))
print(res)


with_dots = ["processing..", "...strings", "with....", "..map.."]
print(list(map(lambda s: s.strip("."), with_dots)))

listOfLambdas = [lambda i=i: i*i for i in range(1, 6)]
for f in listOfLambdas:
    print(f())

from functools import reduce
# Returns the sum of all the elements using `reduce`
result = reduce((lambda a, b: a + b), [1, 2, 3, 4])
result1 = reduce((lambda a, b: a if a>b else b), [1, 2, 3, 4])
print("result =",result)
print("result 1=",result1)


def fun(n,m):
    return n*m
listt=[2,1,3,2]
res=reduce(fun,listt,2)
print(res)


check = lambda x : x > 10 and x < 20
# Check if given numbers are in range using lambda function
print(check(12))
print(check(3))
print(check(24))

abc=lambda x:x*2 if x<10 else (x*3 if x<20 else x)
print(abc(22))
print(abc(2))

# Filter list of numbers by keeping numbers from 10 to 20 in the list only
listofNum = [1, 3, 33, 12, 34, 56, 11, 19, 21, 34, 15]
listofNum = list(filter(lambda x : x > 10 and x < 20, listofNum))
print('Filtered List : ', listofNum)

print(list(filter(lambda x:x>2,[1,2,3,4])))
listt=('php','python','html','css','bs4')
print(list(filter(lambda x:len(x)==3,listt)))

strr='this is a list of string'
listt=''.join(filter(lambda x:x not in ['i','s'],strr))
print(listt)

d = {'a': 1, 'b': 2}
values = map(lambda key: d[key] , d.keys())
print(list(values))

dictOfNames = {
   7 : 'sam',
   8: 'john',
   9: 'mathew',
   10: 'riti',
   11 : 'aadi',
   12 : 'sachin'
}
newdict=dict(filter(lambda x:x[0]%2==0,dictOfNames.items()))
newdict1=dict(filter(lambda x:len(x[1])==4,dictOfNames.items()))
print(newdict)
print(newdict1)

def f(x):
	return x + 1

d = {'A': 0, 'B': 1, 'C': 2}

dict = dict(map(lambda x: (x[0], f(x[1])), d.items()))
print(dict)

listt=('php','python','html','css','bs4')
res=map(list,listt)
print(list(res))


def min_fun(a,b):
    return a if a<b else b

def max_fun(a,b):
    return a if a>b else b

listt=[1,2,34,11]
r1=reduce(min_fun,listt)
r2=reduce(max_fun,listt)
print(r1)
print(r2)

def both_true(a,b):
    return bool(a and b)

print(reduce(both_true, [1,1,1,0]))


