# lambda arguments: expression

def square(x):
    return x * x 
# Instead of above this 

square =  lambda x: x * 2
print(square(5))

multiply = lambda x, y : x * y # for 2 arguments 
print('multiply', multiply(4,5))  

# sort function only applicable to list type, sorted applicable to any type 
# 'key' parameter takes  function as argument(imean value we have to pas it is func - here we clear the param and argument concepts as well)
students = [("olise", 25),("alvarez", 24),( "messi", 39),] # this is type list of tuple

students.sort(key= lambda x: x[1])
print('students->', students)


str3 = ["Arsenal", "Aston Villa", "Barca" ]
str4 = ["Arsenal", "Aston Villa", "Barca" ]
str3.sort(key=lambda x: len(x)) # sort 
str4.sort(key=len) # different way
print("str3->",  str3);
print("str4->",  str4);

print("============= map ==============")
# map() works with any iterable (data types like dict, list)
str =  ["1", "2", "3"]
str2 = list(map(int, str)) # map returns new map object  iterator 
print(str)
print(str2)

print("============= Hello ")