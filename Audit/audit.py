'''
This is a script to give an overall look at the data. 
It grabs a count of all unique tags in the OSM file
It grabs a count of all unique K tags in the OSM file
It grabs a list of all irregular street name endings

This does not change the file, that will happen on the data cleanup phase
It just gives an idea of how much cleaning this file will require.
'''

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
expected_street_types = ["Street","street", "Avenue","avenue", "Boulevard","boulevard", "Drive","drive",
            "Court","court", "Place","place", "Square","square", "Lane","lane",
            "Road","road","Trail","trail", "Parkway","parkway", "Commons","commons",
            "Highway","highway","Way","way"]

# The expected directions
expected_street_directions = ["Southeast","southeast",'SOUTHWEST', "Southwest","southwest", "Northeast","northeast",
             "Northwest","northwest",'East',"east",'West',"west",'North',"north",
             'South',"south"]

def count_unique(value, unique_list):
    if value in unique_list.keys():
        unique_list[value] += 1
    else:
        unique_list[value] = 1


# List all of the unique k tags in the file with counts
def list_unique_k_tags(filename):
        unique_k_tags={}
        for event, elem in ET.iterparse(filename, events=("start",)):    
            # If the element is a tag and has a k attribute, add it to the return        
            if elem.tag == 'tag' and 'k' in elem.attrib:
                if elem.get('k') in unique_k_tags.keys():
                    unique_k_tags[elem.get('k')]=unique_k_tags[elem.get('k')]+1
                else:
                    unique_k_tags[elem.get('k')]=1  
        # Sort the results in reverse order
        sorted_tags = sorted(unique_k_tags.items(), key=operator.itemgetter(1)) 
        sorted_tags.reverse()    
        return sorted_tags     

# Verify the street type is either one of the expected street types or expected street directions
# IE Street instead of St. or Northwest instead of NW
def audit_street_type(street_types, street_name):  
    match = street_type_re.search(street_name)
    if match:
        street_type = match.group()
        if (street_type not in expected_street_types) and (street_type not in expected_street_directions):   
            street_types[street_type].add(street_name)
            
# Is this a street name element
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_post_code(elem):
    return (elem.attrib['k'] == 'addr:postcode')

# Main audit function
def audit_file(filename):
    audit_data = { 
        'unique_tags': {},
        'postal_codes': {},
        'unique_k_tags_count': {},
        'irregular_street_names': defaultdict(set) }
    # I only want to iterate once over the file and check each record for the items I am looking for 
    for event, elem in ET.iterparse(filename, events=("start",)):
        # Always process for unique_tags
        count_unique(elem.tag, audit_data['unique_tags'])
        # If it is a k tag, process k tag
        if elem.tag == 'tag' and 'k' in elem.attrib:
            count_unique(elem.get('k'), audit_data['unique_k_tags_count'])
        # If it is a street, process street
        if (elem.tag == "node" or elem.tag == "way"):
            # Iterate over sub elements, ifits a street name, add to irregular list 
            for tag in elem.iter('tag'):
                if is_street_name(tag):
                    audit_street_type(audit_data['irregular_street_names'], tag.attrib['v'])
                if is_post_code(tag):
                    count_unique(tag.attrib['v'], audit_data['postal_codes'])
                   
                   

    # Sort the k tags desc
    sorted_tags = sorted(audit_data['unique_k_tags_count'].items(), key=operator.itemgetter(1)) 
    sorted_tags.reverse()    
    audit_data['unique_k_tags_count'] = sorted_tags
    return audit_data

if __name__ == '__main__':
    # Audit the file
    audit_data = audit_file('norman-sample.osm')
    print('Count of unique tags in the file: {}'.format(len(audit_data['unique_tags'])))
    print('Count of unique k values in the file: {}'.format(len(audit_data['unique_k_tags_count'])))
    print('Count of irregular street endings in the file: {}'.format(len(audit_data['irregular_street_names'])))
    print('Count of unique postcodes: {}'.format(len(audit_data['postal_codes'])))
    print('Primary tags with counts in the file:')
    pprint.pprint(audit_data['unique_tags'])
    print('K tag values with counts in the file:')
    pprint.pprint(audit_data['unique_k_tags_count'])
    print('Irregular street endings in the file:')
    pprint.pprint(audit_data['irregular_street_names'])
    print('Post codes in the file:')
    pprint.pprint(audit_data['postal_codes'])
    