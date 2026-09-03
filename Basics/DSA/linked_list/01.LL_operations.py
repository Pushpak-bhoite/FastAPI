class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None # *** this is important, we are declaring head and reusing is throughout same
        
    def insert_at_end(self, val):
        new_node = Node(val)
        
        if self.head is None:
            self.head = new_node
            return 
        else :
            current = self.head
            while current.next is not None:
                current = current.next
            
            current.next = new_node 
    
    def update_list(self, old_val, new_val):
        current = self.head
        
        while current.val != old_val:
            current = current.next
        current.val = new_val
        return       
            
    def read_list(self):
        current = self.head
        while current is not None:
            print(current.val, end=" ")
            current = current.next
    
    def delete_node(self, val): #always use temp var like current, if u move self.head directly then it'll loose list first point
        
        if self.head == None:
            return
        
        current = self.head
        while current.next is not None:
            if current.next.val == val:
                current.next = current.next.next
                return
            current = current.next
        return
    
    def delete_node_at_specific_idx(self, idx):
        cnt = 1 
        current = self.head
        while cnt != idx:
            current = current.next
            cnt += 1
        print(f"\nitem deleted at idx-{idx}==>", current.val)
        current.next = current.next.next
        return
        
if __name__ == "__main__":
    ll = LinkedList()
    # create 
    ll.insert_at_end(10)
    ll.insert_at_end(20)
    ll.insert_at_end(30)
    ll.insert_at_end(40)

    # ll.update_list(20, 200)
    # ll.read_list()
    # ll.delete_node(200) #where val is is present
    # print("\nItem deleted\n")
    # ll.read_list()
    ll.delete_node_at_specific_idx(2) 
    ll.read_list()
    print()
    