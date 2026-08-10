import asyncio
import time

from audio.async_runner import AsyncRunner


async def test_task():

    print("Async task: START")

    await asyncio.sleep(2)

    print("Async task: FINISH")

    return 42


def main():

    runner = AsyncRunner()

    future = runner.submit(test_task())

    print("Main: task submitted")

    while not future.done():

        print("Main: working...")
        time.sleep(0.2)

    result = future.result()

    print(f"Main: result = {result}")

    runner.stop()


if __name__ == "__main__":
    main()