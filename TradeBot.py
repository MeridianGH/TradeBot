import time
from steampy.client import SteamClient
from urllib.request import Request, urlopen

# Important variables
api_key = ''
steamguard_path = ''
username = ''
password = ''


def value_to_items(value):
    items = []
    for i in range(int(float(value))):
        items.append('Refined Metal')
    scrap = str(value)[-2:]
    if scrap == '.0':
        return items
    else:
        if scrap == '11':
            items.append('Scrap Metal')
        if scrap == '22':
            items.extend(('Scrap Metal', 'Scrap Metal'))
        if scrap == '33':
            items.append('Reclaimed Metal')
        if scrap == '44':
            items.extend(('Reclaimed Metal', 'Scrap Metal'))
        if scrap == '55':
            items.extend(('Reclaimed Metal', 'Scrap Metal', 'Scrap Metal'))
        if scrap == '66':
            items.extend(('Reclaimed Metal', 'Reclaimed Metal'))
        if scrap == '77':
            items.extend(('Reclaimed Metal', 'Reclaimed Metal', 'Scrap Metal'))
        if scrap == '88':
            items.extend(('Reclaimed Metal', 'Reclaimed Metal', 'Scrap Metal', 'Scrap Metal'))
        return items


def round_to_ref(value):
    value = str(round(value, 2))
    if '.' not in value:
        value = value + '.00'
    else:
        dot = value.find('.')
        scrap = value[dot + 1:dot + 3]
        scrap = int(scrap)
        if 0 < scrap < 6 or scrap == 0:
            scrap = '00'
        elif 6 < scrap < 17:
            scrap = '11'
        elif 17 < scrap < 28:
            scrap = '22'
        elif 28 < scrap < 39:
            scrap = '33'
        elif 39 < scrap < 50:
            scrap = '44'
        elif 50 < scrap < 61:
            scrap = '55'
        elif 61 < scrap < 72:
            scrap = '66'
        elif 72 < scrap < 83:
            scrap = '77'
        elif 83 < scrap < 94:
            scrap = '88'
        elif 94 < scrap:
            scrap = '00'
            value += 1
        value = value[0:dot + 1] + scrap
    return value


def get_webpage(url):
    # print('Searching:', url)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    page = page.decode('UTF-8', errors='ignore')
    return page


def get_key_price():
    link = 'https://backpack.tf/classifieds?item=Mann+Co.+Supply+Crate+Key&quality=6&tradable=1&craftable=1\
&australium=-1&killstreak_tier=0'
    buy_listing = -25
    buy_array = []
    sell_listing = -25
    sell_array = []
    lowsell = 0
    maxbuy = 0

    webpage = get_webpage(link)

    for i in range(5):
        sell_listing = webpage.find("data-listing_intent=\"sell\"", sell_listing + 25)
        price_sell = webpage.find('data-listing_price', sell_listing)
        sell_ref = webpage.find('ref', price_sell)
        price_tag = webpage[sell_ref - 6: sell_ref]
        price_sell = ''
        for j in price_tag:
            if j in '1234567890.':
                price_sell += j
        sell_array.append(float(price_sell))
        if i == 0:
            lowsell = price_sell

    for i in range(5):
        buy_listing = webpage.find("data-listing_intent=\"buy\"", buy_listing + 25)
        price_buy = webpage.find('data-listing_price', buy_listing)
        buy_ref = webpage.find('ref', price_buy)
        price_tag = webpage[buy_ref - 6: buy_ref]
        price_buy = ''
        for j in price_tag:
            if j in '1234567890.':
                price_buy += j
        buy_array.append(float(price_buy))
        if i == 0:
            maxbuy = price_buy

    csp = round_to_ref(sum(sell_array) / len(sell_array))
    cbp = round_to_ref(sum(buy_array) / len(buy_array))
    key_price = value_to_items(csp)

    return [key_price, csp, lowsell, cbp, maxbuy]


def main():
    print('This is the key bot trading with Mann Co. Supply Crate Keys.')
    client = SteamClient(api_key)
    client.login(username, password, steamguard_path)
    print('Bot logged in successfully, fetching offers every 30 seconds')
    while True:
        offers = client.get_trade_offers()['response']['trade_offers_received']
        for offer in offers:
            trade_id = offer.get('tradeofferid')
            if offer.get('accountid_other') == 350539137:
                client.accept_trade_offer(trade_id)
                print('Trade offer from owner accepted!')
            if is_buy(offer):
                client.accept_trade_offer(trade_id)
                print('Trade offer to buy keys accepted!')
                continue
            else:
                client.decline_trade_offer(trade_id)
                continue
            if is_sell(offer):
                client.accept_trade_offer(trade_id)
                print('Trade offer to sell keys accepted!')
                continue
            else:
                client.decline_trade_offer(trade_id)
                continue
        time.sleep(30)


def is_buy(offer: dict) -> bool:
    item_check = []
    items_to_give = []
    for i in offer['items_to_receive']:
        if offer.get('items_to_receive', {}).get(i, {}).get('name') == 'Mann Co. Supply Crate Key':
            item_check.append(1)
        else:
            item_check.append(0)
    if sum(item_check) == len(item_check):
        for j in offer['items_to_give']:
            item = offer.get('items_to_give', {}).get(j, {}).get('name')
            if item not in 'Scrap Metal, Reclaimed Metal, Refined Metal':
                return False
            else:
                items_to_give.append(item)
        if items_to_give == value_to_items(get_key_price()[2]) or items_to_give <= value_to_items(48):
            return True
        else:
            return False
    else:
        return False


def is_sell(offer: dict) -> bool:
    item_check = []
    items_to_get = []
    for i in offer['items_to_give']:
        if offer.get('items_to_give', {}).get(i, {}).get('name') == 'Mann Co. Supply Crate Key':
            item_check.append(1)
        else:
            item_check.append(0)
    if sum(item_check) == len(item_check):
        for j in offer['items_to_receive']:
            item = offer.get('items_to_receive', {}).get(j, {}).get('name')
            if item not in 'Scrap Metal, Reclaimed Metal, Refined Metal':
                return False
            else:
                items_to_get.append(item)
        if items_to_get == value_to_items(get_key_price()[2]) or items_to_get >= value_to_items(48.11):
            return True
        else:
            return False
    else:
        return False


if __name__ == "__main__":
    # execute only if run as a script
    main()
