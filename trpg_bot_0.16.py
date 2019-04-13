from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
import gspread
import discord
import numpy as np
from parse import parse
import json
import unicodedata

def get_east_asian_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count

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
    doc_id = conf['doc_id']##これはスプレッドシートのURLのうちhttps://docs.google.com/spreadsheets/d/以下の部分です
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
    cell_dice = worksheet.col_values(7)
    for k, v, d in zip(cell_keys, cell_values, cell_dice):
        if d == 'dice':
            dice_num = 0
            dice_size = 0
        else:
            dice_info = parse('{}d{}', d)
            dice_num = dice_info[0]
            dice_size = dice_info[1]
        charactor[k] = {
            'value': v,
            'dice_num': dice_num,
            'dice_size': dice_size
        }
    return charactor

def dice(dice_num, dice_size):
    return np.random.randint(1, int(dice_size), int(dice_num))

def judge(dice_array, ability):
    if int(ability) >= np.sum(dice_array):
        return True
    else:
        return False

def damage(charactor, key):
    d = np.array([], dtype=np.int64)
    if key == 'こぶし':
        d = np.append(d, dice(1, 3))
    elif key == '頭突き':
        d = np.append(d, dice(1, 4))
    elif key == 'キック':
        d = np.append(d, dice(1, 6))
    else:
        return None

    if charactor and 'd' in charactor['db']['value']:
        result = parse('{}d{}', charactor['db']['value'])
        dice_size = int(result[1])
        dice_num = int(result[0])
        if dice_num < 0:
            d = np.hstack([d, -dice(1, dice_size)])
        else:
            d = np.hstack([d, dice(1, dice_size)])
    return d


def temp_madness():
    roll = {}
    roll[1] = '鸚鵡返し（誰かの動作・発言を真似することしか出来なくなる）'
    roll[2] = '健忘症（1d6時間以内のことを忘れる）'
    roll[3] = '多弁症（何があってもひたすら喋り続ける）'
    roll[4] = '偏食症（奇妙なものを食べたくなる）'
    roll[5] = '頭痛・嘔吐などの体調不良（技能値に-5）'
    roll[6] = '暴力癖（誰彼構わず暴力を振るう）'
    roll[7] = '幻聴或いは一時的難聴（聞き耳半減。この症状の探索者に精神分析や説得などを試みる場合は技能値に-10）'
    roll[8] ='逃亡癖（その場から逃げようとする）'
    roll[9] = '吃音や失声などの発語障害（交渉技能の技能値が半減する）'
    roll[10] = '不信（単独行動をとりたがる。交渉技能不可。）'
    roll[11] = '恐怖による行動不能'
    roll[12] = '自傷癖（自傷行動を行う。ラウンドごと1d2のダメージ判定を行う）'
    roll[13] = '感情の噴出（泣き続ける、笑い続けるなど。自発行動が出来なくなる）'
    roll[14] = '気絶（精神分析・またはCON*5のロールに成功で目覚める）'
    roll[15] = '幻覚あるいは妄想（目を使う技能は技能値に-30）'
    roll[16] = '偏執症（特定のものや行動に強く執着する）'
    roll[17] = 'フェティシズム（特定のものに性的魅惑を感じる）'
    roll[18] = '退行（乳幼児のような行動をとってしまう）'
    roll[19] = '自己愛（自分を守るために何でもしようとする）'
    roll[20] = '過信（自分を全能と信じて、どんなことでもしてしまう）'
    msg = roll[dice(1, 20)[0]]
    msg += '\n一時的狂気(' + str(dice(1, 10)+4) + 'ラウンドまたは' + str(dice(1, 6)*10+30) + '分)'
    return msg

def ind_madness():
    roll = {}
    roll[1] = '失語症（言葉を使う技能が使えなくなる）'
    roll[2] = '心因性難聴（聞き耳不可。精神分析を受ける際に技能値に-30）'
    roll[3] = '奇妙な性的嗜好（性的倒錯。特定のものに性的興奮を覚える）'
    roll[4] = '偏執症（特定のものや行動に異常に執着する）'
    roll[5] = '脱力・虚脱（自力での行動が出来なくなる）'
    roll[6] = '恐怖症（特定のものに強い恐怖を覚える。そのものが側に存在する場合、技能値に-20）'
    roll[7] = '自殺癖（ラウンドごとに1d4+1のダメージ判定を行う）'
    roll[8] = '不信（単独行動をとりたがる。交渉技能不可。）'
    roll[9] = '幻覚（目を使う技能は技能値に-30）'
    roll[10] = '殺人癖（誰彼構わず殺そうとする） '
    msg = roll[dice(1, 10)[0]]
    msg += '\n不定の狂気(' + str(dice(1, 10)*10) + '時間)'
    return msg

def against(input_msg):
    active = int(input_msg[0])
    passive = int(input_msg[1])

    achivement = 50 + ( (active - passive) * 5)
    dice_array = dice(1, 100)

    result = judge(dice_array, achivement)
    if result:
        inequality = '>='
        result_msg = 'Success'
        if np.sum(dice_array) <= 5:
            result_msg += '【クリティカル】'
    else:
        inequality = '<'
        result_msg = 'Fail'
        if np.sum(dice_array) >= 96:
            result_msg += '【ファンブル】'

    return  '【対抗ロール】{active} VS {passive}'\
            ' : {achivement} {inequality} {dice_result} --> {result_msg}'.format(
                active = active,
                passive = passive,
                achivement = achivement,
                inequality = inequality,
                dice_result = np.sum(dice_array),
                result_msg = result_msg
            )

def charactor_make():
    status = {}
    status['STR'] = np.sum(dice(3, 6))
    status['CON'] = np.sum(dice(3, 6))
    status['POW'] = np.sum(dice(3, 6))
    status['DEX'] = np.sum(dice(3, 6))
    status['APP'] = np.sum(dice(3, 6))
    status['SIZ'] = np.sum(dice(2, 6)) + 6
    status['INT'] = np.sum(dice(2, 6)) + 6
    status['EDU'] = np.sum(dice(3, 6)) + 3

    print('---')
    for k,v in status.items():
        if  8 <= v and v <= 12:
            correction = np.random.rand()
            if correction > 0.7:
                new_v = v + np.sum(dice(3, 4))
                print(v, new_v)
                status[k] = new_v if new_v <= 21 else 21
            elif correction < 0.1:
                new_v = v - np.sum(dice(2, 3))
                print(v, new_v)
                status[k] = new_v if new_v >= 3 else 3
    if status['SIZ'] < 8:
        status['SIZ'] = 8
    if status['INT'] < 8:
        status['INT'] = 8
    if status['EDU'] < 6:
        status['EDU'] = 6

    status['HP'] = int((status['CON'] + status['SIZ']) / 2)
    status['MP'] = status['POW']
    status['SAN'] = status['POW'] * 5
    status['アイディア'] = status['INT'] * 5
    status['幸運'] = status['POW'] * 5
    status['知識'] = status['EDU'] * 5
    
    ATK = (status['STR'] + status['SIZ'])
    if 2 <= ATK and ATK <= 12:
        status['db'] = '-1d6'
    elif 13 <= ATK and ATK <= 16:
        status['db'] = '-1d4'
    elif 17 <= ATK and ATK <= 24:
        status['db'] = '0d0'
    elif 25 <= ATK and ATK <= 32:
        status['db'] = '1d4'
    elif 33 <= ATK and ATK <= 40:
        status['db'] = '1d6'
    elif 41 <= ATK and ATK <= 56:
        status['db'] = '2d6'
    elif 57 <= ATK and ATK <= 72:
        status['db'] = '3d6'

    msg = ''
    for k, v in zip(status.keys(), status.values()):
        msg += '{k} {v} \n'.format(k=k, v=v)
    return msg

def simple_dice(input_msg):
    def single_dice(msg, opt):
        dice_info = msg.split('d')
        dice_num = int(dice_info[0])
        dice_size = int(dice_info[1])
        return np.array([int(opt+str(d)) for d in dice(dice_num, dice_size)])

    secret = None
    top_secret = None
    ability = None

    msg = input_msg[0]
    # ||を除去
    msg = msg.replace('||', '')

    # 返り値を全て隠す
    if 'top_secret' in msg:
        msg = parse('{} top_secret', msg)[0]
        top_secret = True
    # ダイス結果だけ表示する
    elif 'secret' in msg:
        msg = parse('{} secret', msg)[0]
        secret = True

    # ()を除去する
    if '(' in msg:
        tmp = parse('{}({})', msg)
        ability = tmp[1]
        msg = tmp[0]
        dice_size = 100

    dice_array = np.array([], dtype=np.int64)

    operator = ('+', '-')
    opts = list()

    if not msg.startswith('-'):
        msg = '+' + msg

    while any(m in msg for m in operator):
        # 文頭から数えて最初に出てくる演算子を探す
        opts.append(operator[np.argmin([msg.find(opt) if msg.find(opt)>=0 else 999 for opt in operator])])
        # 初回は演算子を取り出すだけ
        if len(opts) == 1:
            msg_tmp = msg.split(opts[0], 1)
            msg = msg_tmp[1]
            continue
        else:
            msg_tmp = msg.split(opts[1], 1)

        opt = opts.pop(0)
        # diceを振る
        if 'd' in msg_tmp[0]:
            dice_result = single_dice(msg_tmp[0], opt)
            dice_array = np.append(dice_array, dice_result)
        # 固定値
        else:
            dice_array = np.append(dice_array, int(opt+msg_tmp[0]))
            
        msg = msg_tmp[1] # 残りのテキストを取り出す
    else: # 最後のテキストに対する処理
        opt = opts.pop(0)
        if 'd' in msg:
            dice_result = single_dice(msg, opt)
            dice_array = np.append(dice_array, dice_result)
        else:
            dice_array = np.append(dice_array, int(opt+msg))

    # 技能判定
    if ability:
        result = judge(dice_array, ability)
        result_msg = '--> '
        (inequality, _, msg) = result_message(dice_size, dice_array, result)
        result_msg += msg
    else:
        (inequality, _, result_msg) = ('', '', '')

    # シークレットメッセージにする
    if secret:
        secret = '||'
    else:
        secret = ''
    if top_secret:
        top_secret = '||'
    else:
        top_secret = ''

    return_msg = '【ダイス】({secret}{ability}{secret}):{inequality} {dice_result}={dice_array} {result_msg}'.format(
        secret = secret,
        ability = ability,
        inequality = inequality,
        dice_result = np.sum(dice_array),
        dice_array = dice_array,
        result_msg = result_msg)

    dummy_blank = ''
    if '【' in result_msg:
        count_len = 70
    else:
        if 'Fail' in return_msg:
            count_len = 92
        else:
            count_len = 84


    while get_east_asian_width_count(return_msg+dummy_blank) < count_len:
        dummy_blank += ' '

    print(return_msg+dummy_blank)
    print(get_east_asian_width_count(return_msg+dummy_blank))

    return '【ダイス】{top_secret}({secret}{ability}{secret}):{inequality} {dice_result}={dice_array} {result_msg}{dummy_blank}{top_secret}'.format(
        top_secret = top_secret,
        secret = secret,
        ability = ability,
        inequality = inequality,
        dice_result = np.sum(dice_array),
        dice_array = dice_array,
        result_msg = result_msg,
        dummy_blank = dummy_blank)

def result_message(dice_size, dice_array, result=None, charactor=None, ability_name=None):
    if result:
        inequality = '>='
        result_msg = 'Success'
        if dice_size == 100 and np.sum(dice_array) <= 5:
            result_msg += '【クリティカル】'
        d = damage(charactor=charactor, key=ability_name)
        if d is not None:
            result_msg += '\nダメージ:{dice_result}={dice_array}'.format(
                dice_result = np.sum(d),
                dice_array = d)
    else:
        inequality = '<'
        result_msg = 'Fail'
        if dice_size == 100 and np.sum(dice_array) >= 96:
            result_msg += '【ファンブル】'
        d = None

    return (inequality, d, result_msg)


def dice_message(input_msg, message):
    if '不定の狂気' in input_msg:
        return ind_madness()
    elif '一時的狂気' in input_msg:
        return temp_madness()
    elif 'cm' in input_msg:
        return charactor_make()
    elif 'VS' in message.content:
        return against(input_msg)
    elif 'dice' in message.content: #技能値判定無しのダイス
        return simple_dice(input_msg)
    else:
        charactor = get_charactor(str(message.author))

        if len(input_msg) == 3:
            dice_num = input_msg[0]
            dice_size = input_msg[1]
            ability_name, ability, ability_detail = calc_ability(input_msg[2], charactor)
        elif len(input_msg) == 1:
            ability_name, ability, ability_detail = calc_ability(input_msg[0], charactor)
            dice_num = charactor[ability_name]['dice_num']
            dice_size = charactor[ability_name]['dice_size']

        dice_num = int(dice_num)
        dice_size = int(dice_size)
        dice_array = dice(dice_num, dice_size)
        result = judge(dice_array, ability)

        (inequality, d, result_msg) = result_message(dice_size, dice_array, result, charactor, ability_name)

        return  '【{ability_name}】{operator} {correction} : '\
                '{base_ability}{operator}{correction} = {ability}'\
                '{inequality} {dice_result} = {dice_array} {result_msg}'.format(
                    ability_name = ability_name,
                    ability = ability,
                    base_ability = ability_detail[0],
                    operator = ability_detail[1],
                    correction = ability_detail[2],
                    inequality = inequality,
                    dice_result = np.sum(dice_array),
                    dice_array = dice_array,
                    result_msg = result_msg)

def calc_ability(input_msg, charactor):
    operators = ['+', '-', '*', '/']
    for opt in operators:
        if  opt in input_msg:
            parsed_msg = parse('{}'+opt+'{}', input_msg)
            ability_name = parsed_msg[0]
            correction = parsed_msg[1]
            operator = opt
            ability = eval(
                charactor[ability_name]['value']+operator+correction
            )
            break
    else:
        ability_name = input_msg
        correction = ''
        operator = ''
        ability = charactor[ability_name]['value']

    return ability_name, int(ability), (charactor[ability_name]['value'], operator, correction)

def bot_startswitch(message):
    # 開始ワード
    if message.content.startswith('/dice'):
        return parse('/dice {}', message.content)
        #return parse('/dice {}d{}', message.content)
    elif message.content.startswith('dice'):
        return parse('dice {}d{} {}', message.content)
    elif message.content.startswith('/'):
        return parse('/{}', message.content)
    elif message.content.startswith('VS'):
        return parse('VS {}/{}', message.content)
    else:
        return None

conf = load_config()
client = discord.Client()
client_id = conf['client_id']

@client.event
async def on_ready():
    print('Logged in')
    print('-----')

@client.event
async def on_message(message):
    # 送り主がBotじゃないか
    if client.user != message.author:
        # 開始ワード
        input_msg = bot_startswitch(message).fixed
        if input_msg is not None:
            m = message.author.name + '\n'
            m += dice_message(input_msg, message)
        # メッセージが送られてきたチャンネルへメッセージを送ります
            await client.send_message(message.channel, m) # discord.py ver0.16

client.run(client_id)