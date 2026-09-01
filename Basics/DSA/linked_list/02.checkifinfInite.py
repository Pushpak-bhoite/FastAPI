# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


ll1 = ListNode(10)
ll2 = ListNode(20)
ll3 = ListNode(30)

ll1.next = ll2
ll2.next = ll3
ll3.next = ll1

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = head
        fast = head
        while head == None:
            if slow == fast:
                return True
        
        return False            
    
sol = Solution() 

print(sol.hasCycle(ll1))