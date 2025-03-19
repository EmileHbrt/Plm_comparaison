import os
import csv

import pandas as pd
import xml.etree.ElementTree as ET

from optparse import OptionParser

#==================================================================================================================

def writter_db_id_name(dico, output):
    for db, entries in dico.items():
        csv_filename = os.path.join(output, f"{db}_id_name.csv")
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['ID', 'ShortName'])
            for entry in entries:
                writer.writerow(entry)

#==================================================================================================================

def writter_ec(dico, output):
    # Create a CSV file for interpro_ec
    csv_filename = os.path.join(output, "interpro_ec.csv")

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
      writer = csv.writer(csv_file)
      writer.writerow(['InterPro_ID', 'EC_Numbers'])  # Header row

      for interpro_id, ec_numbers in dico.items():
        writer.writerow([interpro_id, ";".join(ec_numbers)])

#==================================================================================================================

#def writter_map():

#==================================================================================================================
# 											main
#==================================================================================================================

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

    map_interpro = {} 

    ec_number = {} # { Interpro_id = [ec_1, ec_2, ...], ...}
                   # si aucun ec, l'interpro_id n'est pas dans le dic

    context = ET.iterparse(xml, events=('start', 'end'))
    interpro_id = None 
    shortname = None
    name = None
    ec_number = {}
    all_db = {}
    map_interpro = {}

    res_tag = None
    bool_tag = False

    for event, elem in context:
        
        if event == 'start' and elem.tag == 'interpro':
            interpro_id = elem.attrib.get('id')
            shortname = elem.attrib.get('short_name')
        
            if elem.tag not in all_db:
                all_db[elem.tag] = []
            all_db[elem.tag].append([interpro_id, shortname])
            
        elif event == 'start' and elem.tag == 'db_xref' and bool_tag:
            if res_tag == 'member_list' or bool_tag:
                db = elem.attrib.get('db')
                dbkey = elem.attrib.get('dbkey')
                name = elem.attrib.get('name')

                if db not in all_db:
                    all_db[db] = []
                all_db[db].append([dbkey, name])
                if interpro_id not in map_interpro:
                    map_interpro[interpro_id] = []
                if db not in [entry[0] for entry in all_db.get('member_list', [])]:
                    map_interpro[interpro_id].append(f"{dbkey} ")

        elif event == 'start' and elem.tag == 'db_xref' and elem.attrib.get('db') == 'EC':
            if interpro_id not in ec_number:
                ec_number[interpro_id] = []
            ec_number[interpro_id].append(elem.attrib.get('dbkey'))
        
        elif event == 'start' and elem.tag == 'member_list':
            res_tag = 'member_list'
            bool_tag = True

        elif event == 'end' and elem.tag == 'member_list':
            res_tag = None
            bool_tag = False

    writter_db_id_name(all_db, output_file)
    writter_ec(ec_number, output_file)

    
#==================================================================================================================
if __name__ == "__main__":
	main()