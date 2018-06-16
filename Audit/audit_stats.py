'''
This is a script to give an overall look at the data. 
It grabs a count of all unique tags in the OSM file
It grabs a count of all unique K tags in the OSM file
It grabs a list of all irregular street name endings

four tag categories were provided / defined by Udacity case study:
  "lower", for tags that contain only lowercase letters and are valid,
  "lower_colon", for otherwise valid tags with a colon in their names,
  "problemchars", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories.

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
from audit_fileselector import get_filename



lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def get_user(element):
    if element.get('uid'):
        uid = element.attrib['uid']
        return uid

def key_type(element, keys):
    if element.tag == 'tag':
        k = element.attrib['k']
        if re.search(lower, k): # Its a lower case key
            keys['lower'] += 1
        elif re.search(lower_colon, k):
            keys['lower_colon'] += 1
        elif re.search(problemchars, k):
            keys['problemchars'] += 1
        else:
            keys['other'] += 1
    return keys

def display_stats(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    users = set()

    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
        if get_user(element):
            users.add(get_user(element))

    
    print('Count of the tag categories: ')
    print(keys)
    print('Number of unique User IDs:')
    print(len(users))

if __name__ == '__main__':
    # Audit the file
    display_stats(get_filename())


