import requests
from bs4 import BeautifulSoup as bs
import re

nickname = ""
response = requests.get("https://maplestory.nexon.com/Ranking/World/Total?c=" + nickname)
soup = bs(response.text, 'html.parser')
inventory_link = soup.select_one('.search_com_chk').select_one('a').get('href').replace('?p', '/Inventory?p', 1)

response = requests.get("https://maplestory.nexon.com/" + inventory_link)
soup = bs(response.text, 'html.parser')

items = soup.select_one('.tab02_con_wrap').select('.inven_item_memo_title > h1 > a')

equip = soup.select_one('.tab01_con_wrap').select('.inven_item_memo')
use = [x.text for x in soup.select_one('.tab02_con_wrap').select('.inven_item_memo_title > h1 > a')]
etc = [x.text for x in soup.select_one('.tab03_con_wrap').select('.inven_item_memo_title > h1 > a')]
setup = [x.text for x in soup.select_one('.tab04_con_wrap').select('.inven_item_memo_title > h1 > a')]
cash = [x.text for x in soup.select_one('.tab05_con_wrap').select('.inven_item_memo_title > h1 > a')]

potential_dict = {
    '레어아이템': 1,
    '에픽아이템': 2,
    '유니크아이템': 3,
    '레전드리아이템': 4
}

equip_json = [{
    'name': x.select_one('.inven_item_memo_title > h1 > a').text.strip().replace('\xa0', '').split('\r\n')[0],
    'starforce': (lambda y: int(y.text.replace('성 강화', '')) if y else 0)(x.select_one('.inven_item_memo_title > h1 > a > em')),
    'potential': (lambda y: potential_dict.get(y.text.strip(), 0) if y else 0)(x.select_one('.item_memo_sel')),
   } for x in equip]

use_json = [{
    'name': re.search(r"[ \S]+(?= \(\d+개\))", x).group().strip(),
    'quantity': int(re.search(r"(?<=\()\d+(?=개\))", x).group())
    } for x in use]

etc_json = [{
    'name': re.search(r"[ \S]+(?= \(\d+개\))", x).group().strip(),
    'quantity': int(re.search(r"(?<=\()\d+(?=개\))", x).group())
    } for x in etc]

setup_json = [{
    'name': re.search(r"[ \S]+(?= \(\d+개\))", x).group().strip(),
    'quantity': int(re.search(r"(?<=\()\d+(?=개\))", x).group())
    } for x in setup]

cash_json = [{
    'name': (lambda y: y.group().strip() if y else x)(re.search(r"[ \S]+(?= \(\d+개\))", x)),
    'quantity': (lambda y: int(y.group()) if y else 1)(re.search(r"(?<=\()\d+(?=개\))", x))
    } for x in cash]

#print('\n'.join(map(lambda x: x.text, equip)))
#상세 정보
test = items[3].get('href')

data = {'p': test.split('?p=', 1)[1], '_': 1622164595842}
headers = {
    'Host': 'maplestory.nexon.com',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'close'
    }
res = requests.get("https://maplestory.nexon.com/" + test, headers=headers)

soup = bs(res.json()['view'].replace('\r', ''), 'html.parser')
