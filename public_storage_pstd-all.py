import yaml,time,re,sys,textfile
from mcrcon import MCRcon

print('pstd hello')
#"""
try:
    _playername = sys.argv[1]
    #_args_requests_itemid = sys.argv[2]
except:
    sys.exit()

deny_items_list = ["helmet",'chestplate','leggins','boots','bow',"sword",'tipped_arrow','crossbow','shield','trident',"enchanted_book","flint_and_steel",'shovel',"pickaxe",'axe','hoe','rod','shears','potion','writable_book','firework_rocket','banner',"carrot_on_a_stick","warped_fungus_on_a_stick","elytra",'shulker_box',"player_head",'map','water_bucket','lava_bucket','skull','obsidian','tnt','compass']

_all_item_id_list = []
_all_item_quantity_list = []

def all_deposit(_playername):

    _deny_check = 0
    _deposit_items_dict = {}

    with MCRcon('localhost','minecraft',25700) as mcr:
        for i in range(40):
            _return_code = mcr.command(f'data get entity {_playername} Inventory[{i}]')
            print(f'{i}:{_return_code}')
            if _return_code == f"Found no elements matching Inventory[{str(i)}]":
                print('no items here')
                break

            _all_item_id_re = re.compile(r'(.{0,300}) has the following entity data: {Slot: (.{0,10})b, id: "minecraft:(.{1,300})", Count: (.{0,10})b}')
            _result_all_itemid = _all_item_id_re.finditer(_return_code)
            for i in _result_all_itemid:
                _all_item_id = i.group(3)
                _all_item_quantity = i.group(4)

                for i2 in deny_items_list:
                    _denied_items_check = _all_item_id.find(i2)
                    if _denied_items_check != -1:
                        _deny_check += 1
                    else:
                        pass
                
                if _deny_check == 0:
                    #print(f'all item id :{_all_item_id}\nall item quantity :{_all_item_quantity}')
                    _all_item_id_list.append(_all_item_id)
                    _all_item_quantity_list.append(_all_item_quantity)
                else:
                    _deny_check = 0

        _counter = 0
        for i in _all_item_id_list:
            try:
                _dict_quantity = _deposit_items_dict[i]
                _deposit_items_dict[i] = int(_dict_quantity) + int(_all_item_quantity_list[_counter])
                
            except: 
                _deposit_items_dict[i] = _all_item_quantity_list[_counter]
            _counter += 1

        
 
    
        with open('./storage_items/storage_items.yml','r',encoding='utf-8') as _yml_read:
            _read_things = yaml.safe_load(_yml_read)

        _deposit_did = 0
        
        for i in _deposit_items_dict:
            _clear_return = mcr.command(f'clear {_playername} {i} {_deposit_items_dict[i]}')
            _invalid_quantity = _clear_return.find('No items were found')
            if _invalid_quantity != -1:
                sys.exit()
            #print(f'clear {_playername} {i} {_deposit_items_dict[i]}')
            _clear_return_re = re.compile(r'Removed (.{0,10}) items from player (.{0,300})')
            _result_clear_return = _clear_return_re.finditer(_clear_return)
            for ii in _result_clear_return:
                _return_clear_quantity = ii.group(1)
                
            try:
                if str(_deposit_items_dict[i]) != str(_return_clear_quantity):
                    pass
                else:
                    try:
                        _before_quantity = int(_read_things[i])
                        _after_quantity = _before_quantity + int(_deposit_items_dict[i])
                        textfile.replace('./storage_items/storage_items.yml',f'{i}: {_before_quantity}',f'{i}: {_after_quantity}')
                        _deposit_did += 1
                    except:
                        with open('./storage_items/storage_items.yml','a',encoding='utf-8') as _yml_write:
                            _yml_write.write(f'{i}: {_deposit_items_dict[i]}\n')
                            _deposit_did += 1
            except:
                pass
        
        _total_quantity = 0
        if _deposit_did != 0:
            for ii in _deposit_items_dict:
                _total_quantity += int(_deposit_items_dict[ii])
            mcr.command(f'tellraw {_playername} "アップロードプロセスが完了しました。\\n{_total_quantity}個のアイテムをアップロードしました。"')


all_deposit(_playername)#_args_requests_itemid)