# ** The range object is an iterable that generates numbers on demand. It does not store all the numbers in memory.
# it's actually an immutable sequence type.
r = range(5)
print('range->', r)
print('range->',type(r))

for i in range(4):
    print(i)
    
