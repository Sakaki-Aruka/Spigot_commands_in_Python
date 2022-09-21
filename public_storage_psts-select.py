import subprocess,re,time,sys
from mcrcon import MCRcon


_playername = sys.argv[1]

with MCRcon('localhost','minecraft',25700) as mcr:
    _selected_itemid = mcr.command(f'data get entity {_playername} SelectedItem')
    

    re_check = 0
    _selected_re = re.compile(r'(.{1,300}) has the following entity data: \{id: "minecraft:(.{1,500})",')
    _result_selected_re = _selected_re.finditer(_selected_itemid)
    for i in _result_selected_re:
        _selected_ = i.group(2)
        re_check += 1

        
    
    #mcr.command(f'tellraw {_playername} "{"-"*10}\\nQuantity of yours.\\n{_selected_}: {_user_have_quantity}"')

    
    if re_check != 0:
        subprocess.Popen(['python','public_storage_psts-new.py',_playername,_selected_])
    else:
        sys.exit()