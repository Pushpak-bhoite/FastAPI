a = 5/2
b = 5%2
print(a)
print(b)

def is_prime_no(n):
    if n < 2 : return False
    i = 2
    while i<= n/2 :
        if n%i == 0:
            return False 
        i += 1
    return True
    
def all_prime_numbers(num):
    if num ==  2: return [2] #gaurd
    
    prime_nums = []
    temp = 2
    while temp <= num:
        i = 2
        flag = True
        while i <= temp/2:
            if temp%i == 0:
                flag=False
                break 
            i+= 1
        
        if flag:
            prime_nums.append(temp)
    
        #   
        temp += 1
    return prime_nums

def all_prime_numbers_with_for(num):
    if num ==  2: return [2] #gaurd
    
    prime_nums = []
    for temp in range(2, num):
        flag = True
        for i in range(2, int(temp/2)):
            if temp%i == 0:
                flag=False
                break 
        
        if flag:
            prime_nums.append(temp)
    
    return prime_nums
        
        
def all_prime_numbers_without_flag(num):
    if num ==  2: return [2] #gaurd
    
    prime_nums = []
    for temp in range(2, num):
        flag = True
        if is_prime_no(temp): # just use function instead of Flag (bt it'll take more time and memory)
           prime_nums.append(temp)  
    
    return prime_nums
        
    
print("prime_no-->>", is_prime_no(5))

# Print all prime numbers from 1 to N 
print("all_prime_numbers-->>",all_prime_numbers(166))
print("all_prime_numbers_with_for->", all_prime_numbers_with_for(166))
print("all_prime_numbers_without_flag-->", all_prime_numbers_without_flag(166))
print(int(7/2))