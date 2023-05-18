import requests
from multiprocessing import Process, Value, Array


def f(n):
    num = n.value
    while num <= 5:
        url = f"https://api.stackexchange.com/2.3/tags?order=desc&sort=popular&site=stackoverflow&page={num}"
        response = requests.request("GET", url, headers={}, data={})
        try:
            print( f"Page - {num} \t Row Count - { len(response.json()['items']) } \t Quota Max - {response.json()['quota_max']} \t Quota Remaining - {response.json()['quota_remaining']}" )
        except:
            print( f"Page - {num} \t Exceeded Burst Capacity" )
        num += 1
    
    n.value = num


if __name__ == '__main__':
    num = Value('i', 0)
    p = Process(target=f, args=(num,))
    p.start()
    p.join()

    print( f"Share Value - {num.value}" )
