# BaseException is the ultimate ancestor of every built-in exception, Even Exception's class parent is BaseException

# create custom error
import asyncio

import aiohttp

# custom exceptions
class UserNotExist(Exception):
    pass 

# ---------------------------------------------
def foo():
    try:
        a = 2/0
        print(a)
    except ZeroDivisionError as error: # ZeroDivisionError is subclass of Exception, so we can use Exception 
        print(error)
        
async def get_user():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://jsonplaceholder.typicode.com/todos/1") as res:
                data = await res.json() # or u can use test() as well 
                print(data)
                raise UserNotExist("Requested user doesn't exist")
            
    except Exception as err:
            print(err)
        
foo()

asyncio.run(get_user())
