
# Both gather() and TaskGroup are used for concurrency.
# here we dont have return_exception=True avoid crash. but if u have try/except then can avoid crash 
import asyncio

import aiohttp
# To avoid crash, use try except or return_exception=True

async def get_user1() :
    async with aiohttp.ClientSession() as session:
        async with session.get("https://jsonplaceholder.typicode.com/todos/1") as res:
            result = await res.json()
            return result
            
            
async def get_user2():
    # try:     
        async with aiohttp.ClientSession() as session:
            async with session.get("https://jsonplaceholder.typicode.com/todos/2") as res:
                result = await res.json()
                raise ValueError("Value has wrong format")
                return result
    # except Exception as err:
    #     print("err->", err)
        
                    
async def get_user3():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://jsonplaceholder.typicode.com/todos/3") as res:
            result = await res.json()
            # raise TypeError("unknown type")
            return result
        
async def main():    
    try:                
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(get_user1())
            task2 = tg.create_task(get_user2()) # if one task fails, remaining tasks are canceled 
            task3 = tg.create_task(get_user3())
        print("task1->", task1.result())
        print("task2->", task2.result())
        print("task3->", task3.result())
    except* Exception as eg:  # except* is used to handle exceptions from an ExceptionGroup
                            # it was introduced in v-3.11 specifically working with multiple exceptions at once
        print("Caught errors:->", eg.exceptions
              )
        
asyncio.run(main())

# there is also one more concepts like :
# future, lock, semphore (https://app.notion.com/p/Core-Python-1-3be716bf2b2c8048ac97cf91f81ccfab)