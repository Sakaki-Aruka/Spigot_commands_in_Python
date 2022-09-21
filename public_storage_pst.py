import yaml,time,re,sys,json,codecs,os
from mcrcon import MCRcon

_playername = sys.argv[1]
#_playername = 'ytshiyugh'

_user_items = """[01:48:02] [Server thread/INFO]: ytshiyugh has the following entity data: [{Slot: 6b, id: "minecraft:grass_block", Count: 1b}, {Slot: 31b, id: "minecraft:golden_sword", Count: 1b, tag: {Damage: 0, AttributeModifiers: [{Amount: 20.0d, Slot: "offhand", AttributeName: "minecraft:generic.max_health", Operation: 0, UUID: [I; 203249347, 897421896, -816758991, -575485509], Name: ""}], display: {Lore: ['"GW限定配布アイテム"'], Name: '"Golden Weeeek"'}, Enchantments: [{lvl: 10s, id: "minecraft:mending"}]}}, {Slot: 33b, id: "minecraft:sand", Count: 64b}, {Slot: 34b, id: "minecraft:sand", Count: 64b}, {Slot: 103b, id: "minecraft:leather_helmet", Count: 1b, tag: {Damage: 0}}]"""

_user_items2 = """[10:55:21] [Server thread/INFO]: ytshiyugh has the following entity data: [{Slot: 4b, id: "minecraft:deepslate_redstone_ore", Count: 64b}, {Slot: 5b, id: "minecraft:warped_planks", Count: 64b}, {Slot: 6b, id: "minecraft:grass_block", Count: 1b}, {Slot: 31b, id: "minecraft:golden_sword", Count: 1b, tag: {Damage: 0, AttributeModifiers: [{Amount: 20.0d, Slot: "offhand", AttributeName: "minecraft:generic.max_health", Operation: 0, UUID: [I; 203249347, 897421896, -816758991, -575485509], Name: ""}], display: {Lore: ['"GW限定配布アイテム"'], Name: '"Golden Weeeek"'}, Enchantments: [{lvl: 10s, id: "minecraft:mending"}]}}, {Slot: 33b, id: "minecraft:sand", Count: 64b}, {Slot: 34b, id: "minecraft:sand", Count: 64b}, {Slot: 103b, id: "minecraft:leather_helmet", Count: 1b, tag: {Damage: 0}}]"""

_user_items3 = """[22:00:36] [Server thread/INFO]: ytshiyugh has the following entity data: [{Slot: 0b, id: "minecraft:redstone", Count: 5b}, {Slot: 1b, id: "minecraft:shulker_box", Count: 1b}, {Slot: 2b, id: "minecraft:shulker_box", Count: 1b, tag: {BlockEntityTag: {Items: [{Slot: 0b, id: "minecraft:iron_ingot", Count: 28b}, {Slot: 1b, id: "minecraft:moss_carpet", Count: 50b}, {Slot: 2b, id: "minecraft:flowering_azalea", Count: 19b}, {Slot: 3b, id: "minecraft:redstone", Count: 5b}, {Slot: 4b, id: "minecraft:iron_sword", Count: 1b, tag: {Damage: 0}}, {Slot: 5b, id: "minecraft:azalea", Count: 44b}], id: "minecraft:shulker_box"}}}, {Slot: 6b, id: "minecraft:cobbled_deepslate", Count: 1b}, {Slot: 7b, id: "minecraft:repeater", Count: 1b}, {Slot: 8b, id: "minecraft:chest", Count: 1b}, {Slot: 9b, id: "minecraft:andesite", Count: 3b}, {Slot: 10b, id: "minecraft:iron_shovel", Count: 1b, tag: {Damage: 38}}, {Slot: 11b, id: "minecraft:oak_log", Count: 44b}, {Slot: 12b, id: "minecraft:rooted_dirt", Count: 1b}, {Slot: 18b, id: "minecraft:wheat_seeds", Count: 30b}, {Slot: 20b, id: "minecraft:stick", Count: 13b}, {Slot: 21b, id: "minecraft:piston", Count: 1b}, {Slot: 28b, id: "minecraft:carrot", Count: 64b}, {Slot: 30b, id: "minecraft:moss_block", Count: 9b}, {Slot: 31b, id: "minecraft:shield", Count: 1b, tag: {Damage: 0}}, {Slot: 32b, id: "minecraft:wheat_seeds", Count: 1b}, {Slot: 34b, id: "minecraft:iron_helmet", Count: 1b, tag: {Damage: 0}}, {Slot: 100b, id: "minecraft:iron_boots", Count: 1b, tag: {Damage: 8}}, {Slot: 101b, id: "minecraft:iron_leggings", Count: 1b, tag: {Damage: 8}}, {Slot: 102b, id: "minecraft:iron_chestplate", Count: 1b, tag: {Damage: 8}}, {Slot: 103b, id: "minecraft:leather_helmet", Count: 1b, tag: {Damage: 8}}]"""

_user_items4 = """[22:16:54] [Server thread/INFO]: ytshiyugh has the following entity data: [{Slot: 2b, id: "minecraft:shulker_box", Count: 1b, tag: {BlockEntityTag: {Items: [{Slot: 0b, id: "minecraft:moss_block", Count: 64b}, {Slot: 1b, id: "minecraft:moss_block", Count: 64b}, {Slot: 2b, id: "minecraft:moss_block", Count: 64b}, {Slot: 3b, id: "minecraft:moss_block", Count: 64b}, {Slot: 4b, id: "minecraft:moss_block", Count: 64b}, {Slot: 5b, id: "minecraft:moss_block", Count: 64b}, {Slot: 6b, id: "minecraft:moss_block", Count: 64b}, {Slot: 7b, id: "minecraft:moss_block", Count: 64b}, {Slot: 8b, id: "minecraft:moss_block", Count: 64b}, {Slot: 9b, id: "minecraft:moss_block", Count: 64b}, {Slot: 10b, id: "minecraft:moss_block", Count: 64b}, {Slot: 11b, id: "minecraft:moss_block", Count: 64b}, {Slot: 12b, id: "minecraft:moss_block", Count: 64b}, {Slot: 13b, id: "minecraft:moss_block", Count: 64b}, {Slot: 14b, id: "minecraft:moss_block", Count: 64b}, {Slot: 15b, id: "minecraft:moss_block", Count: 64b}, {Slot: 16b, id: "minecraft:moss_block", Count: 64b}, {Slot: 17b, id: "minecraft:moss_block", Count: 64b}, {Slot: 18b, id: "minecraft:moss_block", Count: 64b}, {Slot: 19b, id: "minecraft:moss_block", Count: 32b}, {Slot: 20b, id: "minecraft:moss_block", Count: 64b}, {Slot: 21b, id: "minecraft:moss_block", Count: 64b}, {Slot: 22b, id: "minecraft:moss_block", Count: 64b}, {Slot: 23b, id: "minecraft:moss_block", Count: 64b}, {Slot: 24b, id: "minecraft:moss_block", Count: 64b}, {Slot: 25b, id: "minecraft:moss_block", Count: 64b}, {Slot: 26b, id: "minecraft:moss_block", Count: 64b}], id: "minecraft:shulker_box"}, display: {Lore: ['"(+NBT)"']}}}, {Slot: 100b, id: "minecraft:iron_boots", Count: 1b, tag: {Damage: 8}}, {Slot: 101b, id: "minecraft:iron_leggings", Count: 1b, tag: {Damage: 8}}, {Slot: 102b, id: "minecraft:iron_chestplate", Count: 1b, tag: {Damage: 8}}, {Slot: 103b, id: "minecraft:leather_helmet", Count: 1b, tag: {Damage: 8}}]"""

_user_items5 = """"""

with MCRcon('localhost','minecraft',25700) as mcr:
    _user_items_minecraft = mcr.command(f'data get entity {_playername} Inventory')
#_user_items_re = re.compile(r'\[(.{0,2}):(.{0,2}):(.{0,2})\] \[Server thread/INFO\]: (.{0,260}) has the following entity data: (.{0,10000000})')
_user_items_re = re.compile(r'(.{0,260}) has the following entity data: (.{0,10000000})')
_result_user_items = _user_items_re.finditer(_user_items_minecraft) #_user_items3)

item_re_judge = 0
_count = 0

_new_path = f"./public_storage_private_data/{_playername}"
if not os.path.exists(_new_path):
    os.mkdir(_new_path)

#if not os.path.exists(f"./public_storage_private_data/{_playername}/{_playername}.yml"):
with open(f'./public_storage_private_data/{_playername}/{_playername}.yml','w',encoding='utf-8') as mkdir_1yml:
    mkdir_1yml.write("")

#if not os.path.exists(f'./public_storage_private_data/{_playername}/{_playername}_item_quantity.yml'):
with open(f'./public_storage_private_data/{_playername}/{_playername}_item_quantity.yml','w',encoding='utf-8') as mkdir_2yml:
    mkdir_2yml.write("")

#if not os.path.exists(f'./public_storage_private_data/{_playername}/items-count-test.yml'):
with open(f'./public_storage_private_data/{_playername}/items-count-test.yml','w',encoding='utf-8') as mkdir_3yml:
    mkdir_3yml.write("")

#with open(f'./public_storage_public_items/public_items_blacklist.yml')

_enchantment_score = 0

for i in _result_user_items:
    #print(i.group(4))
    _user_item_json = (i.group(2))
    _user_item_json = _user_item_json[1:-1]
    #print(_user_item_json)

    for i in range(3):
        print()

    #print(f'user item json:\n{_user_item_json}')

    _end_re = re.compile(r'},')
    _result_end_re = _end_re.finditer(_user_item_json)

    _id_end = int(15)
    for i in _result_end_re:
        _span = str((i.span()))
        print(_span)
        _span_re = re.compile(r'(.{1,100}),(.{1,100})')
        _result_span_re = _span_re.finditer(_span)
        for i in _result_span_re:
            _id_start = int(i.group(1)[1:])
            id_raw = _user_item_json[_id_end:_id_start]
            print(id_raw)
            
            
            
            _id_end = int(i.group(2)[:-1])

            id_re = re.compile(r'Slot: (.{1,3})b, id: "minecraft:(.{1,50})", Count: (.{1,2})b')
            result_id_re = id_re.finditer(id_raw)
            for i in result_id_re:
                
                print(f'id:{i.group(2)}')
                print(f'個数:{i.group(3)}')

                _item_id = i.group(2)
                _item_count = i.group(3)
                if _item_id == "" or _item_count == "":
                    break
                #_item_place_slot = i.group(1)
                else:

                    with open(f'./public_storage_private_data/{_playername}/items-count-test.yml','a',encoding='utf-8') as items_write:
                        items_write.write(f'No{_count}: {i.group(2)}\n')
                        items_write.write(f'{_count}quantity: {i.group(3)}\n')
                    _count += 1
                    item_re_judge = 1

            if item_re_judge != 1:
                id_re_2 = re.compile(r'"minecraft:(.{1,50})", Count: (.{1,2})b')
                result_id_re_2 = id_re_2.finditer(id_raw)
                for i in result_id_re_2:
                    print(f'id:{i.group(1)}')
                    print(f'個数:{i.group(2)}')
                    with open(f'./public_storage_private_data/{_playername}/items-count-test.yml','a',encoding='utf-8') as items_write:
                        items_write.write(f'No{_count}: {i.group(1)}\n')
                        items_write.write(f'{_count}quantity: {i.group(2)}\n')
                    _count += 1
                    item_re_judge = 0
            
            print("______________")

#_latest_number = str(0)

print(f'id end:{_id_end}/')

_id_end_end = int(len(_user_items_minecraft))
_user_last_item = _user_items_minecraft[_id_end:_id_end_end]
print(f'user last item:{_user_last_item}/id end end:{_id_end_end}')


_user_last_re = re.compile(r'"minecraft:(.{1,50})", Count: (.{1,2})b')
_result_user_last = _user_last_re.finditer(_user_last_item)
for iiii in _result_user_last:
    _last_item_id = iiii.group(1)
    _last_item_quantity = iiii.group(2)

try:
    print(f'last item id / last item quantity = {_last_item_id}/{_last_item_quantity}')
except NameError:
    #"""
    with MCRcon('localhost','minecraft',25700) as mcr:
        mcr.command(f'tellraw {_playername} "Error:エンチャント済みアイテムを持たないでください。\\n準備プロセスを破棄します。(1)"')
    sys.exit()
    #"""

with open(f'./public_storage_private_data/{_playername}/items-count-test.yml','a',encoding='utf-8') as _last_write:
    _last_write.write(f'No{_count}: {_last_item_id}\n')
    _last_write.write(f'{_count}quantity: {_last_item_quantity}\n')

with open(f'./public_storage_private_data/{_playername}/items-count-test.yml','r',encoding='utf-8') as items_read:
    _read_items = items_read.read()
    number_re = re.compile(r'(.{1,4})quantity')
    _result_number_re = number_re.finditer(_read_items)
    for i in _result_number_re:
        #print(f'number:{i.group(1)}')
        _latest_number = i.group(1)
#print(f'latest number:{_latest_number}')


_items_list = {}
_items_quantity_list = []

_latest_number = int(_latest_number)
for i in range(_latest_number + 1):
    with open(f'./public_storage_private_data/{_playername}/items-count-test.yml','r',encoding='utf-8') as yml_read:
        _read_things = yaml.safe_load(yml_read)
        #_items_list.append(_read_things[f'No{i}'])
        _items_list[_read_things[f'No{i}']] = 0
        


print(f'len(_items_list):{len(_items_list)}')
#_items_list = dict(set(_items_list))

print(f'_items_list:{_items_list}')

with open(f'./public_storage_private_data/{_playername}/items-count-test.yml','r',encoding='utf-8') as yml_read2:
    _read_things2 = yaml.safe_load(yml_read2)
for ii in range(_latest_number +1):
    for iii in _items_list.keys():
        if str(_read_things2[f'No{ii}']) == str(iii):
            assignment_quantity = int(_items_list[iii]) + int(_read_things2[f'{ii}quantity']) 
            _items_list[iii] = assignment_quantity


print(f'_items_list:{_items_list}')
for i in range(5):
    print()
    #time.sleep(1)


_ignore_items_list = ["shovel",'picaxe','axe','sword','flint_and_steel','hoe','compass','fishing_rod','clock','shears','enchanted_book','helmet','chestplate','leggings','boots','shield','trident','crossbow','potion','banner','player_head','shulker_box','elytra','diamond']

_denied_item = 0
_private_file_counter = 0
_private_file_counter2 = 0

_partition = '_'*10

_total_mcr_ = []

with MCRcon('localhost',"minecraft",25700) as mcr:

    print("_"*10)
    for i4 in _items_list.keys():
        print(f'Item id/Item quantity → {i4}/{_items_list[i4]}')
        
        

        for i in range(len(_ignore_items_list)):

            _ignore_items_find = str(i4).find(_ignore_items_list[i])
            
            if str(_ignore_items_find) == "-1":
                #print('This item is ignored by Public-Storage System.')
                #_ignore_counter += 1
                
                pass
            else:
                print('Public Storage System is denied to deposit this item.')
                _denied_item += 1

                """
                with MCRcon('localhost','minecraft',25700) as mcr:
                        #mcr.command(f'''tellraw {_playername} "Item id/Item quantity → {i4}/{_items_list[i4]}"''')
                        time.sleep(0.1)
                        mcr.command(f'tellraw {_playername} "Public Storage is denied to deposit this item."')
                """

            
                
        if str(_denied_item) == '1':
            _denied_item = 0
            
        else:

            with open(f'./public_storage_private_data/{_playername}/{_playername}_item_quantity.yml','a',encoding='utf-8') as quantity_id:
                quantity_id.write(f'{i4}: {_items_list[i4]}\n')

            with open(f'./public_storage_private_data/{_playername}/{_playername}.yml','a',encoding='utf-8') as private_yml_write:
                private_yml_write.write(f'{_private_file_counter}: {i4}\n')
            _private_file_counter += 1

            #"""
            
            mcr.command(f'''tellraw {_playername} "{_partition}\\n{_private_file_counter2} → {i4}/{_items_list[i4]}"''')
            time.sleep(0.1)
            #"""

            #_total_mcr_.append(f'{_private_file_counter}: {i4}\n')


            _private_file_counter2 += 1
            

            #print(f'Item quantity:{_items_list[i4]}')
        print('_'*20)
        #time.sleep(1.3)

            
    for i in range(10):
        print()
                #print(f'id:{_user_item_json[_id_start:_id_end]}')
                
        #i.group(5)はアイテムのゆるいJSONを取得したものなのでそこから正規表現でアイテムとカウントだけ抜き出す。
        #シュルカーボックス内のアイテムについては要検証

"""
_link = {}
_link_number = 0
for i in _items_list.keys():
    _link[_link_number] = str(i)
    _link_number += 1

#print(_link)

with open(f"./public_storage_private_data/{_playername}/{_playername}.yml","a",encoding='utf-8') as private_data_write:
    for i in _link.keys():
        private_data_write.write(f'{i}: {_link[i]}\n')
"""
