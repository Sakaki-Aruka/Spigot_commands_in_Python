import sys,re,subprocess
from mcrcon import MCRcon

_playername = sys.argv[1]

deny_items_list = ["helmet",'chestplate','leggins','boots','bow',"sword",'tipped_arrow','crossbow','shield','trident',"enchanted_book","flint_and_steel",'shovel',"pickaxe",'axe','hoe','rod','shears','potion','writable_book','firework_rocket','banner',"carrot_on_a_stick","warped_fungus_on_a_stick","elytra",'shulker_box',"player_head",'map','water_bucket','lava_bucket','skull','obsidian','tnt','compass']

with MCRcon('localhost','minecraft',25700) as mcr:
    _user_select_raw = mcr.command(f'data get entity {_playername} SelectedItem')

    _user_select_re = re.compile(r'has the following entity data: \{id: "minecraft:(.{1,500})",')
    _result_user_select = _user_select_re.finditer(_user_select_raw)
    for i in _result_user_select:
        _user_select = i.group(1)
        #print(f'user select :{_user_select}')

    for ii in deny_items_list:
        _deny_found = _user_select.find(ii)
        if _deny_found != -1:
            mcr.command(f'tellraw {_playername} "Error:\\nPstd error:You have invalid items."')
            sys.exit()

    try:
        _user_select_quantity_raw = mcr.command(f'clear {_playername} {_user_select} 0')
    except:
        sys.exit()

    _user_quantity_re = re.compile(r'Found (.{1,5}) matching items on player')
    _result_quantity = _user_quantity_re.finditer(_user_select_quantity_raw)
    for ii in _result_quantity:
        _user_have_quantity = ii.group(1)

    print(f'playername: {_playername}/id: {_user_select}/quantity: {_user_have_quantity}')

    try:
        subprocess.Popen(['python','public_storage_pstd-new.py',_playername,_user_select,_user_have_quantity])
    except:
        print('select-all-out')
        sys.exit()