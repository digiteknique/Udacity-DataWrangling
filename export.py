'''
Much of this was taken from Udacity course information
'''
#import sys
#sys.modules[__name__].__dict__.clear()
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import csv
import pprint
import cerberus
import schema
import codecs
from Clean.clean_postcodes import replace_zipcode
from Clean.clean_streetnames import rename_street_name

OSM_PATH = 'norman.osm'

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user',
               'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

# Is this a street name element


def is_street_name(elem):
    return elem.attrib['k'] == "addr:street"

# Is this a post code element


def is_post_code(elem):
    return elem.attrib['k'] == 'addr:postcode'


def fix_element(element):
    if element.tag == "node" or element.tag == "way":
        for tag in element.iter("tag"):
            if is_street_name(tag):
                name = tag.attrib['v']
                better_name = rename_street_name(name)
                if name != better_name:
                    tag.attrib['v'] = better_name
                    print('Fixed Street: {} => {}'.format(name, better_name))
            if is_post_code(tag):
                zipcode = tag.attrib['v']
                better_zipcode = replace_zipcode(zipcode)
                if zipcode != better_zipcode:
                    tag.attrib['v'] = better_zipcode
                    print('Fixed Zipcode: {} => {}'.format(zipcode, better_zipcode))

def shape_generic_element(element, attr_fields):
    attribs = {}
    tags = []
    for field in attr_fields:
        attribs[field] = element.attrib[field]
        
    for tag in element.iter('tag'):
        k = tag.attrib['k']

        # remove any problem chars
        if re.search(problemchars, k):
            continue 

        tag_dictionary = {}
        tag_dictionary['id'] = attribs['id']

        colon_present = k.split(':')
        if len(colon_present) == 1:
            tag_dictionary['key'] = k
            tag_dictionary['type'] = 'regular'
        elif len(colon_present) == 2:
            tag_dictionary['key'] = colon_present[1]
            tag_dictionary['type'] = colon_present[0]
        else: 
            tag_dictionary['key'] = ':'.join(colon_present[1:])
            tag_dictionary['type'] = colon_present[0]
            
        tag_dictionary['value'] = tag.attrib['v']
        tags.append(tag_dictionary)
    return { 'attribs': attribs, 'tags': tags }


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=problemchars, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""
    way_nodes = []
    fix_element(element)
    if element.tag in ['node', 'way']:
        
        # Node element, parse it out
        if element.tag == 'node':
            data = shape_generic_element(element, node_attr_fields)
            return {'node': data['attribs'], 'node_tags': data['tags']}
        else:
            data = shape_generic_element(element, way_attr_fields)
            # Get the nodes
            n = 0
            for node in element.iter('nd'):
                node_dict = {}
                node_dict['id'] = data['attribs']['id']
                node_dict['node_id'] = node.attrib['ref']
                node_dict['position'] = n
                way_nodes.append(node_dict)
                n += 1
            return {'way': data['attribs'], 'way_nodes': way_nodes, 'way_tags': data['tags']}

# ================================================== #
#               Helper Functions                     #
# ================================================== #


def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)

        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, str) else v) for k, v in row.items()#.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
            codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
            codecs.open(WAYS_PATH, 'w') as ways_file, \
            codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
            codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=False)
    print('Export complete')
