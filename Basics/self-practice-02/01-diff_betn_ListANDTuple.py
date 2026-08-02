
# Refer this page while reading it -https://app.notion.com/p/Core-Python-3ab716bf2b2c80e99553c5309d7ed6fc
import sys
import time

print("============= speed diff Tuple v/s List ===============") # string takes too much time than these 2 
a = list(range(1000)) # this line literally Stores references to all those 1000 integers.
b = tuple(range(1000))
start = time.time_ns() # returns time in nano sec (time.time returns in float sec) 

for i in range(len(a)):
    x = a[i]   #####-> This is where main iteration is going on, which delays the operation 
end = time.time_ns() 
print("time-1 ->", end - start)
    
start = time.time_ns()
for i in range(1000):
    x = b[i]
end = time.time_ns()

print("time- 2->", end - start )

print("============= Memory Efficient test ===============")
x = [] # creating empty list 
y = () 
# Assign value
x = ["Arsenal", "Barcelona", "Aston villa"]
y = ("Arsenal", "Barcelona", "Aston villa")

print('List-x ', sys.getsizeof(x), 'bytes')
print('Tuple-y ', sys.getsizeof(y), 'bytes')

print("============= Methods(all are applicable to List/Tuple/String ) =============")
print("--------- slicing --------------")
a = [1, 2, 3, 4, 5, 6, 7, 8]
b = (6, 7, 8, 9, 10)
print('a->',a[1: 4])  
print('b->',b[: 4])  
print('a->',a[::2])  # second : (colon) introduces step 


a = list(range(5)) #Step 1:  range(5) creates a range object, not five integers immediately in heap
# The list() constructor iterates over the range.
# Then it creates a list object.
# Each slot contains a reference to an integer object which created in heap.
# In-short - 'a' is just a reference in stack to everything created in the heap
print("--------- Repetition --------------")
print('a->', a * 2)  # This way u can repeat List, Tuple, String. 
print("---------- concatination --------------")
print(b + (4,5))
# 
for str in "Hello":
    print(str)
    

print("==========Set ===========")
# set accepts only one iterable 
s = set((1,1,2,3,)) # set with tuple
print(s)
s = set([1,1,2,3]) # set with List
print(s)
s = {"Hi",3,3,3}
print(s);
