import sys,time
from mcrcon import MCRcon

playername = sys.argv[1]
print(f'playername:{playername}')
print('Diamond allow-priunted')

with open('./wtp-allow/allow-list.txt','r',encoding='utf-8') as allowlist_check:
    _check = allowlist_check.read()
    
    _playername = ','+playername
    _list_check = str(_check.find(_playername))
    if _list_check == "-1":
        
        with open('./wtp-allow/allow-list.txt','a',encoding='utf-8') as allow_add:
            allow_add.write(f',{playername}')

print(f'{playername} がallow-list.txtに追加されました。')

with MCRcon('localhost','minecraft',25700) as mcr:
    for i in range(3):
        mcr.command(f'tellraw {playername} " "')
        time.sleep(0.01)
    mcr.command(f'tellraw {playername} "オーバーワールドに入る許可を発行しました。"')
    time.sleep(0.01)
    mcr.command(f'tellraw {playername} "./wtp o (最初のピリオドは必須)をタイプしてオーバーワールドへジャンプしましょう!!"')
    for i in range(3):
        mcr.command(f'tellraw {playername} " "')
        time.sleep(0.01)