import sys,re,subprocess
from mcrcon import MCRcon

_playername = sys.argv[1]
_requests_quantity = sys.argv[2]

deny_items_list = ["helmet",'chestplate','leggins','boots','bow',"sword",'tipped_arrow','crossbow','shield','trident',"enchanted_book","flint_and_steel",'shovel',"pickaxe",'axe','hoe','rod','shears','potion','writable_book','firework_rocket','banner',"carrot_on_a_stick","warped_fungus_on_a_stick","elytra",'shulker_box',"player_head",'map','water_bucket','lava_bucket','skull','obsidian','tnt','compass']

with MCRcon('localhost','minecraft',25700) as mcr:
    _user_have = mcr.command(f'data get entity {_playername} SelectedItem')

    _user_have_re = re.compile(r'has the following entity data: \{id: "minecraft:(.{1,500})",')
    _result_user_have = _user_have_re.finditer(_user_have)
    for i in _result_user_have:
        _user_have_item = i.group(1)

    for ii in deny_items_list:
        deny_found = _user_have_item.find(ii)
        if ii != -1:
            mcr.command(f'tellraw {_playername} "Error:\\nItem id error:You have invalid item."')
            sys.exit()

try:
    subprocess.Popen(['python','public_storage_pstd-new.py',_playername,_user_have_item,_requests_quantity])
except:
    sys.exit()