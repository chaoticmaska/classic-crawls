encounters = [
    # Complete zone crawls (e.g AQ - 1005 also may include some trash mobs from given zone)
    # Check trash section at very bottom of this list

    ##### Ahn`Qiraj SECTION #####
    {
        "encounterID": 2445,
        "name": "Moroes",
        'bossID': 15687,
        'zone': 1007
    },
    {
        "encounterID": 2448,
        "name": "Curator",
        'bossID': 15691,
        'zone': 1007
    },
    {
        "encounterID": 2446,
        "name": "Maiden",
        'bossID': 16457,
        'zone': 1007
    },
    {
        "encounterID": 2453,
        "name": "Malchezaar",
        'bossID': 15690,
        'zone': 1007
    },
    {
        "encounterID": 2454,
        "name": "Nightbane",
        'bossID': 17225,
        'zone': 1007
    },
    {
        "encounterID": 2450,
        "name": "Aran",
        'bossID': 16524,
        'zone': 1007
    },
    {
        'name': 'Kara'
    },
    {
        "encounterID": 2456,
        "name": "Gruul",
        'bossID': 19044,
        'zone': 1008
    },
    {
        "encounterID": 2457,
        "name": "Mag",
        'bossID': 17257,
        'zone': 1008
    },

    ##### TRASH SECTION #####
    # Results COULD be scuffed for fights where multiple mobs of same ID are present
    # Cuz script will assume curse is up on all of them, if curse is presented on one of them
    # This section is mostly for confirming no high-resisted trash mobs are present
]

availableEncounters = list(
    map(
        lambda encounter: encounter.get('name'), encounters
    )
)


def mapRaidZone(raidID: int):
    return list(
        filter(
            lambda encounter: encounter.get('zone') == raidID, encounters
        )
    )


def mapCrawlArgs(school: str, raidZone: str):
    if school == 'Fire':
        spellData = {
            'curseID': 117222,  # Curse of Elements
            'damageModifiers': [
                {'id': 22959, 'mod': 0.03, 'name': 'scorch'},  # Improved Scorch
                {'id': 33200, 'mod': 0.05, 'name': 'misery'},
                {'id': 11722, 'mod': 0.1, 'name': 'coethree'},
                {'id': 27228, 'mod': 0.1, 'name': 'coefour'},
                {'id': 30254, 'mod': 2, 'name': 'evo'}
            ],
            'spellIDs': [27070, 27074, 27079],  # Fireball, Scorch, Fireblast
            'hitTypes': {
                1: 1,  # hitType = 1, hit
                2: 1.545,  # hitType = 2, crit
                16: 1,  # hitType = 16, partial hit
                17: 1.545  # hitType = 17, partial crit
            }  # Damage coefficient for hits and crits
        }
    if school == 'Arcane':
        spellData = {
            'curseID': 117222,  # Curse of Elements
            'damageModifiers': [
                {'id': 33200, 'mod': 0.05, 'name': 'misery'},
                {'id': 11722, 'mod': 0.1, 'name': 'coethree'},
                {'id': 27228, 'mod': 0.1, 'name': 'coefour'},
                {'id': 30254, 'mod': 2, 'name': 'evo'}
            ],
            'spellIDs': [30451],  # Fireball, Scorch, Fireblast
            'hitTypes': {
                1: 1,  # hitType = 1, hit
                2: 1.8175,  # hitType = 2, crit
                16: 1,  # hitType = 16, partial hit
                17: 1.8175  # hitType = 17, partial crit
            }  # Damage coefficient for hits and crits
        }
    elif school == 'Shadow':
        spellData = {
            'curseID': 17937,  # Curse of Shadow
            'damageModifiers': [
                {'id': 15258, 'mod': 0.03, 'name': 'spriest'},  # Shadow vulnerability / priest
                {'id': 17800, 'mod': 0.2, 'name': 'isb'},  # Shadow vulnerability / improved shadow bolt
                {'id': 23605, 'mod': 0.15, 'name': 'nightfall'},  # Nightfall
            ],
            'spellIDs': [11661, 25307],  # Shadow Bolt r9, r10
            'hitTypes': {
                1: 1,  # hitType = 1, hit
                2: 1.5,  # hitType = 2, crit
                16: 1,  # hitType = 16, partial hit
                17: 1.5  # hitType = 17, partial crit
            }  # Damage coefficient for hits and crits
        }

    encounterData = next(filter(lambda e: e.get('name') == raidZone, encounters))

    return {**spellData, 'encounterData': encounterData, 'zone': encounterData.get('zone')}
