import asyncio
import time

async def test1():
    num=1
    while True:
        print(f"Test 1: {num}")
        num += 1
        await asyncio.sleep(2)

async def test2():
    
    while True:
    
        await asyncio.sleep(3)
        print(f"Test 2: time: {time.time()}")


async def main():

    task1 = asyncio.create_task(test1())
    task2 = asyncio.create_task(test2())

    await asyncio.gather(test1(), test2())
    
    await task1
    await task2

if __name__ == "__main__":
    asyncio.run(main())
