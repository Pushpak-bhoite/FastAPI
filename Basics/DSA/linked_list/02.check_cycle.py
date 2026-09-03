# Definition for singly-linked list.
from typing import Optional

from httpx import head

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

ll1 = ListNode(10)
ll2 = ListNode(20)
ll3 = ListNode(30)
ll4 = ListNode(40)

ll1.next = ll2
ll2.next = ll3
ll3.next = ll4
# ll4.next = ll1
# [10,20,30]
# def print_ll(head:ListNode):
    
#     while head != None:
#         print("n->", head.val) 
#         head = head.next
    
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        # print(head.val)
        slow = head
        fast = head
        while fast != None  and fast.next != None   : 
            slow = slow.next
            fast = fast.next.next  
            print(fast.val if fast else None) ## we need if else here otherwise it breaks
            if slow == fast: 
                return True
        return False            
    
sol = Solution()
# print_ll(ll1) #it goes in infinite loop 
print(sol.hasCycle(ll1))