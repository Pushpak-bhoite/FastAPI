
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print("my name is", self.name, self.age)

p1 = Person('Emily', 23)
p1.greet()
