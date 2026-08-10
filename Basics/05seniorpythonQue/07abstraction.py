# Hiding complexity of system and exposing only necessary parts 
# Achieved using ABCs, abstract base classes and interfaces defined in abc module. 

from abc import ABC, abstractmethod


class Shape(ABC): #we always dont need to use ABC class, it's just a helper 
    @abstractmethod
    def area(self):
        pass 
    
    @abstractmethod
    def perimeter(self):
        pass
    
class Rectangle(Shape):
    def __init__(self, height, width):
        self.height = height
        self.height = width
        
    def area(self): #Since Rectangle inherits from Shape, it must implement all the abstract methods defined in Shape.
        return 2 * (self.height * self.width) #otherwise we will get error
    
    def perimeter(self):
        return super().perimeter()

obj1 = Rectangle(2, 4)
print('obj1->', obj1)