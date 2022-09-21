from re import M
import sys,time
#from click import command
from mcrcon import MCRcon

#subprocessで実行されているので、実行時の引数を取得
playername = sys.argv[1]
#playername = 'ytshiyugh' 
#command_type = 'tel' 
command_type = sys.argv[2]

#command_type = "tel" or "set" or "rem"

#mcrconを利用してサーバ－と通信
def home_registration(): #登録
    with MCRcon('localhost','minecraft',25700) as mcr:
        position = mcr.command(f'data get entity {playername} Pos') #data get entity で座標などを取得
        dimension = mcr.command(f'data get entity {playername} Dimension')#ディメンジョン取得

        #座標の成型
        #_make_position1 = position[42:-1]
        #_make_position2 = _make_position1.replace('d','')

        bracket1st = position.find('[')

        bracket2nd = position[bracket1st:]
        print(bracket2nd)
        bracket3rd = bracket2nd.replace('d','')
        bracket4th = bracket3rd.replace(',','')
        bracket5th = bracket4th.replace('[','')
        bracket6th = bracket5th.replace(']','')
        print(bracket6th)

        

        #ディメンジョンの成型
        _make_dimension1 = dimension.find('"')
        _make_dimension2 = dimension[_make_dimension1:]    

        if _make_dimension2 != '"minecraft:overworld"': #登録しようとしている地点がオーバーワールド以外だったら警告を出す。
            mcr.command(f'tellraw {playername} "Error:ホームポイントに登録できるのはオーバーワールドだけです!"')
            time.sleep(0.01)
            mcr.command(f'tellraw {playername} "Error:ホームポイントは登録されませんでした"')
        else:
            #データベース(笑)への書き込み
            with open(f'./home-location/{playername}.txt','w',encoding='utf-8') as data_write:
                data_write.write(f"1:{playername},2:{bracket6th},3:{_make_dimension2}")


            print(f"position:{bracket6th}")

            #操作を行ったプレイヤーに報告
            mcr.command(f'tellraw {playername} "Set:現在の座標をあなたのホームポイントとして設定しました。"')
            time.sleep(0.03)


def home_remove(): #消去
    #無でプレイヤーのホームポイント上書き＝削除
    with open(f'./home-location/{playername}.txt','w',encoding='utf-8') as remove:
        remove.write("")

        #プレイヤーに報告
        with MCRcon('localhost','minecraft',25700) as mcr:
            mcr.command(f'tellraw {playername} "Remove:あなたのホームポイントは削除されました。"')
            time.sleep(0.03)
        
def home_tp(): #TP
    try:
        with open(f'./home-location/{playername}.txt','r',encoding='utf-8') as tp_read:
            tp_locate = tp_read.read()

            if tp_locate == "":
                with MCRcon('localhost','minecraft',25700) as mcr:
                    mcr.command(f'tellraw {playername} "TP:座標が登録されていません。TP失敗。"')

            else:

            #1:[プレイヤーネーム],2:[座標],3:["ディメンジョン"]の形で記録されている
            #print(f'tp_locate:{tp_locate}')

                make_locate1 = tp_locate.find(',2:')
                make_locate2 = make_locate1 - 1
                make_locate3 = tp_locate[2:make_locate2]#プレイヤーネーム

                make_locate4 = tp_locate.find(',2:')
                make_locate5 = make_locate4 + 3  #座標最初
                make_locate6 = tp_locate.find(',3:')
                make_locate7 = make_locate6 -1  #座標終了
                make_locate8 = tp_locate[make_locate5:make_locate7] #座標
                print(make_locate8)
                
                

                make_locate9 = tp_locate.find('"minecraft:')
                make_locate10 = tp_locate[make_locate9:-1]
                make_locate12 = make_locate10.replace('"minecraft:','')#ディメンジョン
                print(f'make_locate12:{make_locate12}')
                
                make_locate11 = make_locate8.replace(',','')#座標から,を抜いて直接tpに利用出来るようにする
                print(f'locate:{make_locate11}')

                if make_locate12 == "overworld":
                    make_locate13 = "world"
                elif make_locate12 == "the_end":
                    make_locate13 = "world_the_end"
                else:
                    make_locate13 = make_locate12
                #overworldのみファイル名がworldなので変換しなくてはいけない
                print(f'make_locate13:{make_locate13}')
            
                with MCRcon('localhost','minecraft',25700) as mcr:
                    mcr.command(f'gamemode survival {playername}')
                    mcr.command(f'mv tp {playername} {make_locate13}')#ディメンジョンの移動
                    print(f'teleport to :mv tp {playername} {make_locate13}')
                    time.sleep(0.03)
                    mcr.command(f'tellraw {playername} "TP:あなたのホームポイントが存在するディメンジョンに移動しました。"')
                    time.sleep(0.03)
                
                    mcr.command(f'tp {playername} {make_locate11}') #Java用。統合版だとなぜか通用しない。

                    try:
                        mcr.command(f'tp {playername}{make_locate11}') #統合版用。なぜか空白が入るのでそれの調整用。意味不。
                    except:
                        pass

                    #print(f"tp command:tp {playername} {make_locate11}") #確認テスト用
                    #print(f'tp {playername} {make_locate8}') #テスト用
                    time.sleep(0.03)
                    mcr.command(f'tellraw {playername} "TP:あなたのホームポイントへ移動しました。"')
                #mvtpでディメンジョン移動させた後にanchorへ移動させる。
    except:
        with MCRcon('localhost','minecraft',25700) as mcr:
            mcr.command(f'tellraw {playername} "Error:ホームポイントが登録されていません。TP失敗"')  

if __name__ == "__main__":
    with open('./vs-test/vs-fighter.txt','r',encoding='utf-8') as _check:
        _check_result = _check.read()
    player_fight_find = str(_check_result.find(playername))
    if player_fight_find == "-1":
        if command_type == "rem":
            home_remove()
        elif command_type == "tel":
            home_tp()
        elif command_type == "set":
            home_registration()
    else:
        with MCRcon('localhost','minecraft',25700) as mcr:
            mcr.command(f'tellraw {playername} "Error:エラーコード:WTP-4"')
    

sys.exit()