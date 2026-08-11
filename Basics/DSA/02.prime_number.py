 
a = 5/2
b = 5%2
print(a)
print(b)

def prime_no(n):
    i = 2
    check = True
    while(i<= n/2 ):
        print(i)
        if(n%i == 0):
            print("found->", i)
            check = False 
            break
        i += 1
        return check

print(prime_no(5))