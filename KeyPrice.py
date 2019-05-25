from urllib.request import Request, urlopen


def value_to_items(value):
    items = []
    for i in range(int(float(value))):
        items.append('refined')
    scrap = str(value)[-2:]
    if scrap == '.0':
        return items
    else:
        if scrap == '11':
            items.append('scrap')
        if scrap == '22':
            items.extend(('scrap', 'scrap'))
        if scrap == '33':
            items.append('reclaimed')
        if scrap == '44':
            items.extend(('reclaimed', 'scrap'))
        if scrap == '55':
            items.extend(('reclaimed', 'scrap', 'scrap'))
        if scrap == '66':
            items.extend(('reclaimed', 'reclaimed'))
        if scrap == '77':
            items.extend(('reclaimed', 'reclaimed', 'scrap'))
        if scrap == '88':
            items.extend(('reclaimed', 'reclaimed', 'scrap', 'scrap'))
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


if __name__ == "__main__":
    # execute only if run as a script
    print('', get_key_price()[1:5], '\n', [' CSP ', ' Sell', ' CBP ', ' Buy '])
