import sys,re,time
from mcrcon import MCRcon
time.sleep

playername = sys.argv[1] #挑戦状を出したプレイヤーの名前    
challengername = sys.argv[2] #挑戦状を受け取ったプレイヤーの名前

try:
    challengername = challengername.replace('\n','')
except:
    pass
player_list = [playername,challengername]

if playername == challengername:
    with MCRcon('localhost','minecraft',25700) as mcr:
        mcr.command(f'tellraw {playername} "Error:エラーコード:VS-2/自分と向き合うにはあまりにも世界が小さすぎる"')
        sys.exit()

#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
with MCRcon('localhost','minecraft',25700) as mcr:
    player_dimension = mcr.command(f'data get entity {playername} Dimension')
    time.sleep(0.02)
    challenger_dimension = mcr.command(f'data get entity {challengername} Dimension')
    
    player_dimension2 = str(player_dimension.find('vs_setup'))
    challenger_dimension2 = str(challenger_dimension.find('vs_setup'))
    if player_dimension2 == "-1":
        for i in player_list:
            mcr.command(f'tellraw {i} "Error:エラーコード:VS-3"')
            time.sleep(0.02)
        with open('./vs-test/vs-fighter.txt','w',encoding='utf-8') as _open:
            _open.write("")
        sys.exit()
    elif challenger_dimension2 == "-1":
        for i in player_list:
            mcr.command(f'tellraw {i} "Error:エラーコード:VS-3"')
            time.sleep(0.02)
        with open('./vs-test/vs-fighter.txt','w',encoding='utf-8') as _open:
            _open.write("")
        sys.exit()
    

#両方の合意が得られなかったら終了
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
    


with MCRcon('localhost','minecraft',25700) as mcr:
    with open('./vs-test/vs-fighter.txt','w',encoding='utf-8') as vs_write:
        vs_write.write(f'1:{playername},2:{challengername}')
    

    player_list = [playername,challengername]
    for i in player_list:
        mcr.command(f'mv tp {i} vs')
        time.sleep(0.01)
        mcr.command(f'gamemode adventure {i}')
        time.sleep(0.01)
    
    mcr.command(f'execute at {playername} run tp {playername} 0 -60 -2') #相手の方を向いている
    time.sleep(0.03)
    mcr.command(f'execute at {challengername} run tp {challengername} 0 -60 2 ~180 ~') #あらぬ方向を向いているので向き変更
    time.sleep(0.01)
    mcr.command(f'execute at {playername} run setblock 0 -57 -2 glass replace') #頭上にガラス設置
    time.sleep(0.01)
    mcr.command(f'execute at {challengername} run setblock 0 -57 2 glass replace') #頭上にガラス設置
    time.sleep(0.01)
    mcr.command(f'execute at {playername} run fill 5 -59 0 -5 -60 0 glass replace') #プレイヤーを仕切るガラス設置
    for i in player_list:
        mcr.command(f'effect give {i} minecraft:slowness 10 250 true') #移動速度低下LV250を10秒間
        time.sleep(0.01)
        mcr.command(f'effect give {i} minecraft:jump_boost 10 250 true') #跳躍力上昇Lv250(負の跳躍力上昇)を10秒間
        time.sleep(0.01)

    _count = 5

    for i in range(5): #5秒間待機させる
        for i in player_list:
            mcr.command(f'title {i} title "{_count}秒前"')
            time.sleep(0.01)
        time.sleep(1)
        _count -= 1
    
    for i in player_list:
        mcr.command(f'effect clear {i}') #与えた効果の解除
        time.sleep(0.01)
    for i in player_list:
        mcr.command(f'effect give {i} minecraft:health_boost 80 4 true')
        time.sleep(0.01)
        mcr.command(f'effect give {i} minecraft:instant_health 1 250 true')

    mcr.command(f'execute at {playername} run fill 10 -60 10 -10 -56 -10 air replace') #仕切りガラスの撤去
    time.sleep(0.01)
    for i in player_list:
        mcr.command(f'title {i} title "戦闘開始!!"') #タイトル表示
        time.sleep(0.01)
    time.sleep(1.5)
    for i in player_list:
        mcr.command(f'title {i} clear') #タイトル消し
        time.sleep(0.01)

    for i in range(120):
        player_health = mcr.command(f'data get entity {playername} Health')
        print(f'player_health:{player_health}')
        time.sleep(0.25)
        challenger_health = mcr.command(f'data get entity {challengername} Health')
        
        player_health_underbar = player_health.replace(' ','_')
        challenger_health_underbar = challenger_health.replace(' ','_')

        if player_health_underbar == "No_entity_was_found": #途中で切断したときの設定
            finish = 0
            break
        elif challenger_health_underbar == "No_entity_was_found": #途中で切断したときの設定
            finish = 0
            break

        player_health_re = re.compile(r'(\d{1,2}).(\d{1,6})')
        p_results = player_health_re.finditer(player_health)
        for i in p_results:
            print(f'player health:{str(i.group(1))}')
            player_health = int(i.group(1))
             #プレイヤーの体力(int)
        print(f'player_health:{player_health}')

        c_results = player_health_re.finditer(challenger_health)
        for i in c_results:
            print(f'challenger health:{str(i.group(1))}')
            challenger_health = int(i.group(1))
        

        if player_health <= 20:
            mcr.command(f'tellraw @a "{challengername}が{playername}に勝利しました!!"')
            finish = 1
            for i in player_list:
                mcr.command(f'effect clear {i}')
                time.sleep(0.01)
            break
        elif challenger_health <= 20:
            mcr.command(f'tellraw @a "{playername}が{challengername}に勝利しました!!"')
            for i in player_list:
                mcr.command(f'effect clear {i}')
                time.sleep(0.01)
            finish = 1
            break
        else:
            finish = 0
            time.sleep(0.2)
        
        #120回ループここまで
        #---------------------------------------------------------------------
        
    
    if finish == 0:
        mcr.command(f'tellraw @a "==Draw=="')
        time.sleep(0.01)
        mcr.command(f'tellraw @a "{playername} v.s. {challengername}"')
        time.sleep(0.01)
        mcr.command(f'tellraw @a "==Draw=="')
        for i in player_list:
            mcr.command(f'effect clear {i}')
            time.sleep(0.01)


with open('./vs-test/vs-fighter.txt','w',encoding='utf-8') as vs_writer:
    vs_writer.write('') #PVPを行うプレイヤーの名前を消す

with open('./vs-test/vs-allow.txt','w',encoding='utf-8') as allow_erase:
    allow_erase.write('') #双方の同意を消す


for i in player_list:
    with MCRcon('localhost','minecraft',25700) as mcr:
        time.sleep(0.05)
        mcr.command(f'mv tp {i} test')
        time.sleep(0.03)
        mcr.command(f'effect give {i} minecraft:instant_heal 10 100')
        time.sleep(0.03)







    
    