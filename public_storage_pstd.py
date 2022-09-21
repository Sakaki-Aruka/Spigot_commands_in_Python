import yaml,time,re,sys,json,codecs,textfile
from mcrcon import MCRcon

#Error request:Your request quantity is too big.

"""
_playername = 'ytshiyugh'
_args_item_deposit = "2" #sys.argvの引数指定で送り込む(depositするアイテムのID)
_args_deposit_quantity = int(20) #sys.argvの引数指定で送り込む(depositするアイテムの数量)
"""

_sys_exit = 0
#"""以下引数一覧（本番環境に出すときに解放）
_playername = sys.argv[1]
_args_item_deposit = sys.argv[2]
_args_deposit_quantity = sys.argv[3]
#"""

#_args_deposit_quantity = int(10)


#_args_item_deposit = int(_args_item_deposit)

if _args_item_deposit == "":
    #MCRconでコードが記入済みの本を渡す
    sys.exit()

#_items_id_list = []
_len = len(_args_deposit_quantity)
if 0 < _len < 5:
    pass
else:
    with MCRcon('localhost',"minecraft",25700) as mcr:
        mcr.command(f'tellraw {_playername} "Error:deposit数が不正な値です。\\nアップロードプロセスを破棄します。01"')
    sys.exit()

ignore_things = [",",'.','+',"*",'/','-']
for i in ignore_things:
    _find = str(_args_deposit_quantity.find(i))
    if _find != "-1":
        with MCRcon('localhost',"minecraft",25700) as mcr:
            mcr.command(f'tellraw {_playername} "Error:deposit数が不正な値です。\\nアップロードプロセスを破棄します。02"')
        sys.exit()

_deposit_quantity_re = re.compile(r'([0-9]{0,4})')
_result_deposit_quantity_re = _deposit_quantity_re.finditer(_args_deposit_quantity)
for i in _result_deposit_quantity_re:
    _quantity = i.group(1)
    try:
        if 0 < int(_quantity) < 2000:
            pass
        else:
            with MCRcon('loclahost','minecraft',25700) as mcr:
                mcr.command(f'tellraw {_playername} "Error:deposit数が不正な値です。\\nアップロードプロセスを破棄します。03"')
            _sys_exit += 1
    except:
        with MCRcon('loclahost','minecraft',25700) as mcr:
            mcr.command(f'tellraw {_playername} "Error:deposit数が不正な値です。\\nアップロードプロセスを破棄します。03"')
        sys.exit()

if _sys_exit != 0:
    sys.exit()

_code_decryptment_re = re.compile(r'(.{1,3})')
_result_code_decrypt = _code_decryptment_re.finditer(_args_item_deposit)
for i in _result_code_decrypt:
    _args_item_deposit =int(i.group(1))

with open(f'./public_storage_private_data/{_playername}/{_playername}.yml','r',encoding='utf-8') as yml_read:
    _items_number_id = yaml.safe_load(yml_read)

"""
with open(f'./public_storage_private_data/{_playername}/{_playername}_item_quantity.yml','r',encoding='utf-8') as yml_read_quantity:
    _items_quantity = yaml.safe_load(yml_read_quantity)
"""


_deposit_item_id = _items_number_id[_args_item_deposit]
_deposit_item_quantity = _args_deposit_quantity #_items_quantity[_deposit_item_id]
print(f'deposit item id:{_deposit_item_id}')
print(f'deposit item quantity:{_deposit_item_quantity}')

print(f'clear {_playername} {_deposit_item_id} {_deposit_item_quantity}')

#_sys_exit = 0

#"""
try:
    #"""
    with MCRcon('localhost','minecraft',25700) as mcr:
        _return_code = str(mcr.command(f'clear {_playername} {_deposit_item_id} {_deposit_item_quantity}'))
        #mcr.command(f'clear {_playername} {_deposit_item_id} {_deposit_item_quantity}')
        print(_return_code)
        try:
            
            _return_code_re = re.compile(r'Removed (.{1,10}) items from player (.{1,300})')
            _result_return_code = _return_code_re.finditer(_return_code)
            for i in _result_return_code:
                """
                if str(i.group(1)) != str(_deposit_item_quantity):
                    mcr.command(f'tellraw {_playername} "Error:共有ストレージにアップするアイテム数と手持ちのアイテム数が一致しません。\\nアップロードプロセスを破棄します。(1)"')
                    #sys.exit()
                    _sys_exit += 1
                """
                    

                if str(i.group(2)) != str(_playername):
                    mcr.command(f'tellraw {_playername} "Error:プレイヤー名が一致しません。\\nアップロードプロセスを破棄します。(2)"')
                    #sys.exit()
                    _sys_exit += 1
        except:
            with MCRcon('localhost','minecraft',25700) as mcr:
                mcr.command(f'tellraw {_playername} "Error:エラーが発生しました。\\nアップロードプロセスを破棄します。(3)"')
                #sys.exit()
                _sys_exit += 1
        try:
            #No items were found on player ytshiyugh
            _return_code_re_2 = re.compile(r'No items were found on player (.{1,300})')
            _result_return_code_2 = _return_code_re_2.finditer(_return_code)
            for ii in _result_return_code_2:
                _warning_player = ii.group(1)
            mcr.command(f'tellraw {_warning_player} "Error:Items not found error.\\nアップロードプロセスを破棄します。(4)"')
            #sys.exit()
            _sys_exit += 1
        except:
            pass

        try:
            #Removed 10 items from player ytshiyugh
            _return_code_re_3 = re.compile(r'Removed (.{1,10}) items from player (.{1,300})')
            _result_returncode_3 = _return_code_re_3.finditer(_return_code)
            for iii in _result_returncode_3:
                _deleted_items_quantity = str(iii.group(1))
                if _deleted_items_quantity != str(_deposit_item_quantity): #消したアイテム数とdeposit申請したアイテム数が一致しない場合
                    
                    mcr.command(f'tellraw {_playername} "Error:Items quantity not matched.\\n対象のアイテムがシュルカーボックスの中に入っていたりしていませんか?\\nアップロードプロセスを破棄します。(5)"')
                    time.sleep(0.1)
                    mcr.command(f'give {_playername} {_deposit_item_id} {_deleted_items_quantity}')
                    print(f'give {_playername} {_deposit_item_id} {_deleted_items_quantity}')
                    #sys.exit()
                    _sys_exit += 1

        except:
            pass

        
    #"""
    """
    with MCRcon('localhost',"minecraft",25700) as mcr:
        mcr.command(f'clear {_playername} {_deposit_item_id} {_deposit_item_quantity}')
    """
except:
    pass

if _sys_exit != 0:
    sys.exit()
    
#"""
        
with open('./public_storage_public_items/public_items.yml','r',encoding='utf-8') as yml_read_items:
    _data_public_storage = yaml.safe_load(yml_read_items)

try:
    
    _plus_item_id = int(_data_public_storage['items'][_deposit_item_id])
    _sumed_item_quantity = int(_deposit_item_quantity) + int(_plus_item_id)

    _replace_deposit_before = str(f'{_deposit_item_id}: {_plus_item_id}')
    _replace_deposit_afther = str(f'{_deposit_item_id}: {_sumed_item_quantity}')
    textfile.replace(f'./public_storage_public_items/public_items.yml',_replace_deposit_before,_replace_deposit_afther)
    print(f'Total {_deposit_item_id} quantity : {_sumed_item_quantity}')
    with MCRcon('localhost','minecraft',25700) as mcr:
        mcr.command(f'tellraw {_playername} "アップロードプロセスが完了しました。\\nDeposit process has finished."')

except KeyError:
    with open('./public_storage_public_items/public_items.yml','a',encoding='utf-8') as storage_item_add:
        storage_item_add.write(f'\n  {_deposit_item_id}: {_args_deposit_quantity}')
    print('A new element was added.')