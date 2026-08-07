# Attribute → a variable that belongs to an object or a class, so that's why var inside class called attr

# Encapsulation
class BankAccount:
    _hello = 10 #  class attribute - shared by all instances
    def __init__(self, name, amt):
        self.name = name # public instance attribute 
        self.__balance = amt #Private attribute 
        # This is Python's name Mangling in action.
        self._boo_protected = 9 #Convention: internal use(for devs), but accessible
        
    def deposit(self, amt):
        if amt > 0:
            self.__balance += amt
            return self.__amt
    
    
    def withdraw(self, amt):
        if self.__balance > 0 and amt <= self.__balance:
            self.__balance -= amt
            return self.__balance
    
    def getBalance(self):
        return self.__balance
    
acc = BankAccount("allan", 400)
acc2 = BankAccount("allan", 400)

# print(acc.__balance) # we cant access directly __balance #❌ AttributeError - private
print(acc.getBalance()) # to access it. we need to create getfunction
print('_hello->', acc._hello)
acc._hello = 20
acc2._hello = 30
print('acc->', acc._hello)
print('acc->', acc2._hello)

# U can change class attr by accessing, in above cases every obj got their own seperate instance 
BankAccount._hello = 33
print("BankAccount._hello->" , BankAccount._hello)
