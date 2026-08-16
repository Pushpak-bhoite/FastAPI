import asyncio
import aiohttp #it's Python(package) built on the asyncio library(package), is an asynchronous HTTP client and server framework 
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
                
                data = await res.json()
                print("API response->:", data)
                return data
    except Exception as error:
        print("error->", error)
        
async def func3():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://jsonplaceholder.typicode.com/todos/1") as res:
                
                # print('res->', res.text())
                data = await res.json()
                print("API response->:", data)
                # raise UserNotExist("User not exist") # == custom error
    except Exception as error:
        print("error->", error)
        
async def main():
    await func1() 
    
    t1 = asyncio.create_task(func2()) #don't use await if ur using gather 
    t2 = asyncio.create_task(func3())
    res =  await asyncio.gather(t1,t2)
    print("concurrent res--->", res)
    # === mostly we do following, dont need to create create_task() ====
    t3 = await asyncio.create_task(func2()) # here await is necessary 
    print('t3--->',t3)
    
    
asyncio.run(main())

# asyncio.gather() can schedule coroutines and wait for them concurrently, while
# asyncio.create_task() explicitly schedules a coroutine as a Task. If I just need to run multiple
# but both perform concurrent operation 
