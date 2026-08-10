# Iterator is an object that implements iterator protocol. 
# That means it has iter dunder method
# In simple - An iterator in Python is an object that lets you go through items one at a time. 


numbers = [10, 20, 30]

it = iter(numbers)  # now it is an iterator (internally it's __iter__)

print(next(it))  # 10
print(next(it))  # 20
print(next(it))  # 30


