# Excellent question. The answer is: the modules we import are mostly abstraction, but they also use encapsulation internally.

class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):
    pass

dog = Dog()
dog.speak()