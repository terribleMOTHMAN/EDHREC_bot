
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import json
import httpx

API_TOKEN = '5151923541:AAE-ED8mZFj7FOlrkeP-mgYm5rasfeCLc0k'

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

main_kb = ReplyKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('/cards')).insert(KeyboardButton('/commanders')).insert(KeyboardButton('/advisor'))
top_kb = ReplyKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('/week')).insert(KeyboardButton('/month')).insert(KeyboardButton('/2years')).insert(KeyboardButton('/back'))

cards_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('top', callback_data='topc')).insert(KeyboardButton('saltiest', callback_data='saltiest'))

topc_kb = ReplyKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('/c-week')).insert(KeyboardButton('/c-month')).insert(KeyboardButton('/c-2years')).insert(KeyboardButton('/back'))

commanders_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('top', callback_data='top')).insert(KeyboardButton('partners', callback_data='partners'))\
    .insert(KeyboardButton('mono', callback_data='mono')).insert(KeyboardButton('2 colors', callback_data='2colors')).insert(KeyboardButton('3 colors', callback_data='3colors')).insert(KeyboardButton('4+ colors', callback_data='4+colors'))

partners_kb = ReplyKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('/all'))
partners_kb.insert(KeyboardButton('/blue')).insert(KeyboardButton('/black')).insert(KeyboardButton('/white')).insert(KeyboardButton('/red')).insert(KeyboardButton('/green'))
partners_kb.insert(KeyboardButton('/azorius')).insert(KeyboardButton('/dimir')).insert(KeyboardButton('/rakdos')).insert(KeyboardButton('/gruul')).insert(KeyboardButton('/selesnya'))
partners_kb.insert(KeyboardButton('/orzhov')).insert(KeyboardButton('/izzet')).insert(KeyboardButton('/golgari')).insert(KeyboardButton('/boros')).insert(KeyboardButton('/simic'))
partners_kb.insert(KeyboardButton('/esper')).insert(KeyboardButton('/grixis')).insert(KeyboardButton('/jund')).insert(KeyboardButton('/naya')).insert(KeyboardButton('/bant'))
partners_kb.insert(KeyboardButton('/abzan')).insert(KeyboardButton('/jeskai')).insert(KeyboardButton('/sultai')).insert(KeyboardButton('/mardu')).insert(KeyboardButton('/temur'))
partners_kb.insert(KeyboardButton('/wubr')).insert(KeyboardButton('/ubrg')).insert(KeyboardButton('/brgw')).insert(KeyboardButton('/rgwu')).insert(KeyboardButton('/gwub')).add(KeyboardButton('/back'))

mono_kb = ReplyKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('/mono-white')).insert(KeyboardButton('/mono-blue')).insert(KeyboardButton('/mono-black')).insert(KeyboardButton('/mono-red')).insert(KeyboardButton('/mono-green')).insert(KeyboardButton('/colorless')).add(KeyboardButton('/back'))
commanders_monowhite_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('w-commanders', callback_data='w-commanders')).insert(KeyboardButton('w-staples', callback_data='w-staples'))
commanders_monoblue_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('u-commanders', callback_data='u-commanders')).insert(KeyboardButton('u-staples', callback_data='u-staples'))
commanders_monoblack_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('b-commanders', callback_data='b-commanders')).insert(KeyboardButton('b-staples', callback_data='b-staples'))
commanders_monored_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('r-commanders', callback_data='r-commanders')).insert(KeyboardButton('r-staples', callback_data='r-staples'))
commanders_monogreen_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('g-commanders', callback_data='g-commanders')).insert(KeyboardButton('g-staples', callback_data='g-staples'))
commanders_colorless_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('c-commanders', callback_data='c-commanders')).insert(KeyboardButton('c-staples', callback_data='c-staples'))

twocolors_kb = ReplyKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('/с-azorius')).insert(KeyboardButton('/с-dimir')).insert(KeyboardButton('/с-rakdos'))\
    .insert(KeyboardButton('/c-gruul')).insert(KeyboardButton('/c-selesnya')).insert(KeyboardButton('/c-orzhov')).insert(KeyboardButton('/c-izzet'))\
    .insert(KeyboardButton('/c-golgari')).insert(KeyboardButton('/c-boros')).insert(KeyboardButton('/c-simic')).add(KeyboardButton('/back'))
commanders_azorius_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('uw-commanders', callback_data='uw-commanders')).insert(KeyboardButton('uw-staples', callback_data='uw-staples'))
commanders_dimir_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('ub-commanders', callback_data='ub-commanders')).insert(KeyboardButton('ub-staples', callback_data='ub-staples'))
commanders_rakdos_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('br-commanders', callback_data='br-commanders')).insert(KeyboardButton('br-staples', callback_data='br-staples'))
commanders_gruul_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('rg-commanders', callback_data='rg-commanders')).insert(KeyboardButton('rg-staples', callback_data='rg-staples'))
commanders_selesnya_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('gw-commanders', callback_data='gw-commanders')).insert(KeyboardButton('gw-staples', callback_data='gw-staples'))
commanders_orzhov_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('wb-commanders', callback_data='wb-commanders')).insert(KeyboardButton('wb-staples', callback_data='wb-staples'))
commanders_izzet_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('ur-commanders', callback_data='ur-commanders')).insert(KeyboardButton('ur-staples', callback_data='ur-staples'))
commanders_golgari_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('bg-commanders', callback_data='bg-commanders')).insert(KeyboardButton('bg-staples', callback_data='bg-staples'))
commanders_boros_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('rw-commanders', callback_data='rw-commanders')).insert(KeyboardButton('rw-staples', callback_data='rw-staples'))
commanders_simic_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('gu-commanders', callback_data='gu-commanders')).insert(KeyboardButton('gu-staples', callback_data='gu-staples'))

three_colors_kb = ReplyKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('/c-esper')).insert(KeyboardButton('/c-grixis'))\
    .insert(KeyboardButton('/c-jund')).insert(KeyboardButton('/c-naya')).insert(KeyboardButton('/c-bant')).insert(KeyboardButton('/c-abzan'))\
    .insert(KeyboardButton('/c-jeskai')).insert(KeyboardButton('/c-sultai')).insert(KeyboardButton('/c-mardu')).insert(KeyboardButton('/c-temur')).add(KeyboardButton('/back'))
commanders_esper_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('wub-commanders', callback_data='wub-commanders')).insert(KeyboardButton('wub-staples', callback_data='wub-staples'))
commanders_grixis_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('ubr-commanders', callback_data='ubr-commanders')).insert(KeyboardButton('ubr-staples', callback_data='ubr-staples'))
commanders_jund_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('brg-commanders', callback_data='brg-commanders')).insert(KeyboardButton('brg-staples', callback_data='brg-staples'))
commanders_naya_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('rgw-commanders', callback_data='rgw-commanders')).insert(KeyboardButton('rgw-staples', callback_data='rgw-staples'))
commanders_bant_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('gwu-commanders', callback_data='gwu-commanders')).insert(KeyboardButton('gwu-staples', callback_data='gwu-staples'))
commanders_abzan_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('wbg-commanders', callback_data='wbg-commanders')).insert(KeyboardButton('wbg-staples', callback_data='wbg-staples'))
commanders_jeskai_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('urw-commanders', callback_data='urw-commanders')).insert(KeyboardButton('urw-staples', callback_data='urw-staples'))
commanders_sultai_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('bgu-commanders', callback_data='bgu-commanders')).insert(KeyboardButton('bgu-staples', callback_data='bgu-staples'))
commanders_mardu_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('rwb-commanders', callback_data='rwb-commanders')).insert(KeyboardButton('rwb-staples', callback_data='rwb-staples'))
commanders_temur_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('gur-commanders', callback_data='gur-commanders')).insert(KeyboardButton('gur-staples', callback_data='gur-staples'))

four_colors_kb = ReplyKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('/c-wubr')).insert(KeyboardButton('/c-ubrg')).insert(KeyboardButton('/c-brgw'))\
    .insert(KeyboardButton('/c-rgwu')).insert(KeyboardButton('/c-gwub')).insert(KeyboardButton('/c-wubrg')).add(KeyboardButton('/back'))
commanders_wubr_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('wubr-commanders', callback_data='wubr-commanders')).insert(KeyboardButton('wubr-staples', callback_data='wubr-staples'))
commanders_ubrg_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('ubrg-commanders', callback_data='ubrg-commanders')).insert(KeyboardButton('ubrg-staples', callback_data='ubrg-staples'))
commanders_brgw_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('brgw-commanders', callback_data='brgw-commanders')).insert(KeyboardButton('brgw-staples', callback_data='brgw-staples'))
commanders_rgwu_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('rgwu-commanders', callback_data='rgwu-commanders')).insert(KeyboardButton('rgwu-staples', callback_data='rgwu-staples'))
commanders_gwub_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('gwub-commanders', callback_data='gwub-commanders')).insert(KeyboardButton('gwub-staples', callback_data='gwub-staples'))
commanders_wubrg_kb = InlineKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('wubrg-commanders', callback_data='wubrg-commanders')).insert(KeyboardButton('wubrg-staples', callback_data='wubrg-staples'))

advisor_kb = ReplyKeyboardMarkup(resize_keyboard=True).insert(KeyboardButton('/info'))

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer('Hello world!', reply_markup=main_kb)

###################################################################
@dp.message_handler(commands=['commanders'])
async def send_welcome(message: types.Message):
    await message.answer('Select an option! 🔧', reply_markup=commanders_kb)

@dp.callback_query_handler(lambda c: c.data == 'top')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Choose a time period! ⏰', reply_markup=top_kb)

@dp.message_handler(commands=['week'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/commanders/week.json')
    data = json.loads(resp.content)
    out = ''
    k = 0
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        if k == 100:
            break
        out += str(i['rank']) + ' ' + '[' + " ".join(i['names']) + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        k += 1
    out += 'Sorted by rank using edhrec.com/commanders/! The most popular commanders of the past week'
    await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['month'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/commanders/month.json')
    data = json.loads(resp.content)
    out = ''
    k = 0
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        if k == 100:
            break
        out += str(i['rank']) + ' ' + '[' + " ".join(i['names']) + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        k += 1
    out += 'Sorted by rank using edhrec.com/commanders/! The most popular commanders of the past manth'
    await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['2years'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/commanders/year.json')
    data = json.loads(resp.content)
    out = ''
    k = 0
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        if k == 100:
            break
        out += str(i['rank']) + ' ' + '[' + " ".join(i['names']) + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        k += 1
    out += 'Sorted by rank using edhrec.com/commanders/! The most popular commanders of the past 2 years'
    await message.answer(out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'partners')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Choose the colors!', reply_markup=partners_kb)

@dp.message_handler(commands=['all'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/partners.json')
    data = json.loads(resp.content)
    out = ''
    k = 0
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        k += 1
        out += str(k) + ' ' + '[' + " ".join(i['names']) + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
    out += 'All partners using edhrec.com/partners!'
    await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['white'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/partners/w.json')
    data = json.loads(resp.content)
    out = ''
    k = 0
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        k += 1
        out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
    out += 'All mono-white partners using edhrec.com/partners/w!'
    await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['blue'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/partners/u.json')
    data = json.loads(resp.content)
    out = ''
    k = 0
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        k += 1
        out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
    out += 'All mono-blue partners using edhrec.com/partners/u!'
    await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['black'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/partners/b.json')
    data = json.loads(resp.content)
    out = ''
    k = 0
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        k += 1
        out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
    out += 'All mono-black partners using edhrec.com/partners/b!'
    await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['red'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/partners/r.json')
    data = json.loads(resp.content)
    out = ''
    k = 0
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        k += 1
        out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
    out += 'All mono-red partners using edhrec.com/partners/r!'
    await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['green'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/partners/g.json')
    data = json.loads(resp.content)
    out = ''
    k = 0
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        k += 1
        out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
    out += 'All mono-green partners using edhrec.com/partners/w!'
    await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['azorius'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/partners/wu.json')
    data = json.loads(resp.content)
    out = ''
    k = 0
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        k += 1
        out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
    out += 'All azorius partners using edhrec.com/partners/wu!'
    await message.answer(out, parse_mode='Markdown')
    await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['dimir'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/partners/ub.json')
    data = json.loads(resp.content)
    out = ''
    k = 0
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        k += 1
        out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
    out += 'All dimir partners using edhrec.com/partners/ub!'
    await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['rakdos'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/partners/br.json')
    data = json.loads(resp.content)
    out = ''
    k = 0
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        k += 1
        out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
    out += 'All rakdos partners using edhrec.com/partners/br!'
    await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['gruul'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/partners/rg.json')
    data = json.loads(resp.content)
    out = ''
    k = 0
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        k += 1
        out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
    out += 'All gruul partners using edhrec.com/partners/rg!'
    await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['selesnya'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/partners/gw.json')
    data = json.loads(resp.content)
    out = ''
    k = 0
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        k += 1
        out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
    out += 'All selesnya partners using edhrec.com/partners/gw!'
    await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['orzhov'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/partners/wb.json')
    data = json.loads(resp.content)
    out = ''
    k = 0
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        k += 1
        out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
    out += 'All orzhov partners using edhrec.com/partners/wb!'
    await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['izzet'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/ur.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All izzet partners using edhrec.com/partners/ur!'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['golgari'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/bg.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All golgari partners using edhrec.com/partners/bg!'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['boros'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/rw.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All boros partners using edhrec.com/partners/rw! \n'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['simic'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/gu.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All simic partners using edhrec.com/partners/gu! \n'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['esper'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/wub.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All esper partners using edhrec.com/partners/wub! \n'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['grixis'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/ubr.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All grixis partners using edhrec.com/partners/ubr! \n'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['jund'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/ubr.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All jund partners using edhrec.com/partners/brg! \n'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['naya'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/rgw.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All naya partners using edhrec.com/partners/rgw! \n'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['bant'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/gwu.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All bant partners using edhrec.com/partners/gwu! \n'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['abzan'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/wbg.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All abzan partners using edhrec.com/partners/wbg! \n'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['jeskai'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/urw.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All jeskai partners using edhrec.com/partners/urw! \n'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['sultai'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/bgu.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All sultai partners using edhrec.com/partners/bgu! \n'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['mardu'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/rwb.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All mardu partners using edhrec.com/partners/rwb! \n'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['temur'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/gur.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All temur partners using edhrec.com/partners/gur! \n'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['wubr'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/wubr.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All Yore-Tiller partners using edhrec.com/partners/wubr! \n'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['ubrg'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/ubrg.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All Glint-Eye partners using edhrec.com/partners/ubrg! \n'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['brgw'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/brgw.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All Dune-Brood partners using edhrec.com/partners/brgw! \n'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['rgwu'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/rgwu.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All Ink-Treader partners using edhrec.com/partners/rgwu! \n'
        await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['gwub'])
async def send_welcome(message: types.Message):
        resp = httpx.get('https://json.edhrec.com/partners/gwub.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All Witch-Maw partners using edhrec.com/partners/gwub! \n'
        await message.answer(out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'mono')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Choose a color!', reply_markup=mono_kb)

@dp.message_handler(commands=['mono-white'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_monowhite_kb)

@dp.callback_query_handler(lambda c: c.data == 'w-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/w.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All mono-white commanders using edhrec.com/commanders/w! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'w-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/w.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All mono-white staples using edhrec.com/commanders/w! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['mono-blue'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_monoblue_kb)

@dp.callback_query_handler(lambda c: c.data == 'u-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/u.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All mono-blue commanders using edhrec.com/commanders/u! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'u-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/u.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All mono-blue staples using edhrec.com/commanders/u! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['mono-black'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_monoblack_kb)

@dp.callback_query_handler(lambda c: c.data == 'b-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/b.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All mono-black commanders using edhrec.com/commanders/b! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'b-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/b.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All mono-black staples using edhrec.com/commanders/b! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['mono-red'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_monored_kb)

@dp.callback_query_handler(lambda c: c.data == 'r-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/r.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All mono-red commanders using edhrec.com/commanders/r! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'r-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/b.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All mono-red staples using edhrec.com/commanders/r! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['mono-green'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_monogreen_kb)

@dp.callback_query_handler(lambda c: c.data == 'g-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/g.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All mono-green commanders using edhrec.com/commanders/r! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'g-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/g.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All mono-green staples using edhrec.com/commanders/g! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['colorless'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_colorless_kb)

@dp.callback_query_handler(lambda c: c.data == 'c-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/colorless.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All colorless commanders using edhrec.com/commanders/colorless! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'c-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/colorless.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All colorless staples using edhrec.com/commanders/colorless! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == '2colors')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Choose the colors!', reply_markup=twocolors_kb)

@dp.message_handler(commands=['с-azorius'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_azorius_kb)

@dp.callback_query_handler(lambda c: c.data == 'uw-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/wu.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All azorius commanders using edhrec.com/commanders/w! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'uw-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/wu.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All azorius staples using edhrec.com/commanders/w! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['с-dimir'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_dimir_kb)

@dp.callback_query_handler(lambda c: c.data == 'ub-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/ub.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All dimir commanders using edhrec.com/commanders/ub! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'ub-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/ub.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All dimir staples using edhrec.com/commanders/ub! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['с-rakdos'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_rakdos_kb)

@dp.callback_query_handler(lambda c: c.data == 'br-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/br.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All rakdos commanders using edhrec.com/commanders/br! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'br-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/br.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All rakdos staples using edhrec.com/commanders/br! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-gruul'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_gruul_kb)

@dp.callback_query_handler(lambda c: c.data == 'rg-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/rg.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All gruul commanders using edhrec.com/commanders/rg! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'rg-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/rg.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All gruul staples using edhrec.com/commanders/rg! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-selesnya'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_selesnya_kb)

@dp.callback_query_handler(lambda c: c.data == 'gw-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/gw.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All selesnya commanders using edhrec.com/commanders/gw! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'gw-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/gw.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All selesnya staples using edhrec.com/commanders/gw! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-orzhov'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_orzhov_kb)

@dp.callback_query_handler(lambda c: c.data == 'wb-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/wb.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All orzhov commanders using edhrec.com/commanders/wb! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'wb-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/wb.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All orzhov staples using edhrec.com/commanders/wb! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-izzet'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_izzet_kb)

@dp.callback_query_handler(lambda c: c.data == 'ur-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/ur.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All izzet commanders using edhrec.com/commanders/ur! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'ur-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/ur.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All izzet staples using edhrec.com/commanders/ur! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-golgari'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_golgari_kb)

@dp.callback_query_handler(lambda c: c.data == 'bg-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/bg.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All golgari commanders using edhrec.com/commanders/bg! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'bg-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/bg.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All golgari staples using edhrec.com/commanders/bg! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-boros'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_boros_kb)

@dp.callback_query_handler(lambda c: c.data == 'rw-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/rw.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All boros commanders using edhrec.com/commanders/rw! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'rw-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/rw.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All boros staples using edhrec.com/commanders/rw! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-simic'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_simic_kb)

@dp.callback_query_handler(lambda c: c.data == 'gu-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/gu.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All simic commanders using edhrec.com/commanders/gu! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'gu-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/gu.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All simic staples using edhrec.com/commanders/gu! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == '3colors')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Choose a color!', reply_markup=three_colors_kb)

@dp.message_handler(commands=['c-esper'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_esper_kb)

@dp.callback_query_handler(lambda c: c.data == 'wub-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/wub.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All esper commanders using edhrec.com/commanders/wub! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'wub-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/wub.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All esper staples using edhrec.com/commanders/wub! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-grixis'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_grixis_kb)

@dp.callback_query_handler(lambda c: c.data == 'ubr-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/ubr.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All grixis commanders using edhrec.com/commanders/ubr! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'ubr-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/ubr.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All grixis staples using edhrec.com/commanders/ubr! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-jund'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_jund_kb)

@dp.callback_query_handler(lambda c: c.data == 'brg-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/brg.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All jund commanders using edhrec.com/commanders/brg! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'brg-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/brg.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All jund staples using edhrec.com/commanders/brg! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-naya'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_naya_kb)

@dp.callback_query_handler(lambda c: c.data == 'rgw-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/rgw.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All naya commanders using edhrec.com/commanders/rgw! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'rgw-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/rgw.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All naya staples using edhrec.com/commanders/rgw! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-bant'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_bant_kb)

@dp.callback_query_handler(lambda c: c.data == 'gwu-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/gwu.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All bant commanders using edhrec.com/commanders/gwu! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'gwu-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/gwu.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All bant staples using edhrec.com/commanders/gwu! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-abzan'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_abzan_kb)

@dp.callback_query_handler(lambda c: c.data == 'wbg-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/wbg.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All abzan commanders using edhrec.com/commanders/wbg! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'wbg-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/wbg.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All abzan staples using edhrec.com/commanders/wbg! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-jeskai'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_jeskai_kb)

@dp.callback_query_handler(lambda c: c.data == 'urw-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/urw.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All jeskai commanders using edhrec.com/commanders/urw! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'urw-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/urw.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All jeskai staples using edhrec.com/commanders/urw! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-sultai'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_sultai_kb)

@dp.callback_query_handler(lambda c: c.data == 'bgu-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/bgu.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All sultai commanders using edhrec.com/commanders/bgu! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'bgu-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/bgu.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All sultai staples using edhrec.com/commanders/bgu! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-mardu'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_mardu_kb)

@dp.callback_query_handler(lambda c: c.data == 'rwb-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/rwb.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All mardu commanders using edhrec.com/commanders/rwb! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'rwb-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/rwb.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All mardu staples using edhrec.com/commanders/rwb! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-temur'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_temur_kb)

@dp.callback_query_handler(lambda c: c.data == 'gur-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/gur.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All temur commanders using edhrec.com/commanders/gur! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'gur-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/gur.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All temur staples using edhrec.com/commanders/gur! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == '4+colors')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Choose a color!', reply_markup=four_colors_kb)

@dp.message_handler(commands=['c-wubr'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_wubr_kb)

@dp.callback_query_handler(lambda c: c.data == 'wubr-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/wubr.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All Yore-Tiller commanders using edhrec.com/commanders/wubr! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'wubr-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/wubr.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All Yore-Tiller staples using edhrec.com/commanders/wubr! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-ubrg'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_ubrg_kb)

@dp.callback_query_handler(lambda c: c.data == 'ubrg-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/ubrg.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All Glint-Eye commanders using edhrec.com/commanders/ubrg! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'ubrg-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/ubrg.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All Glint-Eye staples using edhrec.com/commanders/ubrg! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-brgw'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_brgw_kb)

@dp.callback_query_handler(lambda c: c.data == 'brgw-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/brgw.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All Dune-Brood commanders using edhrec.com/commanders/brgw! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'brgw-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/brgw.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All Dune-Brood staples using edhrec.com/commanders/brgw! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-rgwu'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_rgwu_kb)

@dp.callback_query_handler(lambda c: c.data == 'rgwu-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/rgwu.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All Ink-Treader commanders using edhrec.com/commanders/rgwu! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'rgwu-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/rgwu.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All Ink-Treader staples using edhrec.com/commanders/rgwu! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-gwub'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_gwub_kb)

@dp.callback_query_handler(lambda c: c.data == 'gwub-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/gwub.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All Witch-Maw commanders using edhrec.com/commanders/gwub! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'gwub-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/gwub.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All Witch-Maw staples using edhrec.com/commanders/gwub! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['c-wubrg'])
async def send_welcome(message: types.Message):
    await message.answer('Choose an option! 🔧', reply_markup=commanders_wubrg_kb)

@dp.callback_query_handler(lambda c: c.data == 'wubrg-commanders')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/wubrg.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All Five-Color commanders using edhrec.com/commanders/wubrg! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'wubrg-staples')
async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        resp = httpx.get('https://json.edhrec.com/commanders/wubrg.json')
        data = json.loads(resp.content)
        out = ''
        k = 0
        for i in data['container']['json_dict']['cardlists'][1]['cardviews']:
            k += 1
            if len(i['names']) == 1:
                out += str(k) + ' ' + '[' + i['names'][0] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
            else:
                out += str(k) + ' ' + '[' + i['names'][0] + ' // ' + i['names'][1] + ']' + '(edhrec.com' + i[
                    'url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        out += 'All Five-Color staples using edhrec.com/commanders/wubrg! \n'
        await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['cards'])
async def send_welcome(message: types.Message):
    await message.answer('Select an option! 🔧', reply_markup=cards_kb)

@dp.callback_query_handler(lambda c: c.data == 'topc')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Choose a time period! ⏰', reply_markup=topc_kb)

@dp.message_handler(commands=['c-week'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/top/week.json')
    data = json.loads(resp.content)
    out = ''
    k = 1
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        out += str(k) + ' ' + '[' + " ".join(i['names']) + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        k += 1
    out += 'Sorted by rank using edhrec.com/top! The most popular cards of the past week'
    await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['c-month'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/top/month.json')
    data = json.loads(resp.content)
    out = ''
    k = 1
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        out += str(k) + ' ' + '[' + " ".join(i['names']) + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        k += 1
    out += 'Sorted by rank using edhrec.com/top! The most popular cards of the past month'
    await message.answer(out, parse_mode='Markdown')

@dp.message_handler(commands=['c-2years'])
async def send_welcome(message: types.Message):
    resp = httpx.get('https://json.edhrec.com/top/year.json')
    data = json.loads(resp.content)
    out = ''
    k = 1
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        out += str(k) + ' ' + '[' + " ".join(i['names']) + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(i['num_decks']) + '\n'
        k += 1
    out += 'Sorted by rank using edhrec.com/top! The most popular cards of the past 2 years'
    await message.answer(out, parse_mode='Markdown')

@dp.callback_query_handler(lambda c: c.data == 'saltiest')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    resp = httpx.get('https://json.edhrec.com/top/salt.json')
    data = json.loads(resp.content)
    out = ''
    k = 1
    for i in data['container']['json_dict']['cardlists'][0]['cardviews']:
        out += str(k) + ' ' + '[' + " ".join(i['names']) + ']' + '(edhrec.com' + i['url'] + ')' + ' ' + str(round(i['salt'], 2)) + ' ' + str(i['num_decks']) + '\n'
        k += 1
    out += 'Sorted by rank using edhrec.com/top! The most saltiest cards'
    await bot.send_message(callback_query.from_user.id, out, parse_mode='Markdown')

@dp.message_handler(commands=['advisor'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id, 'Type which commander you are interested in! \nExample typing: Heliod, Sun-Crowned \nExample typing for partners: Brinelin, the Moon Kraken Sakashima of a Thousand Faces')

@dp.message_handler()
async def send_welcome(msg: types.Message, state: FSMContext):
    commander = msg.text
    count = commander.count(',')
    for i in range(0, count):
        commander = commander.replace(',','')
    count = commander.count('-')
    for i in range(0, count):
        commander = commander.replace('-', ' ')
        commander = commander.lower()
        out = '-'.join(commander.split())
        link1 = 'https://json.edhrec.com/commanders/' + out + '.json'
        link2 = 'https://edhrec.com/commanders/' + out
        async with state.proxy() as data:
            data['link1'] = link1
            data['link2'] = link2
            await msg.answer(msg.from_user.id, 'Choose an option! 🔧', parse_mode='Markdown', reply_markup=advisor_kb)

@dp.message_handler(commands=['info'])
async def send_welcome(msg: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            link1 = data['link1']
            link2 = data['link2']
            commander_data = json.loads(link1)
            out = commander_data['container']['json_dict']['card']['image_uris'][0][1] + '\n' + '[' + commander_data['container']['json_dict']['card']['name'] + '](' \
                  + 'edhrec.com/' + link2 + ')'
            await msg.answer(msg.from_user.id, out, parse_mode='Markdown')
    except:
        print('ERROR')

#####################################################################
@dp.message_handler(commands=['back'])
async def some_func(msg: types.Message):
    await msg.answer('✅You are in main menu!', reply_markup=main_kb)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)