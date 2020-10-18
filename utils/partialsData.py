encounters = [
    # Complete zone crawls (e.g AQ - 1005 also may include some trash mobs from given zone)
    # Check trash section at very bottom of this list

    ##### Ahn`Qiraj SECTION #####
    {
        "encounterID": 709,
        "name": "Skeram",
        'bossID': 15263,
        'zone': 1005
    },
    {
        "encounterID": 710,
        "name": "BugTrio",
        'bossID': 15511,  # Lord Kri
        'zone': 1005
    },
    {
        "encounterID": 711,
        "name": "Sartura",
        'bossID': 15516,
        'zone': 1005
    },
    {
        "encounterID": 712,
        "name": "Fankriss",
        'bossID': 15510,
        'zone': 1005
    },
    {
        "encounterID": 714,
        "name": "Huhuran",
        'bossID': 15509,
        'zone': 1005
    },
    {
        "encounterID": 715,
        "name": "TwinEmperors",
        'bossID': 15276,  # Vek`lor
        'zone': 1005
    },
    {
        "encounterID": 716,
        "name": "Ouro",
        'bossID': 15517,
        'zone': 1005
    },
    {
        "encounterID": 717,
        "name": "CthunP1",
        'bossID': 15589,  # Eye of Cthun
        'zone': 1005
    },
    {
        "encounterID": 717,
        "name": "CthunP2",
        'bossID': 15727,  # Cthun himself
        'zone': 1005
    },
    {
        "encounterID": 717,
        "name": "CthunTentacle",
        'bossID': 15728,  # Giant Claw Tentacle
        'zone': 1005
    },
    {
        'name': 'AQ'  # Will run for every boss for zone=1005
    },

    ##### MOLTEN CORE SECTION ######
    {
        "encounterID": 663,
        "name": "Lucifiron",
        'bossID': 12118,
        'zone': 1000
    },
    {
        "encounterID": 664,
        "name": "Magmadar",
        'bossID': 11982,
        'zone': 1000
    },
    {
        "encounterID": 665,
        "name": "Gehennas",
        'bossID': 12259,
        'zone': 1000
    },
    {
        "encounterID": 666,
        "name": "Garr",
        'bossID': 12057,
        'zone': 1000
    },
    {
        "encounterID": 666,
        "name": "Sulfuron",
        'bossID': 12098,
        'zone': 1000
    },
    {
        "encounterID": 666,
        "name": "Golemagg",
        'bossID': 11988,
        'zone': 1000
    },
    {
        "encounterID": 666,
        "name": "MajordomoFlamewakerElite",
        'bossID': 11664,
        'zone': 1000
    },
    {
        "encounterID": 666,
        "name": "MajordomoFlamewakerHealer",
        'bossID': 11663,
        'zone': 1000
    },
    {
        'name': 'MC'  # Will run for every boss for zone=1000
    },

    ##### NAXX SECTION ######
    {
        "encounterID": 1107,
        "name": "Anub",
        'bossID': 15956,
        'zone': 1006
    },
    {
        "encounterID": 1110,
        "name": "Faerlina",
        'bossID': 15953,
        'zone': 1006
    },
    {
        "encounterID": 1116,
        "name": "Maexxna",
        'bossID': 15952,
        'zone': 1006
    },
    {
        'name': 'NAXX'  # Will run for every boss for zone=1006
    },

    ##### TRASH SECTION #####
    # Results COULD be scuffed for fights where multiple mobs of same ID are present
    # Cuz script will assume curse is up on all of them, if curse is presented on one of them
    # This section is mostly for confirming no high-resisted trash mobs are present
    {
        "encounterID": 0,
        "name": "AnubisathDefender",
        'bossID': 15277,  # Lvl 62
        'zone': 1005
    },
    {
        "encounterID": 0,
        "name": "AnubisathWarder",
        'bossID': 15311,  # Lvl 63
        'zone': 1005
    },
    {
        "encounterID": 0,
        "name": "VeknissGuardian",
        'bossID': 15233,  # Lvl 61
        'zone': 1005
    },
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
            'curseID': 11722,  # Curse of Elements
            'damageModifiers': [
                {'id': 22959, 'mod': 0.03, 'name': 'scorch'},  # Improved Scorch
                {'id': 23605, 'mod': 0.15, 'name': 'nightfall'},  # Nightfall
            ],
            'spellIDs': [10151, 25306, 10207, 10199],  # Fireball r11, r12, Scorch, Fireblast
            'hitTypes': {
                1: 1,  # hitType = 1, hit
                2: 1.5,  # hitType = 2, crit
                16: 1,  # hitType = 16, partial hit
                17: 1.5  # hitType = 17, partial crit
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
