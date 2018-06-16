#import sys
#sys.modules[__name__].__dict__.clear()
import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
from audit_fileselector import get_filename

mapping = {
    'c': '73069'
}

def is_post_code(elem):
    return (elem.attrib['k'] == 'addr:postcode')

def display_post_code_errors(filename):
    postcodes = defaultdict(int)
    for _, elem in ET.iterparse(filename, events=("start",)):
        if (elem.tag == "node" or elem.tag == "way"):
            for tag in elem.iter('tag'):
                if is_post_code(tag):
                    postcodes[tag.attrib['v']] += 1

    print('Post code data:')
    pprint.pprint(postcodes)                
    return postcodes

if __name__ == '__main__':
    # Audit the file
    display_post_code_errors(get_filename())
