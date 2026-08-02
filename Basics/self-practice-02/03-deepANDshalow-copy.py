from copy import copy, deepcopy

#1. With '=' this here a & b var are just pointing to same List object. It's not creating new full var
# it's just creating new reference to same obj
# Result: if i change anything in b then changes will be reflected in a 
a = [1,2,[9,6],3,4,5]
b = a 
a[2].append(9)
a[4] = 12

print("a", a)
print("b", b)

print("======= shallow copy ===========")
#2. Duplicate the object, but only copies reference for nested objects. thus changes in nested objects affect both copies
i = [1,2,[9,6],3,4,5]
j = copy(i)
j[2].extend(['D','D','D',]) 
j[2]= 8
j[3]= 9
print('i', i)
print('j', j)

print("======= Deep copy ===========")
# 3. Creates fully independent copy, including all nested objects
x = [1,2,[9,6],3,4,5]
y = deepcopy(x)

y[2].append(6)
print('x', x)
print('y', y)