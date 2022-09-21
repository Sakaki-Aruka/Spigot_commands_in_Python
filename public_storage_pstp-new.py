import yaml,time,sys,re,textfile
from mcrcon import MCRcon

#"""
_playername = sys.argv[1]
_requests_itemid = sys.argv[2]
_requests_itemquantity = sys.argv[3]
#"""

#_playername = "ytshiyugh"
#_requests_itemid = "stone"
#_requests_itemquantity = 0

try:
    _requests_itemquantity = int(_requests_itemquantity)
except:
    sys.exit()

def _pull(_playername,_requests_itemid,_requests_itemquantity):
    with MCRcon('localhost','minecraft',25700) as mcr:

        with open('./storage_items/storage_items.yml','r',encoding='utf-8') as _yml_read:
            _read_things = yaml.safe_load(_yml_read)
        try:
            _items_quantity_on_storage = _read_things[_requests_itemid]
            #print('sac')
        except:
            
            mcr.command(f'tellraw {_playername} "Error:不正な値の検知\\nダウンロードプロセスを破棄します.0"')
            sys.exit()
        
        if int(_items_quantity_on_storage) > int(_requests_itemquantity) and int(_requests_itemquantity) <= 2000:
            pass
        else:
            mcr.command(f'tellraw {_playername} "Error:要求量が大きすぎます\\nダウンロードプロセスを破棄します.1"')
            sys.exit()
        
        _clear_returncode = mcr.command(f'give {_playername} {_requests_itemid} {_requests_itemquantity}')
        _noplayer_was_found = _clear_returncode.find('No player was found')
        if _noplayer_was_found != -1:
            print('no player')
            sys.exit()
        _clear_returncode_re = re.compile(r'Gave (.{1,5}) \[(.{1,300})\] to (.{1,300})')
        _result_clear_returncode = _clear_returncode_re.finditer(_clear_returncode)
        for i in _result_clear_returncode:
            _clear_quantity = i.group(1)
        try:
            if _clear_quantity != str(_requests_itemquantity):
                mcr.command(f'tellraw {_playername} "{"-"*10}\\nError:不正な値を検出\\nダウンロードプロセスを破棄します.01\\n{"-"*10}"')
                sys.exit()
        except:
            mcr.command(f'tellraw {_playername} "{"-"*10}\\nError:不正な値を検出\\nダウンロードプロセスを破棄します.02\\n{"-"*10}"')
            print(f'clear quantity:{_clear_quantity},requests itemquantity:{_requests_itemquantity}')
            sys.exit()
        
        _after_quantity_onstorage = int(_items_quantity_on_storage) - int(_requests_itemquantity)
        textfile.replace('./storage_items/storage_items.yml',f'{_requests_itemid}: {_items_quantity_on_storage}',f'{_requests_itemid}: {_after_quantity_onstorage}')
        mcr.command(f'tellraw {_playername} "ダウンロードプロセス完了\\n{_requests_itemquantity}アイテムを引き出しました"')

        

_len_requests_quantity = len(str(_requests_itemquantity))
if 0 < _len_requests_quantity <5:
    _pull(_playername,_requests_itemid,_requests_itemquantity)

else:
    with MCRcon('localhost','minecraft',25700) as mcr:
        mcr.command(f'tellraw {_playername} "{"-"*10}\\nError:不正な値を検出\\nダウンロードプロセスを破棄します\\n{"-"*10}"')
    sys.exit()