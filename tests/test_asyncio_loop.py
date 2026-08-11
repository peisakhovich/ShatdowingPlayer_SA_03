import asyncio
import threading
import time


async def test():
    print("TEST")
    await asyncio.sleep(2)
    print("TEST END")


loop = asyncio.new_event_loop()


def run_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()


thread = threading.Thread(target=run_loop)
thread.start()


print("MAIN: отправляем задачу")

future = asyncio.run_coroutine_threadsafe(
    test(),
    loop
)

print("MAIN: продолжаем работать")

time.sleep(5)

print("MAIN: останавливаем loop")

loop.call_soon_threadsafe(loop.stop)

thread.join()
loop.close()