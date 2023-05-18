import time
import requests
import threading


class AsyncDataPull(threading.Thread):
    def __init__(self, page_start, page_stop):
        threading.Thread.__init__(self)
        self.page_start = page_start
        self.page_stop = page_stop

    def run(self):
        num = self.page_start
        while num <= self.page_stop:
            url = f"https://api.stackexchange.com/2.3/tags?order=desc&sort=popular&site=stackoverflow&page={num}"
            response = requests.request("GET", url, headers={}, data={})
            print( f"Page - {num} \t Row Count - { len(response.json()['items']) } \t Quota Max - {response.json()['quota_max']} \t Quota Remaining - {response.json()['quota_remaining']}" )
            num += 1


background = AsyncDataPull(1, 5)

background.start()
print('The main program continues to run in foreground.')

#foreground task
for i in range(3):
    print( f"Foreground Wait - {i}" )
    time.sleep(1)

print('Main program completed.')
