# def tri_recursion(k):
#     if (k > 0):
#         result = k + tri_recursion(k - 1)
#         print(result)
#     else:
#         result = 0
#     return result


# print("\n\nRecursion Example Results")
# tri_recursion(6)

# list1 = ["apple", 'banana', 'apricot']
# res = map(lambda s: s[0] == 'a', list1)
# print(list(res))

# list1 = (1, 3, 2, 4, 4)
# list2 = (2, 3, 1, 4, 5)
# res = map(lambda x, y: x + y, list1, list2)
# print(list(res))

# list1 = ['abc', 'aa', 'bsc', 'es', 'as']
# res = filter(lambda s: s[1] == 'b', list1)
# print(list(res))

# from functools import reduce

# listt = [2, 3, 4, 5]
# res = reduce(lambda x, y: x + y, listt, 100)
# print(res)


# class Per:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age


# p1 = Per('abc', 22)
# print(p1.name)
# print(p1.age)


# class MyNumbers:
#     def __iter__(self):
#         self.a = 1
#         return self

#     def __next__(self):
#         x = self.a
#         self.a += 1
#         return x


# myclass = MyNumbers()
# myiter = iter(myclass)

# print(next(myiter))
# print(next(myiter))
# print(next(myiter))
# print(next(myiter))
# print(next(myiter))

# import platform

# x = dir(platform)
# print(x)

# import re

# '''
# Meta characters -
# * - 0 or more
# + - 1 or more
# ? - 0 or 1
# {m} - m times
# {m,n} - min m and max n
# '''

# test_phrase = 'sddsd..sssddd...sdddsddd...dsds...dsssss...sdddd'
# test_patterns = [r'sd*',  # s followed by zero or more d's
#                  r'sd+',  # s followed by one or more d's
#                  r'sd?',  # s followed by zero or one d's
#                  r'sd{3}',  # s followed by three d's
#                  r'sd{2,3}',  # s followed by two to three d's
#                  ]


# def multi_re_find(test_patterns, test_phrase):
#     for pattern in test_patterns:
#         compiledPattern = re.compile(pattern)
#         print('finding {} in test_phrase'.format(pattern))
#         print(re.findall(compiledPattern, test_phrase))


# multi_re_find(test_patterns, test_phrase)

# f = open("demo.txt", "a")
# f.write("new file data")
# f.close()
# f = open("demo.txt", "r")
# for x in f:
#     print(x)
# print(f.readline())

# import os
# os.remove("demo.txt")


from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('all_post')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            print("admin")
            return view_func(request,*args,**kwargs)
        return wrapper_func
    return decorator