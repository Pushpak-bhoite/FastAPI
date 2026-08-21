# https://leetcode.com/problems/valid-palindrome/
class Solution:
    def isPalindrome(self, s: str) -> bool:
        left = 0 
        right = len(s)-1
        
        while left < right:
            if s[left] == s[right]:
                left += 1
                right -= 1
            else:
                return False
          
        return True

str = "madam"
obj = Solution()
print(obj.isPalindrome(str))


print("5".lower())



