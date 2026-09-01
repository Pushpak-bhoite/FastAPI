class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

node1 = Node(10)
node2 = Node(20)
node3 = Node(30)

node1.next = node2
node2.next = node3

current = node1

class LinkedList:
    def __init__(self):

def readLL(head):

    while head:
        head = head.next
        print(head.data)

readLL(node1)      
# print(node1.data)