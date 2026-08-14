
def find_LCM(a:int=4, b:int=6):
    i = a if a>b else b 
    while i:
       if i % a == 0 and i % b == 0 :
           print("i->", i)
           return i
       i += 1
       
def find_LCM_shortcut(a:int=4, b:int=6):
    i = a if a>b else b 
    
    
    
       
print("find->",find_LCM())
print("find->",find_LCM_shortcut())
        


# optimized way 

