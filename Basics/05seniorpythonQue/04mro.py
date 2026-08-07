# https://app.notion.com/p/Adv-Python-3b3716bf2b2c80c1aabbd16223c08ef7
# MRO - Method resolution order
# This determines sequences in which classes are searched for a method or attr 
#  It's important in cases of multiple inheritance where class is derived from multiple classes. 
class A: 
    def greet(self):
        print("Hello from A")

class B:
    def greet(self):
        print("Hello from b")
    
class C(A, B): # here it goes from left to right 
    def greet(self):
        print("Hello from b")

#*** Python uses c3 linearization algorithm to determine this order.  ****

c = C()

print(c.greet())

print("========== Diamond Problem ==========")

class X:
    def greet(self):
        print("Hello x")
    
class Y(X):
    pass
    print("Hello Y")
    
class Z(X):
    def greet(self):
        print("Hello Z")

class K(Y, Z):
    pass 

res = K()
res.greet()
# print('res->', res.greet()) # this trows error bt u can see seq via
print(K.__mro__)