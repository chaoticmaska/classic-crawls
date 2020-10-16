from utils.querys import reportListQuery, reportGearQueryWands, reportDamageQueryWands
import json

playerSubTypes = ('Mage')


def writeToFile(data):
    f = open('oldChromLogs.txt', 'w')
    f.write(json.dumps(data))
    f.close()


# Bunch of pepega code to find starting page for p4 BWL logs
'''
timeThreshold = 1596412800000
zone = 1002

digDeeper = True
page = 1
while digDeeper:
    print(page)
    response = reportListQuery(zone, page).get('reportData', {}).get('reports', {}).get('data', [])
    report = response[0]
    if report.get('endTime') < timeThreshold:
        print(report)
        digDeeper = False
    else:
        print(report.get('endTime'), timeThreshold)
        page += 500

reportList = set()
for page in range(3000, 3020):
    response = reportListQuery(1002, page).get('reportData', {}).get('reports', {}).get('data', [])
    reportList.update([report.get('code') for report in response])
    print(response[0].get('endTime'), str(1596412800000))
reportList = list(reportList)
writeToFile(reportList)
'''
enchantData = {
    2588: 1,  # Mage ZG enchant
}


class FriendlyActor:
    def __init__(self, actor: dict):
        self.id = actor.get('id')
        self.spec = actor.get('subType')
        self.gear = actor.get('gear')
        self.hit = self.getGearValues()

    def getGearValues(self):
        hitValue = 83  # Hit from talents
        for item in self.gear:
            itemID = item.get('id')
            hitValue += enchantData.get(item.get('permanentEnchant'), 0)
            for jsonItem in jsonItems:
                if jsonItem['id'] == itemID:
                    if 'spellHit' in jsonItem:
                        hitValue += jsonItem['spellHit']
        if hitValue > 99:
            hitValue = 99
        return hitValue

    def __str__(self):
        return f'{self.spec}-{self.hit}'


reports = json.load(open('oldChromLogs.txt', 'r'))
with open('utils/item.json') as itemFile:
    jsonItems = json.load(itemFile)

table = {
    83: {
        'hit': 0,
        'total': 0
    },
    84: {
        'hit': 0,
        'total': 0
    },
    85: {
        'hit': 0,
        'total': 0
    },
    86: {
        'hit': 0,
        'total': 0
    },
    87: {
        'hit': 0,
        'total': 0
    },
    88: {
        'hit': 0,
        'total': 0
    },
    89: {
        'hit': 0,
        'total': 0
    },
    90: {
        'hit': 0,
        'total': 0
    },
    91: {
        'hit': 0,
        'total': 0
    },
    92: {
        'hit': 0,
        'total': 0
    },
    93: {
        'hit': 0,
        'total': 0
    },
    94: {
        'hit': 0,
        'total': 0
    },
    95: {
        'hit': 0,
        'total': 0
    },
    96: {
        'hit': 0,
        'total': 0
    },
    97: {
        'hit': 0,
        'total': 0
    },
    98: {
        'hit': 0,
        'total': 0
    },
    99: {
        'hit': 0,
        'total': 0
    }
}

counter = 0
for report in reports:
    response = reportGearQueryWands(report)
    gearResponse = response.get('reportData', {}).get('report', {}).get('events', {}).get('data', [])
    playerResponse = response.get('reportData', {}).get('report', {}).get('masterData', {}).get('actors', [])
    playerResponse = list(filter(lambda player: player.get('subType') in playerSubTypes, playerResponse))
    if not gearResponse or not playerResponse:
        continue

    actors = []
    for player in playerResponse:
        try:
            gear = next(filter(lambda event: event.get('sourceID') == player.get('id'), gearResponse))
            p = FriendlyActor({
                'id': player.get('id'),
                'subType': player.get('subType'),
                'gear': gear.get('gear')
            })
            actors.append(p)
        except:
            continue
    response = reportDamageQueryWands(report).get('reportData', {}).get('report', {}).get('events', {}).get('data', [])
    if not response:
        continue
    for event in response:
        source = event.get('sourceID')
        hitType = event.get('hitType')
        actor = list(filter(lambda p: p.id == source, actors))
        if not actor:
            continue
        actor = actor[0]

        # Hit
        if hitType in (1, 2, 16, 17):
            table[actor.hit]['hit'] += 1
            table[actor.hit]['total'] += 1
        # Resist
        elif hitType == 14:
            table[actor.hit]['total'] += 1
    counter += 1
    if counter % 10 == 0:
        print('###############', counter)
        for key in range(83, 100):
            data = table[key]
            if data['total'] > 0:
                actual = round(data['hit'] * 100 / data['total'], 1)
                print(f'Expected: {key} | Actual: {actual} | Sample: {data["total"]}')
