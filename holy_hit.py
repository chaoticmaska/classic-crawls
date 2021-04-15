from utils.querys import getReportSet, reportGearQuerySmite, reportDamageQuerySmite
import json

playerSubTypes = ('Priest')


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
            for jsonItem in jsonItems:
                if jsonItem['id'] == itemID:
                    if 'spellHit' in jsonItem:
                        hitValue += jsonItem['spellHit']
        if hitValue > 99:
            hitValue = 99
        return hitValue

    def __str__(self):
        return f'{self.spec}-{self.hit}'


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

reports = getReportSet(zone=1005, pages=50)

counter = 0
for report in reports:
    print(counter)
    damage = reportDamageQuerySmite(report).get('reportData', {}).get('report', {}).get('events', {}).get('data', [])
    if not damage:
        continue
    response = reportGearQuerySmite(report)
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
    for event in damage:
        source = event.get('sourceID')
        hitType = event.get('hitType')
        actor = list(filter(lambda a: a.id == source, actors))

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
