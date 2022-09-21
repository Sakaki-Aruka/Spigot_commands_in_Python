import sys,time,subprocess,re
from mcrcon import MCRcon


playername = sys.argv[1] #プレイヤーネーム
_dimension = sys.argv[2] #テレポートしたいディメンジョンの頭文字
print(f'rcon-wtp.py {playername} {_dimension}')
if playername == 'ytshiyugh':
    with MCRcon('localhost','minecraft',25700) as mcr:
        if _dimension == "o":
            mcr.command(f'mv tp {playername} world')
        elif _dimension == "l":
            mcr.command(f'mv tp {playername} test')
        elif _dimension == "e":
            mcr.command(f'mv tp {playername} everyone')
        elif _dimension == "v":
            mcr.command(f'mv tp {playername} vs_setup')
            time.sleep(0.1)
            mcr.command(f'gamemode adventure ytshiyugh')
            #print(f'mv tp {playername} everyone')
        elif _dimension == "w":
            mcr.command(f'mv tp {playername} weekly_end')


        elif _dimension == "g":
            _item = mcr.command(f'data get entity {playername} Inventory')
            print(f'_item:{_item}')
            try:
                _item_replaced = _item.replace(' ','_')
                _judge_template = f"{playername}_has_the_following_entity_data:_[]"
                print(f"judge template:{_judge_template}")
                print(f"item replaced: {_item_replaced}")
                if _item_replaced == _judge_template:
                    mcr.command(f'clear {playername}')
                    time.sleep(0.1)
                    mcr.command(f'mv tp {playername} gweek')
                    print('You teleported the gweek.')
                else:
                    mcr.command(f'tellraw {playername} "GW限定ワールドに行くためにはインベントリを空にする必要があります!!"')
            except:
                pass

            
            #mcr.command(f'mv tp {playername} gweek')
            #time.sleep(0.1)
            


        else:
            mcr.command(f'tellraw ytshiyugh "Error"')
else:
    with open('./wtp-allow/allow-list.txt','r',encoding='utf-8')as _list_read:
        _allowed_player = _list_read.read()
    _find = str(_allowed_player.find(playername))
    if _find != '-1': #見つかった時(許可されたプレイヤーだったとき)
            
        with MCRcon('localhost','minecraft',25700) as mcr:

            if _dimension == "l": #テレポートしたい先がロビーだったら
                mcr.command(f'mv tp {playername} test')
                print(f'command:mv tp {playername} test')
                mcr.command(f'gamemode adventure {playername}')
            
            elif _dimension == "o": #テレポートしたい先がoverworldだったら
                mcr.command(f'mv tp {playername} world')
                time.sleep(0.1)
                mcr.command(f'gamemode survival {playername}')
                try:
                    subprocess.Popen(['python','rcon-homecommand.py',playername,'tel']) 
                        
                except:
                    mcr.command(f'tellraw {playername} "Error:エラーコード WTP-3"')
                    time.sleep(0.1)
                    mcr.command(f'tellraw {playername} "TP:ここはオーバーワールドの初期スポーン地点です。"')
            elif _dimension == "e": #テレポートしたい先がeveryoneだったら
                mcr.command(f'mv tp {playername} everyone')
                time.sleep(0.1)
                mcr.command(f'tellraw {playername} "TP:Everyoneワールドに接続しました。"')
                time.sleep(0.1)
                mcr.command(f'gamemode survival {playername}')

            elif _dimension == "v":
                mcr.command(f'mv tp {playername} vs_setup')
                time.sleep(0.1)
                mcr.command(f'tellraw {playername} "TP:PVP準備ワールドに接続しました。ご武運を。"')
                time.sleep(0.1)
                mcr.command(f'gamemode adventure {playername}')

            elif _dimension == "w":
                if playername == "yt0f1": #ブラックリスト入り
                    mcr.command(f'tellraw {playername} "Error:エラーコード:WTP-2')
                else:    
                    mcr.command(f'mv tp {playername} weekly_end')
                    time.sleep(0.1)
                    mcr.command(f'tellraw {playername} "TP:ウィークリーエンドに接続しました。')
                    time.sleep(0.1)
                    mcr.command(f'gamemode survival {playername}')

            elif _dimension == "g":
                _item = mcr.command(f'data get entity {playername} Inventory')
                print(f'_item:{_item}')
            
            else:  #登録された引数以外を入力していたら
                mcr.command(f'tellraw {playername} "Error:エラーコード WTP-1"') #ワールド引数不明
                #まずオーバーワールドに飛ばす。
                #次にrcon-homecommand.pyを利用してプレイヤーのホームポイントへ飛ばす。
                #エラーを吐いたら初期スポのまま。rcon-homecommand.pyの方でエラーメッセージを出してくれるのでそれに追加する形。
    
    else: #許可されたプレイヤーリストの中に存在しなかった時
        with MCRcon('localhost','minecraft',25700) as mcr:
            if _dimension == "e": #everyoneワールドに接続を希望していたら
                mcr.command(f'mv tp {playername} everyone')
                time.sleep(0.1)
                mcr.command(f'tellraw {playername} "TP:Everyoneワールドに転送されました。"')
                time.sleep(0.1)
                mcr.command(f'gamemode survival {playername}')

            elif _dimension == "l": #ロビーに接続を希望していたら
                mcr.command(f'mv tp {playername} test')
                time.sleep(0.1)
                mcr.command(f'tellraw {playername} "TP:ロビーに転送されました。')
                time.sleep(0.1)
                mcr.command(f'gamemode adventure {playername}')
            
            elif _dimension == "v":
                mcr.command(f'mv tp {playername} vs_setup')
                time.sleep(0.1)
                mcr.command(f'tellraw {playername} "TP:PVP準備ワールドに接続しました。ご武運を。"')
                time.sleep(0.1)
                mcr.command(f'gamemode adventure {playername}')

            else:
                mcr.command(f'tellraw {playername} "Error:エラーコード WTP-2"') #接続権限無し
                time.sleep(0.1)
                mcr.command(f'tellraw {playername} "Error:接続可能なワールドでお楽しみください。"')


sys.exit()