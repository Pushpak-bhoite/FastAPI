
import asyncio
# basically event loop gets creates when we use asyncio.run

# async def creates a coroutine function
async def func1():
    await asyncio.sleep(2) ## we need to use await here, without await sleep coroutine is created bt never executed. 
    print("func 1")
    
async def func2():
    asyncio.sleep(2) 
    print("func 2")
    
async def func3():
    asyncio.sleep(2)
    print("func 3")
    
async def main():
    await func1()  ## since func1 is itself async, calling it return coroutine object. 
    await func2()
    await func3()
    
asyncio.run(main())

# so  both awaits are serving diff purposes 
# func1()


import asyncio

async def task1():
    print("A")
    await asyncio.sleep(0)
    print("B")

async def main():
    print("1")
    asyncio.create_task(task1())
    print("2")
    await asyncio.sleep(0)
    print("3")

asyncio.run(main())