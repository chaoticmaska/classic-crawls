import argparse
from utils.partialsDataTBC import mapCrawlArgs, availableEncounters, mapRaidZone
from utils.querys import getReportSet, reportEnemiesQuery, reportDebuffsQuery, reportCastAndDamageQuery

parser = argparse.ArgumentParser(description='Calculates estimated resist for given magic school and boss')
parser.add_argument(
    "--school",
    type=str,
    help="Verbose name of spell school, e.g Fire",
    choices=['Fire', 'Shadow', 'Arcane'],
    required=True
)
parser.add_argument(
    "--target",
    type=str,
    help="Target name. Available values: {}".format(availableEncounters),
    nargs='+',
    required=True
)
parser.add_argument(
    "--limit",
    type=int,
    default=1,
    help="Page limit for crawl, each page is 100 reports",
)


class CurseEvent:
    def __init__(self, sTime: int, eTime: int):
        self.sTime = sTime
        self.eTime = eTime

    def getValue(self, time: int):
        isTimed = self.sTime <= time <= self.eTime
        return isTimed


class DebuffEvent:
    def __init__(self, sTime: int, eTime: int, mod: float):
        self.sTime = sTime
        self.eTime = eTime
        self.mod = mod

    def getValue(self, time: int, damage: float):
        isTimed = self.sTime <= time <= self.eTime
        return damage * self.mod if isTimed else damage


class DamageEvent:
    # We need both castFinish and damageDone for calculations, since debuffs are calculated at cast finish
    # Fully resisted hits are filtered at report class
    def __init__(
            self,
            castFinish: int,
            hitType: int,
            unmitigatedAmount: int,
            amount: int
    ):
        self.tCast = castFinish
        # Account for crit modifier or make u=1 if hitType is unknown (will lead to excluding given event)
        self.u = unmitigatedAmount * encounterData.get('hitTypes').get(hitType, 0) or 1
        self.a = amount  # Used in calculations as final damage landed

    def __str__(self):  # For development
        return 'Cast finish: {}, U: {}, A: {}'.format(self.tCast, self.u, self.a)


class Report:
    def __init__(self, url: str):
        self.url = url
        self.e = encounterData.get('encounterData')
        self.enemyID = self.e.get('bossID')
        self.curses, self.mods = self.getUptime()
        self.damageEvents = self.getDamageAndCasts()

    def getEnemyID(self):
        response = reportEnemiesQuery(self.url) \
            .get('reportData', {}).get('report', {}).get('masterData', {}).get('actors', [])
        bossActors = list(filter(lambda actor: actor.get('gameID') == self.e.get('bossID'), response))
        if bossActors:
            return bossActors[0].get('id')
        else:
            return 0

    def getUptime(self):
        # Get uptime for curse and all damage modifiers
        response = reportDebuffsQuery(
            url=self.url,
            bossID=self.enemyID,
            curse=encounterData.get('curseID'),
            modifiers=encounterData.get('damageModifiers')
        ).get('reportData', {}).get('report', {})

        # Separate objects for curse (to split data later) and damage modifiers
        # Curse uses table request, while modifiers uses events request
        curses = response.get('curse', {}).get('data', {}).get('auras', {})
        curseList = []
        if curses:
            for curse in curses[0].get('bands'):
                curseList.append(
                    CurseEvent(
                        curse.get('startTime'),
                        curse.get('endTime')
                    )
                )

        modList = []
        for mod in encounterData.get('damageModifiers'):
            name = mod.get('name')
            data = response.get(name, {}).get('data', [])
            if not data:
                continue
            stackCount = 0
            startingTiming = 0
            lastEvent = ''
            for event in data:
                # + 1 millisecond is workaround for scorch, since it does not use modifier from stack applied by itself
                if event.get('type') == 'applydebuff':
                    if lastEvent == 'applydebuff':
                        continue
                    startingTiming = event.get('timestamp') + 1
                    stackCount = 1
                if event.get('type') == 'applydebuffstack':
                    modList.append(
                        DebuffEvent(
                            startingTiming,
                            event.get('timestamp'),
                            1 + stackCount * mod.get('mod')
                        )
                    )
                    startingTiming = event.get('timestamp') + 1
                    stackCount += 1
                if event.get('type') == 'removedebuff':
                    modList.append(
                        DebuffEvent(
                            startingTiming,
                            event.get('timestamp'),
                            1 + stackCount * mod.get('mod')
                        )
                    )
                    stackCount = 0
                lastEvent = event.get('type')
        return [curseList, modList]

    def getDamageAndCasts(self):
        response = reportCastAndDamageQuery(
            self.url,
            self.enemyID,
            encounterData.get('spellIDs')
        ).get('reportData', {}).get('report', {})
        casts = response.get('casts', {}).get('data', [])
        damage = response.get('damage', {}).get('data', [])
        damageEvents = []
        for event in casts:
            try:  # Find corresponding damage event
                cEvent = next(
                    filter(
                        lambda e: e.get('timestamp') >= event.get('timestamp') and
                                  e.get('sourceID') == event.get('sourceID') and
                                  e.get('abilityGameID') == event.get('abilityGameID') and
                                  (e.get('timestamp') - event.get('timestamp')) < 4000,
                        damage
                    )
                )
                if cEvent.get('hitType') == 14:  # Skip resists as we don't need them in partials calculation
                    continue
                damageEvent = DamageEvent(
                    event.get('timestamp'),
                    cEvent.get('hitType'),
                    cEvent.get('unmitigatedAmount', 1),
                    cEvent.get('amount')
                )
                damageEvents.append(damageEvent)
            except StopIteration:  # Ability did not land
                continue
        print('==================================')
        print(self.url)
        print('==================================')
        return damageEvents

    def checkIfCurseIsUp(self, damageEvent):
        for curse in self.curses:
            if curse.getValue(damageEvent.tCast):
                return True
        return False

    @staticmethod
    def mapPartialValue(damage):
        # Returns index for partials count list or -1 if value does not correspond to any partial
        if 12 < damage < 37:
            return 0
        if 38 < damage < 62:
            return 1
        if 63 < damage < 87:
            return 2
        if 88 < damage < 112:
            return 3
        return -1

    def returnPartialsTable(self):
        table = [
            [0, 0, 0, 0],  # Events without curse, 25/50/75/100% damage done
            [0, 0, 0, 0]  # Events with curse, 25/50/75/100% damage done
        ]
        for event in self.damageEvents:
            damage = event.u
            withCurse = self.checkIfCurseIsUp(event)
            if withCurse:
                damage *= 1.1
            for mod in self.mods:
                damage = mod.getValue(event.tCast, damage)
            # Curse and every damage modifier were accounted, now we can check if hit was partial
            partial = self.mapPartialValue(event.a * 100 / damage)
            partialToPrint = ''
            if partial == 0:
                partialToPrint = 25
            if partial == 1:
                partialToPrint = 50
            if partial == 2:
                partialToPrint = 75
            if partial == 3:
                partialToPrint = 100
            if partial == -1:
                partialToPrint = 'Error'

            print('DAMAGE EVENT ===================================')
            if partialToPrint == 'Error':
                print(event.tCast)
            print(
                f'Partial: {partialToPrint}% ||| Calculated damage: {damage} ||| Real damage: {event.a} ||| Unmitigated: {event.u}')

            if partial > -1:
                table[int(withCurse)][partial] += 1
        return table


def calcMitigation(values: list):
    damageWeighted = 0.25 * values[0] + 0.5 * values[1] + .75 * values[2] + values[3]
    damageTotal = sum(values) or 1
    mitigation = damageWeighted / damageTotal
    return str(round(315 * (1 - mitigation) * 100 / 75, 1))


def run():  # Get reports, gather data and write it down
    result = [
        [0, 0, 0, 0],  # Events without curse, 25/50/75/100% damage done
        [0, 0, 0, 0]  # Events with curse, 25/50/75/100% damage done
    ]
    reportSet = getReportSet(encounterData.get('zone'), l)
    reportCount = len(reportSet)
    processedCount = 0
    encounterName = encounterData.get('encounterData').get('name')
    zoneNumber = encounterData.get('zone')
    for url in reportSet:
        report = Report(url)
        data = report.returnPartialsTable()
        for curseType in range(2):
            for partialType in range(4):
                result[curseType][partialType] += data[curseType][partialType]
        processedCount += 1
        print(
            '{} out of {} reports are done for {}'.format(
                processedCount,
                reportCount,
                encounterName
            )
        )
        if processedCount % 10 == 0 or processedCount == len(reportSet):
            # Rewrite crawl results sometimes to backup in case of crash or error
            fileName = '{}-{}-{}.txt'.format(zoneNumber, encounterName, s)
            f = open(fileName, 'w')
            f.write(f'# {encounterName}\n')
            f.write('### No curse: {}\n'.format(calcMitigation(result[0])))
            f.write('### With curse: {}\n\n'.format(calcMitigation(result[1])))
            f.write('##### Dataset (number of casts by % of damage done):\n')
            f.write('No curse: 25% - {} | 50% - {} | 75% - {} | 100% - {}\\\n'.format(
                result[0][0],
                result[0][1],
                result[0][2],
                result[0][3]
            ))
            f.write('With curse: 25% - {} | 50% - {} | 75% - {} | 100% - {}\n'.format(
                result[1][0],
                result[1][1],
                result[1][2],
                result[1][3]
            ))
            f.close()


if __name__ == '__main__':  # General stuff like parse args and run crawls for selected zones
    args = parser.parse_args()
    s = args.school
    z = args.target
    l = args.limit
    for zone in z:
        if zone == 'Kara':
            for encounter in mapRaidZone(1007):
                encounterData = mapCrawlArgs(s, encounter.get('name'))
                run()
        else:
            encounterData = mapCrawlArgs(s, zone)
            run()
