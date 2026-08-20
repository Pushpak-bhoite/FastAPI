# https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/
def sum_two(nums, target):
    
    for i in range(len(nums)):
        for j in range(i+1 ,len(nums)): #start j from 1 step next to i
            if nums[i] + nums[j] == target: 
                return [i+1, j+1]
 
print("====== Optimize-1 =========")
# since it's sorted 

def two_sum2(nums, target):
    print("len(nums)-1->", len(nums) -1)
    left = 0
    right = len(nums) - 1
    while left < right:
        print(nums[left], nums[right])
        sum = nums[left] + nums[right]
        if sum == target:
            return [left+1, right+1]
        
        if sum > target:
            right -= 1
        else:
            left += 1    
    
    return "didn't found anything "

numbers = [ 2, 4, 6, 8]
print(sum_two(numbers, 9))
print(two_sum2(numbers, 9))
