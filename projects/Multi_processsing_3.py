import requests
from multiprocessing import Pool

def f(num):
    url = f"https://api.stackexchange.com/2.3/tags?order=desc&sort=popular&site=stackoverflow&page={num}"
    response = requests.request("GET", url, headers={}, data={})
    try:
        print( f"Page - {num} \t Row Count - { len(response.json()['items']) } \t Quota Max - {response.json()['quota_max']} \t Quota Remaining - {response.json()['quota_remaining']}" )
    except:
        print( f"Page - {num} \t Exceeded Burst Capacity" )
    num += 1

if __name__ == '__main__':
    with Pool(2) as p:
        # print(p.map(f, [1, 2, 3]))
        p.map(f, range(10) )
