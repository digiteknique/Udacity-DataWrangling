#import sys
#sys.modules[__name__].__dict__.clear()
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import operator

mapping = {
    'c': '73069'
}

def is_post_code(elem):
    return (elem.attrib['k'] == 'addr:postcode')

def audit_post_codes(filename):
    postcodes = defaultdict(int)
    for event, elem in ET.iterparse(filename, events=("start",)):
        if (elem.tag == "node" or elem.tag == "way"):
            for tag in elem.iter('tag'):
                if is_post_code(tag):
                    postcodes[tag.attrib['v']] += 1
                    
    return postcodes

if __name__ == '__main__':
    # Audit the file
    audit_data = audit_post_codes('norman.osm')
    print('Post code data:')
    pprint.pprint(audit_data)