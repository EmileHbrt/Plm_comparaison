import os
import csv

import pandas as pd
import xml.etree.ElementTree as ET

from optparse import OptionParser

def main():
    usage = "python Interpro_parse.py -i <input_file> -o <output_folder> \n"
    parser = OptionParser(usage)
    parser.add_option("-i", "--input_file", dest="input_file", help="path for the Interpro dataset")
    parser.add_option("-o", "--output_folder", dest="output_folder", help="path to the folder where the data will be saved")

    (option, args) = parser.parse_args()
    input_file = option.input_file
    output_file = option.output_file

    try:
        xml = open(input_file, "r", encoding='utf-8')
    except:
        print(' error with -i : correspond to the path of the dataset ')

    all_db = {} # {db = [[id,name], ...], ...} que le shortname est utile !

    map_interpro = {} # {Interpro_id = ['', '', '', ...]
                      # db = ['', '', '', ...] 
                      # ... }

    ec_number = {} # { Interpro_id = [ec_1, ec_2, ...], ...}
                   # si aucun ec, l'interpro_id n'est pas dans le dic

    context = ET.iterparse(xml, events=('start', 'end'))

    interpro_id = None 
    shortname = None
    name = None
    res_tag = None

    for event, elem in context:
    
        if event == 'start' and elem.tag == 'interpro':
            interpro_id = elem.attrib.get('id')
            shortname = elem.attrib.get('short_name')
    
            if elem.tag not in all_db:
                all_db[elem.tag] = []
            all_db[elem.tag].append([interpro_id, shortname])
        
        elif event == 'start' and elem.tag == 'db_xref' and res_tag == 'member_list':
            db = elem.attrib.get('db')
            dbkey = elem.attrib.get('dbkey')
            name = elem.attrib.get('name')

            if db not in all_db:
                all_db[db] = []
            all_db[db].append([dbkey, name])

        elif event == 'start' and elem.tag == 'db_xref' and elem.attrib.get('db') == 'EC':
            if interpro_id not in ec_number:
                ec_number[interpro_id] = []
            ec_number[interpro_id].append(elem.attrib.get('dbkey'))
    
        res_tag = elem.tag

    


    


#==================================================================================================================
if __name__ == "__main__":
	main()