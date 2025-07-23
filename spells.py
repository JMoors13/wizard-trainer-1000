# spells.py

SPELLBOOK_TEMPLATES = {
    'Righteous': {
        'devotion': [
            {'name': 'saenctious might', 'level': 1, 'chance': 0.7},
            {'name': 'praengenis', 'level': 5, 'chance': 0.5},
            {'name': 'deiticous fortunes', 'level': 10, 'chance': 0.3},
        ]
    },
    'Rogue': {
        'iniquity': [
            {'name': 'marronastic depletion', 'level': 1, 'chance': 0.7},
            {'name': 'binaric removal', 'level': 5, 'chance': 0.5},
            {'name': 'cruel expulsion', 'level': 10, 'chance': 0.3},
        ]
    },
    'Unconventional': {
        'whimsy': [
            {'name': 'humarieous cuss', 'level': 1, 'chance': 0.7},
            {'name': 'bubblaeic exhaling', 'level': 5, 'chance': 0.5},
            {'name': 'delusionaic halls', 'level': 10, 'chance': 0.3},
        ]
    }
}

SHARED_SPELLS = {
    'whimsy': [
        {'name': 'laughing hex', 'level': 1, 'chance': 1.0}
    ]
}
