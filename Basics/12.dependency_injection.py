# we have this concept in JS, java, python 
# To keep code segregate and independent, and avoid staticness we use dependency injection. 
print(f"========== dependency injection using only functions=========  ")
def get_token():
    return "brandan stark"

def user_service(token):
    # token = get_token()  #if we do this way, then use_service() is directly dependant on get_token()
    print(token) 
    
    
print(user_service(get_token()))

print("============Both are dependency injections  =========================")
# A
class Database:
    def get_db(self):
        return "abcdef"
    
class UserService:
    def __init__(self, db):
        self.db = db
    
    def get_user(self):
        tempDB = self.db.get_db()
        print("tempDB->", tempDB)
        return tempDB
        
obj1 = UserService(Database())
print(obj1.get_user())

print("===============we passes db via function ============================")
# B
class Database:
    def get_db(self):
        return "abcdef"
    
class UserService:
    
    def get_user(self, db):
        tempDB = db.get_db()
        print("tempDB->", tempDB)
        return tempDB
db = Database()        
obj1 = UserService()

print(obj1.get_user(db))

print("========== When it's useful ==================")
# same UserService, different database implementations
# DI becomes powerful, especially for in testing, loose coupling, and swapping implementations.
class MySQLDatabase:
    def get_db(self):
        return "MySQL"


class MockDatabase:
    def get_db(self):
        return "Mock data"


class UserService:
    def __init__(self, db):
        self.db = db
        
service1 = UserService(MySQLDatabase())
service2 = UserService(MockDatabase())



#This gives you benefits like:

# reuse the same object
# easier testing
# easier replacement
# less coupling
# centralized configuration 