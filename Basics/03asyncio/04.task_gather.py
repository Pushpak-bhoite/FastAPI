
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
            return result

async def main():
    # execution(if we have use return_exceptions=True or try/except in that func). Otherwise it crashes
    # So simply gather isn't good at err handling & it does cancels other coroutines if one of them were to fail
    # gather does not handle errs, if any one of api fails then it does not abort whole 
    result = await asyncio.gather(get_user1(), get_user2(), get_user3(), return_exceptions=True) 
    
    for i, res in enumerate(result):
        print(f"res[{i}] => ", res)

    
asyncio.run(main())