# L5 takeUforward
# *** set is unordered (so be careful while storing data in it ) ***
def fruits_into_two_baskets(arr):
    seen = set()
    left = 0
    right = 1
    bucket =[]
    maxBucket =[]
    while right < len(arr):
        print(left, right, bucket, seen)
        if arr[right] in seen or len(seen) < 2:
            bucket.append(arr[right])
            seen.add(arr[right])
            right += 1
            if len(bucket) > len(maxBucket):
                maxBucket = bucket 
        else :
            # shift left until u don't reach to next diff element
            bucket = bucket[1:]
            if arr[left] in seen:
                    seen.remove(arr[left]) #we can also use pop bt it removes arbitary value
                    print(seen)
                    bucket = [i for i in bucket if i != arr[left]]
            left += 1
        # print(bucket)
        #i can put it here becoz in else window wil be shrinking
        # if len(bucket) > len(maxBucket):
        #                 maxBucket = bucket 
               
            
    print("maxBucket->", maxBucket)
    return maxBucket

Hello =[3,3,3,1,2,1,1,2,2,1,3,3,4,4,4,4,3,3]
print(fruits_into_two_baskets(Hello))

# def fruits_into_two_baskets_practice(arr):
#     left = 0
#     right = 1
#     seen = set()
#     bucket = []
#     maxBucket = []
#     while right < len(arr):
#         if arr[right] in seen or len(seen) < 2:
#             seen.add(arr[right])
#             bucket.append(arr[right])
#             right += 1
#         else:
#             if arr[right] != arr[left + 1]
#             left +=1
        


# print(fruits_into_two_baskets_practice(Hello))

# print(Hello)