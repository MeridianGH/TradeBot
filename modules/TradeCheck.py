from modules.PriceCheck import *
from modules.Tools import *


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
        if items_to_value(items_to_give) <= get_key_price()[3] or items_to_value(items_to_give) <= 52.88:
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
        if items_to_value(items_to_get) >= get_key_price()[1] or items_to_value(items_to_get) >= 53:
            return True
        else:
            return False
    else:
        return False


def is_item_buy(offer: dict) -> bool:
    total_value = 0
    for item in offer['items_to_receive']:
        total_value += price_check(item)[0]
        if total_value >= items_to_value(offer['items_to_give']):
            return True
        else:
            return False


def is_item_sell(offer: dict) -> bool:
    total_value = 0
    for item in offer['items_to_give']:
        total_value += price_check(item)[0] + 0.11
        if total_value <= items_to_value(offer['items_to_receive']):
            return True
        else:
            return False
