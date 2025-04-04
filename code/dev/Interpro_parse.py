import os
import csv
from tqdm import tqdm
import xml.etree.ElementTree as ET
from optparse import OptionParser

#==================================================================================================================

def writter_db_id_name(name_dict, output):
    '''Create a csv - database_id_name
        with the databe_id and the shortname
        --- arg ---
        name_dict is a dict like {key= db : value=[db_id, shortname]...}
        output is the folder direction to save this csv
        -----------'''
    for db, entries in name_dict.items():
        csv_filename = os.path.join(output, f"{db}_id_name.csv")
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['ID', 'ShortName'])
            for entry in entries:
                writer.writerow(entry)

#==================================================================================================================

def writter_ec(dict_ec, output):
    '''Create a csv - interpro_ec.csv 
        for each interpro_id, the ec_number
        --- arg ---
        dict_ec is a dict like {key= interpro_id : value=[ec_number, ...], ...}
        output is the folder direction to save this csv
        -----------'''
    csv_filename = os.path.join(output, "interpro_ec.csv")

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
      writer = csv.writer(csv_file)
      writer.writerow(['InterPro_ID', 'EC_Numbers'])  # Header row

      for interpro_id, ec_numbers in dict_ec.items():
        writer.writerow([interpro_id, ";".join(ec_numbers)])

#==================================================================================================================

def writter_map_interpro(map_dict, name_dict, output):
    '''Create a csv - interpro_map_id.csv
        For each intepro_id, all matching database_id
        --- arg ---
        map_dict is a dict like {key=interpro_id : value=[database, database_id, ...], ...}
        name_dict is a dict like {key= db : value=[db_id, shortname]...}
        output is the folder direction to save this csv
        -----------'''

    with open(output +"\interpro_map_id.csv", mode='w', newline='',encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([key for key,val in name_dict.items()])
        for interpro_id, entries in map_dict.items(): # entries is a list with db and dbkey associated
            for entry in entries:
                row = [interpro_id] + ["" for _ in name_dict]
                for entry in entries:
                    if entry[0] in name_dict:
                        row[list(name_dict.keys()).index(entry[0])] = entry[1]
            writer.writerow(row)

#==================================================================================================================
# 											main
#==================================================================================================================

def main():
    usage = "python Interpro_parse.py -i <input_file> -o <output_dir> \n"
    parser = OptionParser(usage)
    parser.add_option("-i", "--input_file", dest="input_file", help="path for the Interpro dataset")
    parser.add_option("-o", "--output_dir", dest="output_dir", help="path for the folder where the csv will be saved")

    (options, args) = parser.parse_args()
    input_file = options.input_file
    output_dir  = options.output_dir

    try:
        xml = open(input_file, "r", encoding='utf-8')
    except:
        print(' error with -i : correspond to the path of the dataset ')

    all_db = {}
    map_interpro = {}
    ec_number = {}
    interpro_id = None 
    shortname = None
    name = None
    res_tag = None
    bool_tag = False
    
    context = ET.iterparse(xml, events=('start', 'end'))

    for event, elem in tqdm(context, desc="Processing XML"):
        
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
                    map_interpro[interpro_id].append([db,dbkey])

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

    writter_db_id_name(all_db, output_dir)
    writter_map_interpro(map_interpro, all_db, output_dir)
    writter_ec(ec_number, output_dir)

#==================================================================================================================
if __name__ == "__main__":
	main()