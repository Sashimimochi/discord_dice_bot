from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
import gspread
import discord
import numpy as np
from parse import parse
import json

def load_config():
    with open('config.json') as f:
        conf = json.load(f)
    return conf

def get_gs():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    json_file = conf['json_file']#OAuth用クライアントIDの作成でダウンロードしたjsonファイル
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scopes=scopes)
    http_auth = credentials.authorize(Http())

    # スプレッドシート用クライアントの準備
    doc_id = conf['doc_id']#これはスプレッドシートのURLのうちhttps://docs.google.com/spreadsheets/d/以下の部分です
    gs = gspread.authorize(credentials)
    gfile   = gs.open_by_key(doc_id)#読み書きするgoogle spreadsheet
    return gfile

def get_charactor(name):

    gfile = get_gs()

    #worksheetの名前はdiscordのユーザー名にしておく
    worksheet = gfile.worksheet(name)

    charactor = {}
    cell_keys = worksheet.col_values(1)
    cell_values = worksheet.col_values(2)
    for k,v in zip(cell_keys, cell_values):
        charactor[k] = v
    return charactor

def dice(dice_size):
    num = np.random.randint(1, int(dice_size))
    return num

def simple_dice(dice_size, dice_num):
    dice_val = np.array([], dtype=np.int64)    
    for i in range(dice_num):
        dice_val = np.append(dice_val, dice(dice_size))
    msg = 'dice: ' + str(np.sum(dice_val)) + ' = ' + str(dice_val)
    return msg

def judge(charactor, key, dice_size, dice_num):
    dice_val = np.array([], dtype=np.int64)
    for i in range(dice_num):
        dice_val = np.append(dice_val, dice(dice_size))
    if int(charactor[key]) >= np.sum(dice_val):
        msg = key + ' ' + str(charactor[key]) + ' >= ' + str(np.sum(dice_val)) + ' = ' + str(dice_val)
        if np.sum(dice_val) <= 5:
            msg += ' 【クリティカル】'
        msg += ' Success'
        return msg, True
    else:
        msg = key + ' ' + str(charactor[key]) + ' < ' + str(np.sum(dice_val)) + ' = ' + str(dice_val)
        if np.sum(dice_val) >= 96:
            msg += ' 【ファンブル】'
        msg += ' Fail'
        return msg, False

def damage(charactor, key):
    d = np.array([], dtype=np.int64)
    if key == 'こぶし':
        d = np.append(d, dice(3))
    elif key == '頭突き':
        d = np.append(d, dice(4))
    elif key == 'キック':
        d = np.append(d, dice(6))
    else:
        return None

    if 'd' in charactor['db']:
        result = parse('{}d{}', charactor['db'])
        dice_size = int(result[1])
        dice_num = int(result[0])
        for i in range(np.abs(dice_num)):
            if dice_num < 0:
                d = np.append(d, -dice(dice_size))
            else:
                d = np.append(d, dice(dice_size))
    return d


def temp_madness():
    roll = {}
    roll[1] = '鸚鵡返し（誰かの動作・発言を真似することしか出来なくなる）'
    roll[2] = '健忘症（1d6時間以内のことを忘れる）'
    roll[3] = '多弁症（何があってもひたすら喋り続ける）'
    roll[4] = '偏食症（奇妙なものを食べたくなる）'
    roll[5] = '頭痛・嘔吐などの体調不良（技能値に－5）'
    roll[6] = '暴力癖（誰彼構わず暴力を振るう）'
    roll[7] = '幻聴或いは一時的難聴（聞き耳半減。この症状の探索者に精神分析や説得などを試みる場合は技能値に－10）'
    roll[8] ='逃亡癖（その場から逃げようとする）'
    roll[9] = '吃音や失声などの発語障害（交渉技能の技能値が半減する）'
    roll[10] = '不信（単独行動をとりたがる。交渉技能不可。）'
    roll[11] = '恐怖による行動不能'
    roll[12] = '自傷癖（自傷行動を行う。ラウンドごと1d2のダメージ判定を行う）'
    roll[13] = '感情の噴出（泣き続ける、笑い続けるなど。自発行動が出来なくなる）'
    roll[14] = '気絶（精神分析・またはCON＊5のロールに成功で目覚める）'
    roll[15] = '幻覚あるいは妄想（目を使う技能は技能値に－30）'
    roll[16] = '偏執症（特定のものや行動に強く執着する）'
    roll[17] = 'フェティシズム（特定のものに性的魅惑を感じる）'
    roll[18] = '退行（乳幼児のような行動をとってしまう）'
    roll[19] = '自己愛（自分を守るために何でもしようとする）'
    roll[20] = '過信（自分を全能と信じて、どんなことでもしてしまう）'
    msg = roll[dice(20)]
    msg += '\n一時的狂気(' + str(dice(10)+4) + 'ラウンドまたは' + str(dice(6)*10+30) + '分)'
    return msg

def ind_madness():
    roll = {}
    roll[1] = '失語症（言葉を使う技能が使えなくなる）'
    roll[2] = '心因性難聴（聞き耳不可。精神分析を受ける際に技能値に－30）'
    roll[3] = '奇妙な性的嗜好（性的倒錯。特定のものに性的興奮を覚える）'
    roll[4] = '偏執症（特定のものや行動に異常に執着する）'
    roll[5] = '脱力・虚脱（自力での行動が出来なくなる）'
    roll[6] = '恐怖症（特定のものに強い恐怖を覚える。そのものが側に存在する場合、技能値に－20）'
    roll[7] = '自殺癖（ラウンドごとに1d4＋1のダメージ判定を行う）'
    roll[8] = '不信（単独行動をとりたがる。交渉技能不可。）'
    roll[9] = '幻覚（目を使う技能は技能値に－30）'
    roll[10] = '殺人癖（誰彼構わず殺そうとする） '
    msg = roll[dice(10)]
    msg += '\n不定の狂気(' + str(dice(10)*10) + '時間)'
    return msg

conf = load_config()
client = discord.Client()
client_id = conf['client_id']#discordのbotのid

@client.event
async def on_ready():
    print('Logged in')
    print('-----')

@client.event
async def on_message(message):
    # 開始ワード
    if message.content.startswith('dice'):
        # 送り主がBotじゃないか
        if client.user != message.author:
            info = parse('dice {}d{} {}', message.content)
            if info:
                if info[1].isdecimal() and info[0].isdecimal():
                    dice_num = int(info[0])
                    dice_size = int(info[1])
                    key = info[2]
                    # メッセージを書きます
                    m = message.author.name + ' '
                    if key == '一時的狂気':
                        m = temp_madness()
                    elif key == '不定の狂気':
                        m = ind_madness()
                    elif key == 'dice':
                        m = simple_dice(dice_size, dice_num)
                    else:
                        chara = get_charactor(str(message.author))
                        msg, result = judge(chara, key, dice_size, dice_num)
                        m += msg
                        if result:
                            d = damage(chara, key)
                        else:
                            d = None
                        if d is not None:
                            m += '\nダメージ: ' + str(np.sum(d)) + ' = ' + str(d)
                    # メッセージが送られてきたチャンネルへメッセージを送ります
                    await client.send_message(message.channel, m)

client.run(client_id)