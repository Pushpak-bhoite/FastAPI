# take u forword - L2 (lecture 2)
# Maximum points u can obtain from from cards
# condition - card has to choose consecutively from start or end. 
arr = [6,2,3,4,7,2,7,7,1]
k = 4 
cards = []
def max_points(nums, k): 
    left = k-1
    right = len(arr) - 1 
    total = 0
    max = sum(arr[:4]) # using built in function
    cards = nums[:4] # start with first 4 cards
    print("nums[:left]->", nums[:left])
    print("nums[right:len(nums)->", nums[right:len(nums)])
    while left >= 0 :
        print("left->", right)
        # left sum 
        lSum = 0
        rSum = 0
        for i in range(0, left):
            lSum = lSum + nums[i] 
            
        for i in range(right, len(nums)-1)   :
            rSum = rSum + nums[i]
        
        total = lSum + rSum
        print("total > max->", total > max)
        if total > max:
            max = total 
            cards=[]
            for i in range(0, left):
                cards.append(nums[i])
                        
            for i in range(len(nums)-1,right-1,-1): #iterate array in rev way. 
                cards.append(nums[i])
            # cards = nums[:left] + nums[len(nums)-1:right-1:-1] # short 
            print("cards->", cards)
            
        # shift window
        left -= 1
        right -= 1

    return {"left": left, "right" : right, "max":max, "cards": cards }
        
        
    
print(max_points(arr, k))
