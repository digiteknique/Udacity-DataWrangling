# Rename the street to match our convention using the defined mapping
# Iterating over the words to match 
def rename_street_name(name):
    mapping = {
        'Ave': 'Avenue',
        'Ave.': 'Avenue',
        'Blvd': 'Boulevard',
        'Blvd.': 'Boulevard',
        'DR': 'Drive',
        'Rd': 'Road',
        'St': 'Street',
        'St.': 'Street',
        'Steet': 'Street',
        'NE': 'Northeast',
        'SW': 'Southwest',
        'SE': 'Southeast',
        'NW': 'Northwest',
        'N': 'North',
        'S': 'South',
        'E': 'East',
        'W': 'West',
        'N.': 'North',
        'S.': 'South',
        'E.': 'East',
        'W.': 'West',
    }

    words = name.split()
    for w in range(len(words)):
        if(words[w] in mapping):
            if(words[w - 1].lower() not in ['suite', 'ste.', 'ste']):
                words[w] = mapping[words[w]]
    name = ' '.join(words)
    # special case for street name of just "Maple". I looked up the address
    if name.lower() == 'maple':
        name = 'Maple Avenue'
    # special case for street name of just "73069". I looked up the address
    if name == '73069':
        name = 'West Robinson Avenue'
    return name 
