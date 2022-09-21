import yaml,time,re,sys,json,codecs,textfile
from mcrcon import MCRcon

_playername = sys.argv[1]
_args_pull_itemid = sys.argv[2]
_args_pull_quantity = sys.argv[3]

try:
    _quantity_len = int(len(_args_pull_quantity))
    if 0 < _quantity_len < 5:
        pass
    else:
        with MCRcon('locahost','minecraft',25700) as mcr:
            mcr.command(f'tellraw {_playername} "Error:個数が不正な値です。\\nダウンロードプロセスを破棄します。(01"')
        sys.exit()
except:
    with MCRcon('localhost',"minecraft",25700) as mcr:
        mcr.command(f'tellraw {_playername} "Error:ダウンロードプロセスを破棄します。"')
    sys.exit()

ignore_things = [",",'.','+',"*",'/','-']
for i in ignore_things:
    _find = str(_args_pull_quantity.find(i))
    if _find != "-1":
        with MCRcon('locahost','minecraft',25700) as mcr:
            mcr.command(f'tellraw {_playername} "Error:個数が不正な値です。\\nダウンロードプロセスを破棄します。(02"')
        sys.exit()

_invalid_args_re = re.compile(r'([0-9]{0,4})')
_result_invalid_re = _invalid_args_re.finditer(_args_pull_quantity)
for i in _result_invalid_re:
    _quantity = i.group(1)
    try:
        if 0 < int(_quantity) < 2000:
            break
        else:
            with MCRcon('localhost','minecraft',25700) as mcr:
                mcr.command(f'tellraw {_playername} "Error:個数が不正な値です。\\nダウンロードプロセスを破棄します。(03"')
            break
    except:
        with MCRcon('localhost','minecratf',25700) as mcr:
            mcr.command(f'tellraw {_playername} "Error:個数が不正な値です。\\nダウンロードプロセスを破棄します。(04"')
        sys.exit()
        


_sys_exit = 0
try:
    if int(_args_pull_quantity) >= 2000:

        with MCRcon('localhost','minecraft',25700) as mcr:
            mcr.command(f'tellraw {_playername} "Error:Your pull request is too big.\\n要求アイテム数を2000個以下にしてください\\nダウンロードプロセスを破棄します。(1)"')
        _sys_exit += 1
    
    #_args_quantity_re = re.compile(r'([1-9]{1,4})')

except:
    sys.exit()

if _sys_exit != 0:
    sys.exit()

"""
_playername = 'ytshiyugh'
_args_pull_itemid = 31
_args_pull_quantity = int(5)
"""

for i in range(5):
    print()



with open('./public_storage_public_items/public_items.yml','r',encoding='utf-8') as yml_item_read:
    _pulled_data = yaml.safe_load(yml_item_read)

_pulled_items_id = {}
#print(_pulled_data['items'])
_counter = 0
for i in _pulled_data['items']:
    _pulled_items_id[str(f'i{_counter}')] = str(i)
    _counter += 1

#print(_pulled_items_id)

#print(f'_pulled items id: {_pulled_items_id}')
print(f'pulled items idの要素数は{str(len(_pulled_items_id))}')

_pull_id = _pulled_items_id[f'i{_args_pull_itemid}']
_public_storage_quantity = int(_pulled_data['items'][_pull_id])
print(f"storage's {_pull_id} quantity : {_public_storage_quantity}")

_args_pull_quantity = int(_args_pull_quantity)
print(f'_args_pull_quantity:{_args_pull_quantity}')
if _public_storage_quantity > _args_pull_quantity:
    if _public_storage_quantity - _args_pull_quantity > 0:
        #print('pull request')
        _remaining_quantity = _public_storage_quantity - _args_pull_quantity
        textfile.replace('./public_storage_public_items/public_items.yml',f'{_pull_id}: {_public_storage_quantity}',f'{_pull_id}: {_remaining_quantity}')
        print(f'pull request → \nbefore storage quantity [{_pull_id}: {_public_storage_quantity}]\nafter storage quantity [{_pull_id}: {_remaining_quantity}]')
        with MCRcon('localhost','minecraft',25700) as mcr:
            mcr.command(f'give {_playername} {_pull_id} {_args_pull_quantity}')
    else:
        with MCRcon('localhost',"minecraft",25700) as mcr:

            mcr.command(f'tellraw {_playername} "Error:Your request quantity is over the quantity on the storage.\\nダウンロードプロセスを破棄します。(3)"')
else:
    with MCRcon('localhost',"minecraft",25700) as mcr:

        mcr.command(f'tellraw {_playername} "Error:Your request quantity is over the quantity on the storage.\\nダウンロードプロセスを破棄します。(2)"')
    sys.exit()