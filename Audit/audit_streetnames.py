#import sys
#sys.modules[__name__].__dict__.clear()
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import operator
from audit_fileselector import get_filename


# Regular expression to get the street type
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# The expected types of street
expected_street_types = ['Street', 'Avenue', 'Boulevard', 'Drive', 'Court', 'Circle',
                         'Diagonal', 'Place', 'Square', 'Lane', 'Road', 'Trail', 'Parkway', 
                         'Commons', 'Highway', 'Way', 'Terrace', 'Southeast', 'Southwest', 
                         'Northeast', 'Northwest', 'East', 'West', 'North', 'South']



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
    for _, elem in ET.iterparse(filename, events=("start",)):
        if (elem.tag == "node" or elem.tag == "way"):
            for tag in elem.iter('tag'):
                if is_street_name(tag):
                    audit_street_type(irregular_street_names, tag.attrib['v'])
    print('Irregular street naming')
    pprint.pprint(irregular_street_names)                
    return irregular_street_names



if __name__ == '__main__':
    # Audit the file
    audit_street_types(get_filename())
    