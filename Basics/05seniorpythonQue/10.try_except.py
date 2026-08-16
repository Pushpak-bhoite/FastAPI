

import asyncio
import aiohttp #Python built on the asyncio library, is an asynchronous HTTP client and server framework 
async def func1():
    await asyncio.sleep(2) 
    print("func 1")

# create custom error
class UserNotExist(Exception):
    pass 

async def func2():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://jsonplaceholder.typicode.com/todos/1") as res:
                
                # print('res->', res.text())
                data = await res.json()
                print("API response->:", data)
                raise UserNotExist("User not exist") # == custom error
                # ==== built-in Exception types ======
                # raise ValueError("Invalid Value")
                # raise TypeError("Expected a string")
                # raise RuntimeError("Something went wrong")
                # raise PermissionError("Access denied")
                # raise RuntimeError("Something went wrong")
    except Exception as error:
        print("error->", error)
        
    print("func 2")
    
async def func3():
    await asyncio.sleep(2)
    print("func 3")
    
async def main():
    await func1() 
    await func2()
    await func3()
    
asyncio.run(main())