class Example:
    class_var = "shared"
    
    def __init__(self, name):        # Define 'name' here first!
        self.name = name
    
    def instance_method(self):
        return self.name             # Now this works
    
    @classmethod
    def class_method(cls):
        return cls.class_var
    
    @staticmethod
    def static_method(x, y):
        return x + y

# Usage
obj = Example("Alice")   # 'name' is set via __init__
print(obj.instance_method())  # "Alice"