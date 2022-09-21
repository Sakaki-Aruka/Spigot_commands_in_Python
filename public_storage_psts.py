import time,re,sys,yaml
from mcrcon import MCRcon

_playername = sys.argv[1]
print(f'psts.py player:{_playername}')
#_playername = 'ytshiyugh'

with open('./public_storage_public_items/public_items.yml','r',encoding='utf-8') as _yml_read:
    _read_data = yaml.safe_load(_yml_read)

_counter = 0
_items_list = []

for i in _read_data['items']:
    print(f"{str(_counter)} → {i}:{_read_data['items'][i]}")
    _items_list.append(f"{str(_counter)} → {i}:{_read_data['items'][i]}")
    _counter += 1

#_items_string = '\n'.join(_items_list)

_mcr_counter = 0

with MCRcon('localhost','minecraft',25700) as mcr:
    for i in _read_data['items']:

        mcr.command(f'''tellraw {_playername} "{str(_mcr_counter)} → {i} : {_read_data['items'][i]}"''')
        _mcr_counter += 1
        time.sleep(0.1)


#print(_items_string)