a = [1,2,3,4,5]

b = filter(lambda x: x%2 == 0 , a)  #returns new filter iterator object 
print('b', list(b)) # 

print('a->', a)

# well i can do the same thing using map

c = [1,2,3,4,5]

d = map(lambda x: x%2 == 0 , a)  # returns new map iterator object

print('MAP-d', list(d))

print('MAP-a', c)

print("====================== memory address =======================")

x= [1,2]
y= x 
print(id(x))
print(id(y))
 

a = [1, 2, 3]
b = [1, 2, 3]

print("-------- Each memory address is having different memory address -------- ")
j = [1, 2, 3, 4]

k = filter(lambda x: x % 2 == 0, a) # this newly created filter object will also be having different memory address. 
# 
print(id(j))
print(id(k))
k= list(k)
print(id(k))
