from utils.querys import fetchGraphQL
from utils.utils import writeToFile
import json

"""
reportSet = set()
for page in range(1, 6):
    query = f'''
    {{
        worldData {{
            encounter(id: 1120) {{
                characterRankings(
                    className: "Mage"
                    includeCombatantInfo: false
                    page: {page}
                )
            }}
        }}
    }}
    '''
    response = fetchGraphQL(query).get('worldData').get('encounter').get('characterRankings').get('rankings')
    for item in response:
        reportSet.add(item.get('report').get('code'))
writeToFile(data=list(reportSet), filename='rankings.json')
"""
"""
data = open('rankings.json')
data = json.load(data)
for code in data:
    query = f'''
        {{
            reportData {{
                report(code: "{code}") {{
                    table(
                        dataType: Debuffs
                        hostilityType: Enemies
                        encounterID: 1120
                        abilityID: 12654
                        endTime: 999999999999
                        filterExpression: "target.id = 15928"
                    )
                }}
            }}
        }}
        '''
    response = fetchGraphQL(query).get('reportData').get('report').get('table').get('data').get('auras')
    print(response)
"""
for page in range(1, 101):
    query = f'''
    {{
    reportData {{
        reports(page: {page}) {{
            data {{
                code
            }}
        }}
    }}
}}
    '''
    response = fetchGraphQL(query)
    for code in response.get('reportData').get('reports').get('data'):
        url = code.get('code')
        query = f'''
        {{
            reportData {{
               report(code: "{url}") {{
                table(dataType: Debuffs, endTime: 99999999999, filterExpression: "ability.id in (28833, 28832,28834, 28835) and stack > 5")
}} }} }}
        '''
        data = fetchGraphQL(query).get('reportData').get('report').get('table').get('data').get('auras')
        if len(data) > 0:
            print(f'https://classic.warcraftlogs.com/reports/{url}')