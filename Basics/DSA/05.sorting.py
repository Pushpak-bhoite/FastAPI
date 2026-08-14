a = [5,4,3,2,1]

for i in range(len(a)):
    print(a)
    for j in range(i + 1, len(a)):
        if a[i] > a[j]:
            temp = a[j]
            a[j] = a[i]
            a[i] = temp
        
        
print(a)
        

    
    