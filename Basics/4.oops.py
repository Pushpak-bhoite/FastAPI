# pass
class Person:
    def __init__(self, name, age ):
        self.name = name
        self.age = age

    def printname(self):
        print("My name is ",self.name, " and age", self.age)

class Student(Person):
   pass

# Note: The __init__() function is called automatically every time the class is being used to create a new object.
s1 = Student("bran", 24)
s1.printname()

#2. ---------------------------------------
class Person2:
    def __init__(self, fname,lname):
        self.fname = fname
        self.lname = lname

    def printFulName(self):
        print("im person 2 ->", self.lname, " ", self.lname)

class Student2(Person2):
    def __init__(self, fname, lname, age):
        Person2.__init__(self, fname, lname )
        self.age = age
    def greetStudent(self):
     print("Hey im student ->", self.fname, self.lname, self.age)

x1 = Student2("john", "snow", 22)
x1.printFulName()
x1.greetStudent()
