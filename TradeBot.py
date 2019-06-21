import time
from steampy.client import SteamClient
from steampy.models import GameOptions
from modules.TradeCheck import is_buy, is_sell
from modules.PriceCheck import get_key_price
import pytf2

# Important variables
api_key = ''
steamguard_path = ''
username = ''
password = ''
owner_id = ''
bp_api_key = ''
bp_user_token = ''

pytf2 = pytf2.Manager(bp_api_key=bp_api_key, bp_user_token=bp_user_token)


def main():
    print('This is the key bot trading with Mann Co. Supply Crate Keys.')
    client = SteamClient(api_key)
    client.login(username, password, steamguard_path)
    print('Bot logged in successfully, fetching offers every 30 seconds')
    while True:
        offers = client.get_trade_offers()['response']['trade_offers_received']
        for offer in offers:
            trade_id = offer.get('tradeofferid')
            if offer.get('accountid_other') == owner_id:
                client.accept_trade_offer(trade_id)
                print('Trade offer from owner accepted!')
            elif not pytf2.bp_can_trade(steamid=offer.get('accountid_other')):
                client.decline_trade_offer(trade_id)
                print('User is not allowed to trade!')
            elif is_buy(offer):
                client.accept_trade_offer(trade_id)
                print('Trade offer to buy keys accepted!')
                # Post bp.tf sell listing
                price = {"metal": get_key_price()[1], "keys": 0}
                item_id = 0
                data = pytf2.bp_create_listing_create_data(intent=1, currencies=price, item_or_id=item_id, details=' \
                I am selling Mann Co. Keys for ' + str(price.get('metal')) + 'refined! This is an \
                automatic trading bot.')
                pytf2.bp_create_listing(data)
                continue
            elif is_sell(offer):
                client.accept_trade_offer(trade_id)
                print('Trade offer to sell keys accepted!')
                # Post bp.tf buy order
                price = {"metal": get_key_price()[1], "keys": 0}
                item = 'Mann Co. Supply Crate Key'
                data = pytf2.bp_create_listing_create_data(intent=0, currencies=price, item_or_id=item, details=' \
                I am buying Mann Co. Keys for ' + str(price.get('metal')) + ' refined! This is an \
                automatic trading bot.')
                pytf2.bp_create_listing(data)
                continue
            else:
                client.decline_trade_offer(trade_id)
                continue
        inventory = client.get_my_inventory(game=GameOptions('440', '2'))
        print(inventory)
        for item in inventory:
            print(item)
            if inventory.get(str(item)).get('name') == 'Mann Co. Supply Crate Key':
                price = {"metal": float(get_key_price()[1]) + 1}
                data = pytf2.bp_create_listing_create_data(1, price, str(item), details='\
I am selling Mann Co. Keys for ' + str(price.get('metal')) + ' refined! This is an \
automatic trading bot.')
                print(data)
                listing = pytf2.bp_create_listing(listings=[data], parse=True)
                print(listing)
        time.sleep(30)
        bp_heartbeat()


def bp_heartbeat():
    current_minute = time.strftime("%M", time.gmtime())
    if str(current_minute) in ['0', '15', '30', '45']:
        print('Bumping listings...')
        bump = pytf2.bp_send_heartbeat(automatic='all')
        print('Bumped ' + str(bump) + ' listing(s).')


if __name__ == "__main__":
    # execute only if run as a script
    main()
