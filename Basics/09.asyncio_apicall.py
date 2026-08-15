
import asyncio
import aiohttp #Python built on the asyncio library, is an asynchronous HTTP client and server framework 
async def func1():
    await asyncio.sleep(2) 
    print("func 1")
    
async def func2():
    async with aiohttp.ClientSession as session:
        async with session.get("https://jsonplaceholder.typicode.com/todos/1") as res:
            data = await res.json()
            print("API response:", data)
    print("func 2")
    
async def func3():
    asyncio.sleep(2)
    print("func 3")
    
async def main():
    await func1() 
    await func2()
    await func3()
    
asyncio.run(main())