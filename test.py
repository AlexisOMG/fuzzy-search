from bk_tree import levenshtein_distance
a, b = 'book', 'back'
print(f'{a}, {b} dist = {levenshtein_distance(a, b)}, equal = {levenshtein_distance(a, b) == 2}')
a, b = 'hfjrfr', 'hjdrfjkfhrjf'
print(f'{a}, {b} dist = {levenshtein_distance(a, b)}, equal = {levenshtein_distance(a, b) == 7}')
a, b = 'hfjrfr', 'hfjrfr'
print(f'{a}, {b} dist = {levenshtein_distance(a, b)}, equal = {levenshtein_distance(a, b) == 0}')