import requests
import time

def data_pull(start, stop):
    num = start

    while num <= stop:
        url = f"https://api.stackexchange.com/2.3/tags?order=desc&sort=popular&site=stackoverflow&page={num}"
        response = requests.request("GET", url, headers={}, data={})
        # yield response.json()
        yield f"Page - {num} \t Row Count - { len(response.json()['items']) } \t Quota Max - {response.json()['quota_max']} \t Quota Remaining - {response.json()['quota_remaining']}"
        num += 1

for data in data_pull(1, 5):
    print( data )
    time.sleep( 5 )
