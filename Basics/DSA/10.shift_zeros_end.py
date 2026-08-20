
a = [0,3,5,0,8,0,3,1,0,4]

def shift_zeros_to_end(nums):
    left = 0
    right = len(a) -1 

    while left < right :
        if a[left] == 0 :
            if a[right] == 0 :
                right -= 1
            else:
                temp = a[left]
                a[left] = a[right]
                a[right] = temp
        else: 
            left += 1 
        
shift_zeros_to_end(a)        
print(a)
                
                
                
              
    