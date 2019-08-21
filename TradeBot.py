from steampy.client import SteamClient
from modules.TradeCheck import is_buy, is_sell
from modules.bptf import *
from apscheduler.schedulers.blocking import BlockingScheduler
import pytf2
from datetime import datetime as time

# Credentials
credentials = open('credentials.txt', 'r')
lines = credentials.readlines()
credentials.close()
api_key = lines[1][:-1]
steamguard_path = lines[2][:-1]
username = lines[3][:-1]
password = lines[4][:-1]
owner_id = lines[5][:-1]
bp_api_key = lines[6][:-1]
bp_user_token = lines[7][:-1]

# Setting up APIs
pytf2 = pytf2.Manager(bp_api_key=bp_api_key, bp_user_token=bp_user_token)
client = SteamClient(api_key)
client.login(username, password, steamguard_path)
print('Bot logged in successfully.')

# Price and Stock
stock = 1
price = get_key_price(pytf2)


def main():
    offers = client.get_trade_offers()['response']['trade_offers_received']
    for offer in offers:
        trade_id = offer.get('tradeofferid')
        if offer.get('accountid_other') == int(owner_id):
            client.accept_trade_offer(trade_id)
            print('Trade offer from owner accepted!')
        elif not pytf2.bp_can_trade(steamid=offer.get('accountid_other')):
            client.decline_trade_offer(trade_id)
            print('User is not allowed to trade!')
        elif is_buy(offer):
            client.accept_trade_offer(trade_id)
            print('Trade offer to buy keys accepted!')
            continue
        elif is_sell(offer):
            client.accept_trade_offer(trade_id)
            print('Trade offer to sell keys accepted!')
            continue
        else:
            client.decline_trade_offer(trade_id)
            continue


scheduler = BlockingScheduler()
scheduler.add_job(main, 'interval', seconds=30, next_run_time=time.now())
scheduler.add_job(bp_listing_manager, 'cron', minute='*/15', args=(client, pytf2, stock, price), next_run_time=time.now())

if __name__ == "__main__":
    # execute only if run as a script
    scheduler.start()
    print(price)
