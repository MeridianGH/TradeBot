import urllib.request, urllib.parse
import json


def price_check(item_name):
    quality = '6'
    if 'Strange' in item_name:
        item_name = item_name[8:]
        quality = '11'

    # TODO: Add other qualities
    item_name = urllib.parse.quote(item_name)
    link = 'https://backpack.tf/classifieds?quality=' + quality + '&item=' + item_name
    print('Searching:', link)

    url = urllib.request.urlopen(link)
    data = json.loads(url.read())
    data = json.dumps(data)

    buy_listing = data.find('\"intent\": 0', 0)
    # print('Got first buy listing at: ', buy_listing)


# Ignoring Painted Offers
    while True:
        for i in range(15):
            if 'data-paint_name' in data[buy_listing:]:
                buy_listing = data.find("data-listing_intent=\"buy\"", buy_listing + 25)
                print('Paint iteration')
            elif 'data-paint_name' not in data[buy_listing:]:
                found_data = True
                print('Found data')
                break
        if not found_data:
            link = 'https://backpack.tf/classifieds?item=' + item_name.replace(' ', '+') + \
                   '&quality=6&tradable=1&craftable=1'
        if strange:
            link = 'https://backpack.tf/classifieds?item=' + item_name.replace(' ','+') + \
                   '&quality=11&tradable=1&craftable=1'
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        data = urlopen(req).read()
        data = data.decode('UTF-8', errors='ignore')
        if found_data:
            break

    tag = data.find('fa fa-tag', buy_listing)
    print('Got price tag at: ', tag)
    ref_tag = data.find('ref', tag)
    print('Got ref at: ', ref_tag)

    price_tag = data[ref_tag - 6: ref_tag]
    print('Got raw price: ', price_tag)
    price = ''

    for i in price_tag:
        if i in '1234567890.':
            price += i

    # price += ' ref'
    # print(price)
    return price


if __name__ == "__main__":
    # execute only if run as a script
    item_name = input('Item: ')
    price = price_check(item_name)
    print(price)
