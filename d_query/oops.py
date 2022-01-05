class Parent:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def res(self):
        return f"the name is {self.name} and age is {self.age}"


class Child(Parent):
    pass


obj1 = Child("abc", 20)
print(obj1)
print(obj1.res())


# Python code to demonstrate how parent constructors
# are called.

# parent class
class Person(object):

    # __init__ is known as the constructor
    def __init__(self, name, idnumber):
        self.name = name
        self.idnumber = idnumber

    def display(self):
        print(self.name)
        print(self.idnumber)


# child class
class Employee(Person):
    def __init__(self, name, idnumber, salary, post):
        self.salary = salary
        self.post = post

        # invoking the __init__ of the parent class
        Person.__init__(self, name, idnumber)

    def displayy(self):
        print(self.salary)
        print(self.post)
        return f"the name of employee is {self.name} salary is {self.idnumber} \t the salery is {self.salary} and post is {self.post}"


# creation of an object variable or an instance
a = Employee('Rahul', 886012, 200000, "Intern")

# calling a function of the class Person using its instance
a.display()
print(a.displayy())


class A:
    def __init__(self, n="Rahul", city="kharar"):
        self.name = n
        self.city = city


class B(A):
    def __init__(self, age):
        self.age = age

        A.__init__(self)


object = B(23)
print(object.name, object.city)
print(object.age)


class Base:
    def __init__(self, name):
        self.name = name


class Base1:
    def __init__(self, age):
        self.age = age


class Base2(Base, Base1):
    def __init__(self, name, age):
        self.name = name
        self.age = age

        Base.__init__(self, name)

        Base1.__init__(self, age)

    def show(self):
        return f"name is {self.name} and age is {self.age}"


obj4 = Base2("abc", 22)
print(obj4.show())


# Multilevel

class Parent:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        print("name=", self.name)


class Child(Parent):
    def __init__(self, name, age):
        Parent.__init__(self, name)
        self.age = age

    def get_age(self):
        print("age=", self.age)


class grandchild(Child):
    def __init__(self, name, age, address):
        Child.__init__(self, name, age)
        self.address = address

    def get_address(self):
        print("address=", self.address)


obj = grandchild("rahul", 22, "Noida")
obj.get_name(), obj.get_age(), obj.get_address()


class C:
    def __init__(self):
        self.c = 22
        self.__d = 35


class D(C):
    def __init__(self):
        C.__init__(self)
        self.e = 44


obj = D()


# print(obj.d) -----> Giving error because d is private variable


class Base:
    def __init__(self):
        self._a = 10  # protected variable


class Derived(Base):
    def __init__(self):
        Base.__init__(self)
        print("calling protected variable=", self._a)


obj = Derived()
obj2 = Base()


# print(obj2.a)


class Shape:
    def __init__(self, l, b):
        self._l = l
        self._b = b

    def get_value(self):
        print("length", self._l)
        print("breadth", self._b)


class Rect(Shape):
    def __init__(self, l, b):
        Shape.__init__(self, l, b)

    def get_area(self):
        print("area=", self._l * self._b)


class Rect1(Rect):
    def __init__(self, l, b):
        Rect.__init__(self, l, b)


obj = Rect1(40, 20)
obj.get_value()
obj.get_area()


class A:
    def m1(self):
        print("hi")

    def m2(self):
        print("hello")


class B:
    def m1(self):
        print("hii")

    def m2(self):
        print("helloo")


o1 = A()
o2 = B()
for o3 in (o1, o2):
    o3.m1()
    o3.m2()


class A:
    def m1(self):
        print("hi")

    def m2(self):
        print("hello")


class B:
    def m1(self):
        print("hii")

    def m2(self):
        print("helloo")


def fun(o3):
    o3.m1()
    o3.m2()
o1=A()
o2=B()

fun(o1)
fun(o2)


import abc

class parent:
    def func(self):
        pass
class Child(parent):
    def func(self):
        print("hii")

print(isinstance(Child(),parent))
print(issubclass(parent,Child))