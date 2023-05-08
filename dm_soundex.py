from itertools import groupby
from unicodedata import normalize as unicode_normalize
import string

dms_mappings = {
    'combinations': {
        'STCH': (2, 4, 4),
        'DRZ': (4, 4, 4),
        'ZH': (4, 4, 4),
        'ZHDZH': (2, 4, 4),
        'DZH': (4, 4, 4),
        'DRS': (4, 4, 4),
        'DZS': (4, 4, 4),
        'SCHTCH': (2, 4, 4),
        'SHTSH': (2, 4, 4),
        'SZCZ': (2, 4, 4),
        'TZS': (4, 4, 4),
        'SZCS': (2, 4, 4),
        'STSH': (2, 4, 4),
        'SHCH': (2, 4, 4),
        'D': (3, 3, 3),
        'H': (5, 5, '_'),
        'TTSCH': (4, 4, 4),
        'THS': (4, 4, 4),
        'L': (8, 8, 8),
        'P': (7, 7, 7),
        'CHS': (5, 54, 54),
        'T': (3, 3, 3),
        'X': (5, 54, 54),
        'OJ': (0, 1, '_'),
        'OI': (0, 1, '_'),
        'SCHTSH': (2, 4, 4),
        'OY': (0, 1, '_'),
        'Y': (1, '_', '_'),
        'TSH': (4, 4, 4),
        'ZDZ': (2, 4, 4),
        'TSZ': (4, 4, 4),
        'SHT': (2, 43, 43),
        'SCHTSCH': (2, 4, 4),
        'TTSZ': (4, 4, 4),
        'TTZ': (4, 4, 4),
        'SCH': (4, 4, 4),
        'TTS': (4, 4, 4),
        'SZD': (2, 43, 43),
        'AI': (0, 1, '_'),
        'PF': (7, 7, 7),
        'TCH': (4, 4, 4),
        'PH': (7, 7, 7),
        'TTCH': (4, 4, 4),
        'SZT': (2, 43, 43),
        'ZDZH': (2, 4, 4),
        'EI': (0, 1, '_'),
        'G': (5, 5, 5),
        'EJ': (0, 1, '_'),
        'ZD': (2, 43, 43),
        'IU': (1, '_', '_'),
        'K': (5, 5, 5),
        'O': (0, '_', '_'),
        'SHTCH': (2, 4, 4),
        'S': (4, 4, 4),
        'TRZ': (4, 4, 4),
        'SHD': (2, 43, 43),
        'DSH': (4, 4, 4),
        'CSZ': (4, 4, 4),
        'EU': (1, 1, '_'),
        'TRS': (4, 4, 4),
        'ZS': (4, 4, 4),
        'STRZ': (2, 4, 4),
        'UY': (0, 1, '_'),
        'STRS': (2, 4, 4),
        'CZS': (4, 4, 4),
        'MN': ('6_6', '6_6', '6_6'),
        'UI': (0, 1, '_'),
        'UJ': (0, 1, '_'),
        'UE': (0, '_', '_'),
        'EY': (0, 1, '_'),
        'W': (7, 7, 7),
        'IA': (1, '_', '_'),
        'FB': (7, 7, 7),
        'STSCH': (2, 4, 4),
        'SCHT': (2, 43, 43),
        'NM': ('6_6', '6_6', '6_6'),
        'SCHD': (2, 43, 43),
        'B': (7, 7, 7),
        'DSZ': (4, 4, 4),
        'F': (7, 7, 7),
        'N': (6, 6, 6),
        'CZ': (4, 4, 4),
        'R': (9, 9, 9),
        'U': (0, '_', '_'),
        'V': (7, 7, 7),
        'CS': (4, 4, 4),
        'Z': (4, 4, 4),
        'SZ': (4, 4, 4),
        'TSCH': (4, 4, 4),
        'KH': (5, 5, 5),
        'ST': (2, 43, 43),
        'KS': (5, 54, 54),
        'SH': (4, 4, 4),
        'SC': (2, 4, 4),
        'SD': (2, 43, 43),
        'DZ': (4, 4, 4),
        'ZHD': (2, 43, 43),
        'DT': (3, 3, 3),
        'ZSH': (4, 4, 4),
        'DS': (4, 4, 4),
        'TZ': (4, 4, 4),
        'TS': (4, 4, 4),
        'TH': (3, 3, 3),
        'TC': (4, 4, 4),
        'A': (0, '_', '_'),
        'E': (0, '_', '_'),
        'I': (0, '_', '_'),
        'AJ': (0, 1, '_'),
        'M': (6, 6, 6),
        'Q': (5, 5, 5),
        'AU': (0, 7, '_'),
        'IO': (1, '_', '_'),
        'AY': (0, 1, '_'),
        'IE': (1, '_', '_'),
        'ZSCH': (4, 4, 4),
        'CH': ((5, 4), (5, 4), (5, 4)),
        'CK': ((5, 45), (5, 45), (5, 45)),
        'C': ((5, 4), (5, 4), (5, 4)),
        'J': ((1, 4), ('_', 4), ('_', 4)),
        'RZ': ((94, 4), (94, 4), (94, 4)),
        'RS': ((94, 4), (94, 4), (94, 4)),
    },
    'ordering': {
        'A': ('AI', 'AJ', 'AU', 'AY', 'A'),
        'B': ('B',),
        'C': ('CHS', 'CSZ', 'CZS', 'CH', 'CK', 'CS', 'CZ', 'C'),
        'D': ('DRS', 'DRZ', 'DSH', 'DSZ', 'DZH', 'DZS', 'DS', 'DT', 'DZ', 'D'),
        'E': ('EI', 'EJ', 'EU', 'EY', 'E'),
        'F': ('FB', 'F'),
        'G': ('G',),
        'H': ('H',),
        'I': ('IA', 'IE', 'IO', 'IU', 'I'),
        'J': ('J',),
        'K': ('KH', 'KS', 'K'),
        'L': ('L',),
        'M': ('MN', 'M'),
        'N': ('NM', 'N'),
        'O': ('OI', 'OJ', 'OY', 'O'),
        'P': ('PF', 'PH', 'P'),
        'Q': ('Q',),
        'R': ('RS', 'RZ', 'R'),
        'S': (
            'SCHTSCH',
            'SCHTCH',
            'SCHTSH',
            'SHTCH',
            'SHTSH',
            'STSCH',
            'SCHD',
            'SCHT',
            'SHCH',
            'STCH',
            'STRS',
            'STRZ',
            'STSH',
            'SZCS',
            'SZCZ',
            'SCH',
            'SHD',
            'SHT',
            'SZD',
            'SZT',
            'SC',
            'SD',
            'SH',
            'ST',
            'SZ',
            'S',
        ),
        'T': (
            'TTSCH',
            'TSCH',
            'TTCH',
            'TTSZ',
            'TCH',
            'THS',
            'TRS',
            'TRZ',
            'TSH',
            'TSZ',
            'TTS',
            'TTZ',
            'TZS',
            'TC',
            'TH',
            'TS',
            'TZ',
            'T',
        ),
        'U': ('UE', 'UI', 'UJ', 'UY', 'U'),
        'V': ('V',),
        'W': ('W',),
        'X': ('X',),
        'Y': ('Y',),
        'Z': (
            'ZHDZH',
            'ZDZH',
            'ZSCH',
            'ZDZ',
            'ZHD',
            'ZSH',
            'ZD',
            'ZH',
            'ZS',
            'Z',
        ),
    },
    'vowels': set('AEIJOUY'),
}

def delete_consecutive_repeats(word: str) -> str:
    return ''.join(char for char, _ in groupby(word))

def daitch_mokotoff_encode(word: str, max_length: int = 6, zero_pad: bool = True) -> str:
    def find_matching_substring(pos, order):
        for substr in order[word[pos]]:
            if word[pos:].startswith(substr):
                return substr
        return None

    def get_dm_code(pos, substr, table):
        dm_values = table[substr]
        if pos == 0:
            return dm_values[0]
        elif pos + len(substr) < len(word) and word[pos + len(substr)] in dms_mappings['vowels']:
            return dm_values[1]
        else:
            return dm_values[2]

    dms_codes = ['']
    word = unicode_normalize('NFKD', word.upper())
    word = ''.join(c for c in word if c in string.ascii_uppercase)

    if not word:
        return '0' * max_length if zero_pad else '0'

    pos = 0
    while pos < len(word):
        substr = find_matching_substring(pos, dms_mappings['ordering'])
        if substr:
            dm_value = get_dm_code(pos, substr, dms_mappings['combinations'])

            if isinstance(dm_value, tuple):
                dms_codes = [code + str(dm_value[0]) for code in dms_codes] + [code + str(dm_value[1]) for code in dms_codes]
            else:
                dms_codes = [code + str(dm_value) for code in dms_codes]
            pos += len(substr)

    dms_codes = [''.join(c for c in delete_consecutive_repeats(code) if c != '_') for code in dms_codes]
    dms_codes = [code[:max_length] for code in dms_codes]
    if zero_pad:
        dms_codes = [code.ljust(max_length, '0') for code in dms_codes]

    return dms_codes[0]

def dms_table():
    return dms_mappings['combinations']

def dms_order():
    return dms_mappings['ordering']

def uc_v_set():
    return dms_mappings['vowels']

def encode(word: str, max_length: int = 6, zero_pad: bool = True) -> str:
    dms_table_data = dms_table()
    dms_order_data = dms_order()
    uc_v_set_data = uc_v_set()
    uc_set = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    dms = ['']

    word = unicode_normalize('NFKD', word.upper())
    word = ''.join(c for c in word if c in uc_set)

    if not word:
        if zero_pad:
            return '0' * max_length
        return '0'

    pos = 0
    while pos < len(word):
        for sstr in dms_order_data[word[pos]]:
            if word[pos:].startswith(sstr):
                dm_tup = dms_table_data[sstr]

                if pos == 0:
                    dm_val = dm_tup[0]
                elif (
                    pos + len(sstr) < len(word)
                    and word[pos + len(sstr)] in uc_v_set_data
                ):
                    dm_val = dm_tup[1]
                else:
                    dm_val = dm_tup[2]

                if isinstance(dm_val, tuple):
                    dms = [_ + str(dm_val[0]) for _ in dms] + [
                        _ + str(dm_val[1]) for _ in dms
                    ]
                else:
                    dms = [_ + str(dm_val) for _ in dms]
                pos += len(sstr)
                break
    dms = [
        ''.join(c for c in delete_consecutive_repeats(_) if c != '_')
        for _ in dms
    ]

    if zero_pad:
        dms = [
            (_ + ('0' * max_length))[: max_length] for _ in dms
        ]
    else:
        dms = [_[:max_length] for _ in dms]
    return dms[0]
