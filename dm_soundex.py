def daitch_mokotoff_soundex(name: str) -> str:
    """
    Encode a name using the Daitch-Mokotoff Soundex algorithm.
    """
    # Convert the name to uppercase and remove non-alphabetic characters
    name = ''.join(filter(str.isalpha, name.upper()))

    # If the name is empty or has only one letter, return the original name
    if len(name) < 2:
        return name

    # Define the numerical values for each consonant
    consonants = {'B': '1', 'F': '2', 'P': '1', 'V': '2', 'G': '3', 'K': '3', 'J': '4', 'Y': '4', 'S': '8', 'Z': '8', 'X': '8', 'C': '8', 'D': '3', 'T': '3', 'L': '5', 'M': '6', 'N': '6', 'R': '7'}

    # Initialize the encoded name with the first letter
    encoded_name = name[0]

    # Encode the remaining letters of the name
    for letter in name[1:]:
        # Ignore vowels and certain consonants
        if letter in ['A', 'E', 'I', 'O', 'U', 'H', 'W']:
            continue
        # Handle special cases
        elif letter in ['C', 'S', 'X', 'Z'] and encoded_name[-1] in ['C', 'S', 'X', 'Z']:
            continue
        elif letter in ['D', 'T'] and encoded_name[-1] in ['D', 'T']:
            continue
        elif letter == 'Z' and encoded_name[-1] == 'Z':
            continue
        # Encode the consonant using its numerical value
        else:
            encoded_name += consonants[letter]

    # Pad the encoded name with zeros to ensure that it has a length of three characters
    encoded_name = (encoded_name + '000')[:3]

    return encoded_name

from transliterate import translit

# name = 'Иванов'

# transliterated_name = translit(name, 'ru', reversed=True)

# print(name, '->', transliterated_name)


name1 = 'Иванов'
name2 = 'Ивамофа'

name1 = translit(name1, 'ru', reversed=True)
name2 = translit(name2, 'ru', reversed=True)

code1 = daitch_mokotoff_soundex(name1)
code2 = daitch_mokotoff_soundex(name2)

print(name1, '->', code1)
print(name2, '->', code2)

if code1 == code2:
    print('The names sound similar.')
else:
    print('The names do not sound similar.')
