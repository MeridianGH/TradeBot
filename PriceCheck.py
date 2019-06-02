from urllib.request import Request, urlopen
import urllib.parse


def round_to_ref(value):
    value = round(value, 2)
    scrap = str(value)[-2:]
    if scrap == '.0':
        scrap = '.00'
    elif '.' not in str(value):
        scrap = '.00'
    else:
        scrap = int(scrap)

        if 0 < scrap < 6:
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

    value = str(value)[0:-2] + scrap

    return value


def get_webpage(link):
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    webpage = webpage.decode('UTF-8', errors='ignore')
    print('Searching:', link)
    return webpage


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


if __name__ == "__main__":
    # execute only if run as a script
    item = input('Item: ')
    result = price_check(item)
    print('Median price: ', result[0])
    print('CSP: ', round_to_ref(result[0]))
    print('Highest listing: ', result[1])
