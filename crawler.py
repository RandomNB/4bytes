import requests
from bs4 import BeautifulSoup

url = 'https://www.4byte.directory/signatures/?page={}'

sigs = set()


def load(fn):
    with open(fn) as f:
        c = f.readlines()
    for i in c:
        hash, name = i.strip().split(': ')
        sigs.add((hash, name))


def save(fn, lsig):
    end = False
    with open(fn, 'a') as f:
        for s in lsig:
            if s not in sigs:
                sigs.add(s)
                f.write(f"{s[0]}: {s[1]}\n")
            else:
                end = True
    return end


def save_all(fn):
    with open(fn, 'w') as f:
        for s in sigs:
            f.write(f"{s[0]}: {s[1]}\n")


failed = []


def download(k):
    try:
        r = requests.get(url.format(k)).content
        r = BeautifulSoup(r)
        hashes = [x.text for x in r.find_all('td', class_='bytes_signature')]
        names = [x.text for x in r.find_all('td', class_='text_signature')]
        print(f"Download page {k} success with {len(names)} items")
        return list(zip(hashes, names))
    except:
        print(f"!!!! Download page {k} ERROR")
        failed.append(k)
        return []


load('4bytes.txt')
i = 1
while(True):
    ss = download(i)
    end = save('4bytes.txt', ss)
    if end:
        break
    i += 1
