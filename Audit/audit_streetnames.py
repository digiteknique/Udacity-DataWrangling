#import sys
#sys.modules[__name__].__dict__.clear()
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import operator


# Regular expression to get the street type
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# The expected types of street
expected_street_types = ['Street', 'Avenue', 'Boulevard', 'Drive', 'Court', 'Circle',
                         'Diagonal', 'Place', 'Square', 'Lane', 'Road', 'Trail', 'Parkway', 
                         'Commons', 'Highway', 'Way', 'Terrace', 'Southeast', 'Southwest', 
                         'Northeast', 'Northwest', 'East', 'West', 'North', 'South']

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

# Is this a street name element
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

# Verify the street type is either one of the expected street types or expected street directions
# IE Street instead of St. or Northwest instead of NW
def audit_street_type(street_types, street_name):  
    match = street_type_re.search(street_name)
    if match:
        street_type = match.group()
        if (street_type not in expected_street_types): # and (street_type not in expected_street_directions):   
            street_types[street_type].add(street_name)
            

def audit_street_types(filename):
    irregular_street_names = defaultdict(set)
    for event, elem in ET.iterparse(filename, events=("start",)):
        if (elem.tag == "node" or elem.tag == "way"):
            for tag in elem.iter('tag'):
                if is_street_name(tag):
                    print(tag.attrib['v'], rename_street_name(tag.attrib['v']))
                    audit_street_type(irregular_street_names, tag.attrib['v'])
                    
    return irregular_street_names

# Rename the street to match our convention using the defined mapping
# Iterating over the words to match 
def rename_street_name(name):
    words = name.split()
    for w in range(len(words)):
        if(words[w] in mapping):
            if(words[w - 1].lower() not in ['suite', 'ste.', 'ste']):
                words[w] = mapping[words[w]]
    name = ' '.join(words)
    # special case for street name of just "Maple"
    if name.lower() == 'maple':
        name = 'Maple Avenue'
    return name 

if __name__ == '__main__':
    # Audit the file
    audit_data = audit_street_types('norman.osm')
    print('Irregular street naming')
    pprint.pprint(audit_data)