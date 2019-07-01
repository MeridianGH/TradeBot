from modules.PriceCheck import get_key_price
from steampy.models import GameOptions


def bp_listing_manager(client, pytf2, stock):
    bp_listings(client, pytf2, stock)
    bp_heartbeat(pytf2)


def bp_heartbeat(pytf2):
    bump = pytf2.bp_send_heartbeat(automatic='all')
    print('Bumped ' + str(bump) + ' listing(s).')


def bp_listings(client, pytf2, stock):
    key_count = 0
    item = 0
    inventory = client.get_my_inventory(game=GameOptions('440', '2'))
    for item in inventory:
        if inventory.get(str(item)).get('name') == 'Mann Co. Supply Crate Key':
            key_count += 1
            item = str(item)

    if 0 < key_count < stock:
        price = {"metal": float(get_key_price()[1])}
        details = 'I am selling Mann Co. Keys for ' + str(price.get('metal')) + ' refined! My current stock is ' \
                  + str(key_count) + ' out of ' + str(stock) + '. This is an automatic trading bot.'
        data = pytf2.bp_create_listing_create_data(1, price, str(item), offers=1, details=details)
        response = pytf2.bp_create_listing(listings=[data], parse=True)
        print(response)
        price = {"metal": float(get_key_price()[3])}
        details = 'I am buying Mann Co. Keys for ' + str(price.get('metal')) + ' refined! My current stock is ' \
                  + str(key_count) + ' out of ' + str(stock) + '. This is an automatic trading bot.'
        data = pytf2.bp_create_listing_create_data(0, price, 'Mann Co. Supply Crate Key', offers=1, details=details)
        response = pytf2.bp_create_listing(listings=[data], parse=True)
        print(response)

    elif key_count == 0:
        listings = pytf2.bp_my_listings(parse=False).get('listings')
        for listing in listings:
            if listing.get('intent') == 1:
                pytf2.bp_delete_listing(listing.get('id'))
            elif listing.get('intent') == 0:
                return
        price = {"metal": float(get_key_price()[3])}
        details = 'I am buying Mann Co. Keys for ' + str(price.get('metal')) + ' refined! My current stock is ' \
                  + str(key_count) + ' out of ' + str(stock) + '. This is an automatic trading bot.'
        data = pytf2.bp_create_listing_create_data(0, price, 'Mann Co. Supply Crate Key', offers=1, details=details)
        response = pytf2.bp_create_listing(listings=[data], parse=True)
        print(response)

    elif key_count >= stock:
        listings = pytf2.bp_my_listings(parse=False).get('listings')
        for listing in listings:
            if listing.get('intent') == 0:
                pytf2.bp_delete_listing(listing.get('id'))
            elif listing.get('intent') == 1:
                return
        price = {"metal": float(get_key_price()[1])}
        details = 'I am selling Mann Co. Keys for ' + str(price.get('metal')) + ' refined! My current stock is ' \
                  + str(key_count) + ' out of ' + str(stock) + '. This is an automatic trading bot.'
        data = pytf2.bp_create_listing_create_data(1, price, str(item), offers=1, details=details)
        response = pytf2.bp_create_listing(listings=[data], parse=True)
        print(response)
