import requests
import time
from variables import wcl_token as token
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
apiUrl = 'https://classic.warcraftlogs.com/api/v2'
bearer = "Bearer " + token
headers = {"Authorization": bearer}


def fetchGraphQL(query):
    try:
        response = requests.post(apiUrl, json={'query': query}, headers=headers).json()
        if not response or response.get('errors'):
            return {}
        else:
            return response.get('data')
    except Exception as e:
        print(e)
        print('Sleeping', datetime.now())
        time.sleep(60)
        fetchGraphQL(query)


#######################
##### Basic stuff #####
def reportListQuery(zone: int, page: int, limit: int = 100) -> dict:
    query = '''
    {{
        reportData {{
            reports(
                zoneID: {zone}
                limit: {limit}
                page: {page}
            ) {{
                data {{
                    code
                    visibility
                    endTime
                }}
                from
                to
            }}
        }}
    }}
    '''.format(
        zone=str(zone),
        limit=str(limit),
        page=str(page)
    )
    return fetchGraphQL(query)


def getReportSet(zone: int, pages: int, limit: int = 100):  # Basic report url's set for selected zone
    reportSet = set()
    for page in range(1, pages + 1):
        data = reportListQuery(zone, page, limit)
        reportSet.update(
            [report.get('code') for report in data.get('reportData', {}).get('reports', {}).get('data', [])]
        )
    return reportSet


#####################
##### Twin Emps #####
def twinEmpEvents(url: str) -> dict:
    query = '''
    {{
        reportData {{
            report(code: "{url}") {{
                events(
                    dataType: Buffs
                    startTime: 0
                    endTime: 99999999999
                    hostilityType: Enemies
                    abilityID: 800
                ) {{
                    data
                    nextPageTimestamp
                }}
            }}
        }}
    }}
    '''.format(url=url)
    return fetchGraphQL(query)


#####################
##### Twin Emps #####
def twinEmpEvents(url: str) -> dict:
    query = '''
    {{
        reportData {{
            report(code: "{url}") {{
                events(
                    dataType: Casts
                    startTime: 0
                    endTime: 99999999999
                    hostilityType: Enemies
                    abilityID: 800
                ) {{
                    data
                    nextPageTimestamp
                }}
            }}
        }}
    }}
    '''.format(url=url)
    return fetchGraphQL(query)


#####################
##### Patchwerk #####
def patchwerkHatefulStrike(url: str) -> dict:
    query = '''
    {{
        reportData {{
            report(code: "{url}") {{
                events(
                    dataType: DamageDone
                    startTime: 0
                    endTime: 99999999999
                    hostilityType: Enemies
                    abilityID: 28308
                ) {{
                    data
                    nextPageTimestamp
                }}
            }}
        }}
    }}
    '''.format(url=url)
    return fetchGraphQL(query)


####################
##### Partials #####
def reportEnemiesQuery(url: str):
    query = '''
    {{
        reportData {{
            report(code: "{reportUrl}") {{
                masterData(translate: true) {{
                    actors(type: "NPC") {{
                        id
                        gameID
                    }}
                }}
            }}
        }}
    }}
    '''.format(reportUrl=url)
    return fetchGraphQL(query)


def reportDebuffsQuery(url: str, bossID: int, curse: int, modifiers: list):
    query = f'''
    {{
        reportData {{
            report(code: "{url}") {{
                curse: table(
                    dataType: Debuffs, 
                    startTime: 0, 
                    endTime: 99999999999, 
                    hostilityType: Enemies
                    abilityID: {curse}
                    filterExpression: "target.id = {bossID}"
                )
    '''
    for mod in modifiers:
        query += '''{queryName}: events(
            dataType: Debuffs, 
            startTime: 0, 
            endTime: 99999999999, 
            hostilityType: Enemies
            abilityID: {ability}
            filterExpression: "target.id = {bossID}"
        ) {{ data }}
        '''.format(
            queryName=mod.get('name'),
            ability=mod.get('id'),
            bossID=bossID
        )
    query += '''} } }'''
    return fetchGraphQL(query)


def reportCastAndDamageQuery(url: str, bossID: int, abilities: list):  # Exclude tick damage in query
    abilityQuery = ', '.join(str(cast) for cast in abilities)
    filterExpression = 'target.id = {bossID} and ability.id in ({abilityQuery}) and isTick = false'.format(
        bossID=bossID,
        abilityQuery=abilityQuery
    )
    query = '''
    {{
        reportData {{
            report(code: "{url}") {{
                casts: events(
                    startTime: 0
                    endTime: 999999999999
                    dataType: Casts
                    filterExpression: "{filterExpression}"
                ) {{
                    data
                }}
                damage: events(
                    startTime: 0
                    endTime: 999999999999
                    dataType: DamageDone
                    filterExpression: "{filterExpression}"
                ) {{
                    data
                }}
            }}
        }}
    }}
    '''.format(url=url, filterExpression=filterExpression)
    return fetchGraphQL(query)


####################
##### Wands #####
def reportGearQueryWands(url: str, startTime: int = 0) -> dict:
    query = f'''
    {{
        reportData {{
            report(code: "{url}") {{
                masterData {{
                    actors(type: "Player") {{
                        id
                        type
                        subType
                    }}
                }}
                events(
                    dataType: CombatantInfo
                    endTime: 99999999999
                    startTime: {startTime}
                    encounterID: 616
                ) {{
                    data
                    nextPageTimestamp
                }}
            }}
        }}
    }}
    '''
    return fetchGraphQL(query)


def reportGearQuerySmite(url: str, startTime: int = 0) -> dict:
    query = f'''
    {{
        reportData {{
            report(code: "{url}") {{
                masterData {{
                    actors(type: "Player") {{
                        id
                        type
                        subType
                    }}
                }}
                events(
                    dataType: CombatantInfo
                    endTime: 99999999999
                    startTime: {startTime}
                    encounterID: 717
                ) {{
                    data
                    nextPageTimestamp
                }}
            }}
        }}
    }}
    '''
    return fetchGraphQL(query)


def reportDamageQueryWands(url: str) -> dict:
    query = f'''
    {{
        reportData {{
            report(code: "{url}") {{
                events(
                    dataType: DamageDone
                    endTime: 99999999999
                    startTime: 0
                    encounterID: 616
                    abilityID: 5019
                ) {{
                    data
                    nextPageTimestamp
                }}
            }}
        }}
    }}
    '''
    return fetchGraphQL(query)


def reportDamageQuerySmite(url: str) -> dict:
    query = f'''
    {{
        reportData {{
            report(code: "{url}") {{
                events(
                    dataType: DamageDone
                    killType: Encounters
                    endTime: 99999999999
                    encounterID: 717
                    startTime: 0
                    abilityID: 10934
                ) {{
                    data
                    nextPageTimestamp
                }}
            }}
        }}
    }}
    '''
    return fetchGraphQL(query)


def sapphDmgTaken(url: str, startTime: int = 0):
    query = f'''
    {{
        reportData {{
            report(code: "{url}") {{
                events(
                      encounterID: 1119
                      killType: All
                      dataType: DamageTaken
                      startTime: {startTime}
                      endTime: 99999999999
                      abilityID: 28531
                ) {{
                    data
                    nextPageTimestamp
                }}
            }}
        }}
    }}
    '''
    return fetchGraphQL(query)


def obsidianTable(url: str):
    query = f'''
    {{
        reportData {{
            report(code: "{url}") {{
                table(
                      encounterID: 1119
                      killType: All
                      dataType: DamageDone
                      startTime: 0
                      endTime: 99999999999
                        filterExpression: "source.class in ('Warrior', 'Paladin')"
                )
            }}
        }}
    }}
    '''
    return fetchGraphQL(query)


#####################
##### Time to first cast #####
def firstCastTime(url: str, encounterID: int, abilityID: int) -> dict:
    query = f'''
    {{
        reportData {{
            report(code: "{url}") {{
                fights(
                    killType: All
                    encounterID: {encounterID}
                ) {{
                    startTime
                }}
                events(
                    dataType: Casts
                    startTime: 0
                    endTime: 99999999999
                    hostilityType: Enemies
                    abilityID: {abilityID}
                ) {{
                    data
                    nextPageTimestamp
                }}
            }}
        }}
    }}
    '''
    return fetchGraphQL(query)
