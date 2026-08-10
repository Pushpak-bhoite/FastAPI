# Polymorphism means the same interface or method can behave differently depending on the object using it.

class Shape:
    def area(self): 
        raise NotImplementedError("subclass must implement this method")

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width 
        self.height = height
        
    def area(self):
        return self.width * self.height
        
class Circle(Shape):
    def __init__(self, radius ) :
        self.radius = radius
    
    def area(self):  
        return 3.14 * self.radius * self.radius

rectangle = Rectangle(5, 10 )

circle = Circle(5)