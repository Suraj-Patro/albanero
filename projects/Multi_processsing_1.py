import time
import requests
from multiprocessing import Process


def f(page_start, page_stop):
    num = page_start
    while num <= page_stop:
        url = f"https://api.stackexchange.com/2.3/tags?order=desc&sort=popular&site=stackoverflow&page={num}"
        response = requests.request("GET", url, headers={}, data={})
        print( f"Page - {num} \t Row Count - { len(response.json()['items']) } \t Quota Max - {response.json()['quota_max']} \t Quota Remaining - {response.json()['quota_remaining']}" )
        num += 1


if __name__ == '__main__':
    p = Process(target=f, args=(1, 5))
    p.start()

    print('The main program continues to run in foreground.')

    #foreground task
    for i in range(3):
        print( f"Foreground Wait - {i}" )
        time.sleep(1)

    p.join()
    print('Main program waited until background was done.')
