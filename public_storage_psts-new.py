from mcrcon import MCRcon
import yaml,sys,re

_playername = sys.argv[1]
_requests_itemid = sys.argv[2]

#_playername ="ytshiyugh"
#_requests_itemid = "sto"

_check = 0

with MCRcon('localhost','minecraft',25700) as mcr:

    with open('./storage_items/storage_items.yml','r',encoding='utf-8') as _yml_read:
        _read_things = yaml.safe_load(_yml_read)

    _user_have = mcr.command(f'clear {_playername} {_requests_itemid} 0')
    _user_have_re = re.compile(r'Found (.{1,5}) matching items on player')
    _result_user_have = _user_have_re.finditer(_user_have)
    for i in _result_user_have:
        _users_quantity = i.group(1)
        _check += 1


    try:
        _requests_result = _read_things[_requests_itemid]
        if _check == 0:
            mcr.command(f'tellraw {_playername} "{"-"*10}\\nQuantity of the storage\\n{_requests_itemid}: {_requests_result}\\n{"-"*10}"')
        elif _check != 0:
            mcr.command(f'tellraw {_playername} "{"-"*10}\\nQuantity of yours\\n{_requests_itemid}: {_users_quantity}\\n{"-"*10}\\nQuantity of storage\\n{_requests_itemid}: {_requests_result}\\n{"-"*10}"')
    except:
        mcr.command(f'tellraw {_playername} "{"-"*10}\\nError:不正なアイテムIDです。\\n閲覧オーダーを破棄します。\\n{"-"*10}"')