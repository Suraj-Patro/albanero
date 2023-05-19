import time
import requests
from threading import Thread


def data_pull(delay, num):
    print( f"Page - {num} \t T1 - Queuing Wait" )
    time.sleep(delay)

    url = f"https://api.stackexchange.com/2.3/tags?order=desc&sort=popular&site=stackoverflow&page={num}"
    response = requests.request("GET", url, headers={}, data={})

    try:
        print( f"Page - {num} \t T2 - Row Count - { len(response.json()['items']) } \t Quota Max - {response.json()['quota_max']} \t Quota Remaining - {response.json()['quota_remaining']}" )
    except:
        print( f"Page - {num} \t T2 - Exceeded Burst Capacity" )

    time.sleep(delay)

    print( f"Page - {num} \t T3 - Data Parse Wait" )
    time.sleep(delay)



tasks = []

for i in range(5):
    tasks.append( Thread(target=data_pull, args=(0, i + 1)) )

start = time.time()

for i in range(len(tasks)):
    tasks[i].start()


for i in range(len(tasks)):
    tasks[i].join()

end = time.time()
print(f"Time taken in seconds - {end - start}")
