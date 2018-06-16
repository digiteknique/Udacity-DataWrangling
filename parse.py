'''
This script modified irregular street names and outputs JSON objects for the xml data in the file
It then writes out a JSON file with the parsed data

'''

import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json