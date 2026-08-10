class BankAccount:
    bank_name = "HDFC Bank"   # class variable

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    # 1. Instance method
    def deposit(self, amount): # 
        self.balance += amount
        return self.balance

    # 2. Class method
    @classmethod
    def change_bank_name(clg, new_name): # used to make changes in class attributes 
        # print('clg->>>>', clg.balance)#******** this isn't possible becoz class methods can't access or modify instance attr/var
        clg.bank_name = new_name

    # 3. STATIC METHOD = It's just a utility function provided by class for instances,
    # it doesn't take any argument like cls or self. 
    @staticmethod
    def is_valid_amount(amount): # dont take any argument
        return amount > 0 
    
obj1 = BankAccount("pushpak", 200)
# Both works 
obj1.deposit(70)
BankAccount.deposit(obj1, 80) # becoz internally this happens - the instance get's passed to method as the self instance

# It works even it's class method
# obj1.change_bank_name("Axis")

print(" ===== static method - method can be called by class or object (same with class methods) === ")
print(obj1.is_valid_amount(4))  
print(BankAccount.is_valid_amount(4))

print(" ====== call class method ====== ")
print(obj1.change_bank_name("FFFFFFFFFFF"))  
print(BankAccount.change_bank_name(obj1, "kkkkkkkkkkkkkkk"))

print('obj1->', obj1.bank_name)
print(BankAccount.bank_name) 

print("========= Before and after updation of class attr ===========")
print("before updation->",obj1.bank_name)
BankAccount.bank_name = "Nestle"
print("after updation->",obj1.bank_name)

print("Hello->", BankAccount.deposit(obj1, 80))

# The only main diff i found is we can't access instance var in class method

# | Feature                        | Instance Method          | Class Method                       | Static Method                      |
# | ------------------------------ | ------------------------ | ---------------------------------- | ---------------------------------- |
# | Decorator                      | No decorator             | `@classmethod`                     | `@staticmethod`                    |
# | First parameter                | `self`                   | `cls`                              | No special parameter               |
# | Works with                     | Instance/object          | Class                              | Neither specifically               |
# | Can access instance variables? | ✅ Yes                    | ❌ No                               | ❌ No                               |
# | Can access class variables?    | ✅ Yes                    | ✅ Yes                              | ❌ Directly                         |
# | Can modify instance state?     | ✅ Yes                    | ❌ No                               | ❌ No                               |
# | Can modify class state?        | ✅ Yes                    | ✅ Yes                              | ❌ No                               |
# | Called using                   | `obj.method()`           | `Class.method()` or `obj.method()` | `Class.method()` or `obj.method()` |
# | Used for                       | Object-specific behavior | Class-level behavior               | Utility/helper functions           |
