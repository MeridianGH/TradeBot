from urllib.request import Request, urlopen


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


def items_to_value(items):
    value = 0
    for item in items:
        if item == 'Scrap Metal':
            value += 0.11
        elif item == 'Reclaimed Metal':
            value += 0.33
        elif item == 'Refined Metal':
            value += 1.0
        else:
            return False
    return round_to_ref(value)


def round_to_ref(value):
    value = str(round(value, 2))
    if '.' not in value:
        value = value + '.00'
        trigger = False
        dot = 2
        scrap = 0
    elif len(value) == 4:
        dot = value.find('.')
        scrap = value[dot + 1:dot + 2]
        scrap = int(scrap)
        trigger = True
    else:
        dot = value.find('.')
        scrap = value[dot + 1:dot + 3]
        scrap = int(scrap)
        trigger = True
    if trigger:
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
            value = str(int(value) + 1)
        value = value[0:dot + 1] + str(scrap)
    return value


def get_webpage(url):
    # print('Searching:', url)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    page = page.decode('UTF-8', errors='ignore')
    return page
