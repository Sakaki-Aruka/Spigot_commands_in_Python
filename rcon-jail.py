from pydoc import plainpager
import sys,time
from mcrcon import MCRcon

ban_target = sys.argv[1]
#print(f'ban_target:{ban_target}') #テスト用
ban_target2 = ban_target.replace('\n','') #なぜか改行が入ってしまっているので改行を取り除く

with MCRcon('localhost',"minecraft",25700) as mcr:
    mcr.command(f'mv tp {ban_target2} test')
    print('MCRcon30')
    time.sleep(0.01)
    #ここにリストからの削除とホームポイントの削除もついか

    #mcr.command(f'tp {ban_target2} -28 71 -253')
    #print(f'TEST:tp {ban_target2} -28 71 -253')
    time.sleep(0.03)
    mcr.command(f'tellraw {ban_target2} "貴方はモデレーターによって疑似BANされました。"')
    time.sleep(0.03)
    mcr.command(f'tellraw {ban_target2} "異議がある場合はPublicServer公式Discordの異議申し立てチャンネルで承ります。"')
    time.sleep(0.03)
    #mcr.command(f'tellraw {ban_target2} "なお、異議申し立てをしない場合はそのままBANとなります。"')
    print(f'tellraw {ban_target2} ')
    time.sleep(0.03)

    with open(f'./home-location/{ban_target2}.txt','w',encoding='utf-8') as home_remove:
        home_remove.write('')
        #疑似BAN対象者のホームポイントを削除する

sys.exit()