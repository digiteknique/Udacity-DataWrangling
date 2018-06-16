#import sys
#sys.modules[__name__].__dict__.clear()
import xml.etree.cElementTree as ET
from audit_fileselector import get_filename

# Is this a state element
def is_state(elem):
    return (elem.attrib['k'] == "addr:state")

# Main audit function
def display_state_errors(filename):
    error_states = set()
    # I only want to iterate once over the file and check each record for the items I am looking for 
    for _, elem in ET.iterparse(filename, events=("start",)):
        # If it is a state, process 
        if (elem.tag == "node" or elem.tag == "way"):
            # Iterate over sub elements, if its a state
            for tag in elem.iter('tag'):
                if is_state(tag):
                    state = tag.attrib['v']
                    if state != 'OK':
                        error_states.add(state)
    print('States that are not listed as OK:')
    print(error_states)


if __name__ == '__main__':
    # Audit the file
    display_state_errors(get_filename())
    