# max consecutive ones from array 
def consecutive_ones(arr):
    right = 0 
    left = 0
    cnt = 0
    max = 1
    
    while right < len(arr) :
        if  arr[right] == 1 :
            cnt += 1
            right +=1
        else:
            cnt = 0
            if left <= right:
                left +=1
            else:
                right +=1 
        
        if cnt > max:
            max = cnt
    return max

print(consecutive_ones([1,1,1,1,0,0,0,1,1,1,1,0,0,1,1,0]))