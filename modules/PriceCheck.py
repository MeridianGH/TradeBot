import urllib.parse
from modules.Tools import *


def price_check(item_name):
    quality = '6'     # Standard: Unique
    killstreak = '0'  # Standard: None

    if 'Strange' in item_name:
        item_name = item_name[8:]
        quality = '11'

    if 'Genuine' in item_name:
        item_name = item_name[8:]
        quality = '1'

    if 'Vintage' in item_name:
        item_name = item_name[8:]
        quality = '3'

    # TODO: Add other qualities and options

    item_name = urllib.parse.quote(item_name)

    page = 1
    link = 'https://backpack.tf/classifieds?craftable=1&quality=' + quality + '&killstreak_tier=' + killstreak + \
           '&item=' + item_name + '&page=' + str(page)

    webpage = get_webpage(link)

    buy_listing = -25
    found_data = False

    while not found_data:
        for i in range(10):
            buy_listing = webpage.find("data-listing_intent=\"buy\"", buy_listing + 25)
            # print(buy_listing)
            paint_name = webpage.find('data-paint_name', buy_listing, buy_listing + 1000)
            # print(paint_name)
            if paint_name < 0 < buy_listing:
                found_data = True
                break
        if not found_data:
            page += 1
            link = list(link)
            link[-1] = str(page)
            link = ''.join(link)
            webpage = get_webpage(link)

    value_arr = []
    highest_listing = 0

    for i in range(5):
        tag = webpage.find('data-listing_price', buy_listing)
        ref_tag = webpage.find('ref', tag)
        price_tag = webpage[ref_tag - 6: ref_tag]
        price = ''
        for j in price_tag:
            if j in '1234567890.':
                price += j
        if i == 0:
            highest_listing = price
        if price == '':
            print('Error')
        else:
            value_arr.append(float(price))
        buy_listing = webpage.find("data-listing_intent=\"buy\"", buy_listing + 25)
        if buy_listing == -1:
            break
        if '</html>' in webpage[buy_listing:buy_listing + 12800]:
            page += 1
            link = list(link)
            link[-1] = str(page)
            link = ''.join(link)
            get_webpage(link)
            buy_listing = webpage.find("data-listing_intent=\"buy\"", buy_listing + 25)

    csp = sum(value_arr) / len(value_arr)

    return [csp, highest_listing]


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
    search_item = input('Item: ')
    result = price_check(search_item)
    print('Median price: ', result[0])
    print('CSP: ', round_to_ref(result[0]))
    print('Highest listing: ', result[1])
    print(get_key_price())
