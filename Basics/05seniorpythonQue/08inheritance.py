# In inheritance allows a class or child to inherit attributes and methods from another class 
class Animal:
    def __init__(self, name):
        self.name = name
        
    def speak(self ): ##Following Error will be raised if we dont implement method 
        raise NotImplementedError("Subclass Must Implement this method")
    
class Dog(Animal):
    def speak(self):
        return f"{self.name} says woof"
    

class Cat(Animal):
    def speak(self):
        return f"{self.name} says woof"
    
    