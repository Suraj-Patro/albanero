import time
import asyncio
import requests


async def execute(delay, num):
    print( f"Page - {num} \t T1 - Queuing Wait" )
    await asyncio.sleep(delay)

    url = f"https://api.stackexchange.com/2.3/tags?order=desc&sort=popular&site=stackoverflow&page={num}"
    response = requests.request("GET", url, headers={}, data={})

    try:
        print( f"Page - {num} \t T2 - Row Count - { len(response.json()['items']) } \t Quota Max - {response.json()['quota_max']} \t Quota Remaining - {response.json()['quota_remaining']}" )
    except:
        print( f"Page - {num} \t T2 - Exceeded Burst Capacity" )
    
    await asyncio.sleep(delay)

    print( f"Page - {num} \t T3 - Data Parse Wait" )
    await asyncio.sleep(delay)

    num += 1


async def main():
    # Using asyncio.create_task() method to run coroutines concurrently as asyncio
    tasks = []
    
    for i in range(5):
        tasks.append( asyncio.create_task( execute( 5 - i, i )) )


    print(f"started at {time.strftime('%X')}")
  
    for i in range(len(tasks)):
        await tasks[i]

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())  
