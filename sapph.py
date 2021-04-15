from utils.querys import getReportSet, obsidianTable

reportSet = getReportSet(1006, 2)
counter = 1
'''
events = []
partials = {
    25: 0,
    50: 0,
    75: 0,
    100: 0
}
for report in reportSet:
    print(counter, 'out of', len(reportSet))
    startTime = 1
    while startTime:
        print(startTime)
        response = sapphDmgTaken(report, startTime).get('reportData', {}).get('report', {}).get('events', {})
        data = response.get('data')
        events.extend(data)
        startTime = response.get('nextPageTimestamp', 0)
        if len(events) > 60000:
            break
    if len(events) > 60000:
        break
    counter += 1

fullRes = 0
total = 0
for event in events:
    u = event.get('unmitigatedAmount', 0)
    r = event.get('resisted', 0)
    m = event.get('mitigated', 0)
    t = event.get('hitType', 0)
    absorb = event.get('absorbed', 0)
    amount = event.get('amount', 0)
    r = absorb + amount
    if t == 14:
        fullRes += 1
        continue

    if u == 0:
        continue

    if 0 < r < 210:
        total += 1
        partials[75] += 1
    elif 210 <= r <= 390:
        total += 1
        partials[50] += 1
    elif 400 <= r < 560:
        total += 1
        partials[25] += 1
    elif r == 0:
        total += 1
        partials[100] += 1

weight = partials[100] + partials[75] * 0.75 + partials[50] * 0.5 + partials[25] * 0.25
print(weight * 100 * 4.2 / total)
print(weight, total)
print(fullRes, 'out of', len(events))
'''

for report in reportSet:
    response = obsidianTable(report).get('reportData', {}).get('report', {}).get('table', {}).get('data', {})
    for actor in response.get('entries', []):
        gear = actor.get('gear', [])
        if len(list(filter(lambda item: item.get('id') == 22196, gear))):
            print(f'https://classic.warcraftlogs.com/reports/{report}', actor.get('name'))