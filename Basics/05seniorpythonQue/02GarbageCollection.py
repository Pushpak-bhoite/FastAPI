# Garbage collection struggles here in - circular object referencing 
#  this leads to memory leak
import gc


class Node:
    def __init__(self, name ):  #constructor initializer 
        self.name = name 
        self.next = None
        
# create node 
obj_a = Node("A")
obj_b = Node("B")

# Create Circular reference 
obj_a.next = obj_b 
obj_b.next = obj_a 

print("reference cnt ->", obj_a)
print("reference cnt ->", obj_b)

# delete var - del removes the variable from the stack (the reference), NOT the object from the heap. 
del obj_a
del obj_b

# Note: we cant print ref count here becoz we cant access a or b here 
collected = gc.collect()
print("collected refes ", collected )

#  and GC cant resolve these reference cycles easily and so we can force GC & still collect 2 objects




# ===============================
# __inti__ working 
# Python internally does:
# obj = Node.__new__(Node)   # Creates the object
# obj.__init__("A")          # Initializes the object