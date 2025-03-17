# partiton d'interpro 
import os
import csv
import pandas as pd
import xml.etree.ElementTree as ET

from optparse import OptionParser

def main():
    usage = "python Interpro_partse.py -i <input_file> -o <output_file> \n"
    parser = OptionParser(usage)
    parser.add_option("-i", "--input_file", dest="input_file", help="path for the Interpro dataset")
    parser.add_option("-db", "--create_db", dest="create_db", help="create a csv that contains id + name (+ if possible shortname) by db in input_file")
    parser.add_option("-map", "--map_db", dest="",help="creat a csv for each Interpro Id shows the bases that compose it")
    parser.add_option("-ec", "ec", dest = "ec", help="creat a csv for each Interpro Id shows the EC_number that compose it")

    (option, args) = parser.parse_args()
    input_file = option.input_file
    output_file = option.output_file

    try:
        fichier = open(input_file, "r", encoding='utf-8')
    except:
        print(' error with -i : correspond to the path of the dataset ')


    title_1 = 'ID name'
    title_2 = 'ID shortname name'
    title_3 = 'INTERPRO_ID ANTIFAM CATHGENE3D CDD HAMAP NCBIFAM PANTHER PFAM PIRSF PRINTS PROFILE PROSITE reviewed SFLD SMART SSF UniProt unreviewed'
    title_4 = 'INTERPRO_ID EC'

    header_1 = ','.join(title_1.split())
    header_2 = ','.join(title_2.split())
    header_3 = ','.join(title_3.split())
    header_4 = ','.join(title_4.split())

    for ligne in fichier:

        if option.create_db is not None:
            if 'dbinfo' in ligne:
                ligne = ligne.split()[2][8:-1]
                part = open(ligne + "_id_name.csv", "w")
            if ligne == 'INTERPRO':
                part.write(header_1 + '\n')
            else:
                part.write(header_2 + '\n')
            part.close()

            part = open("interpro_id_name.csv", "a")

            if 'interpro id' in ligne:
                ID = ligne.split()[1][4:-1]
                shortname = ligne.split( )[3][12:-1]
                name = ligne.split()[3][12:-1]
                line = ','.join([ID, shortname, name])
                part.write(line + '\n')
            part.close()

            if 'db_xref protein_count' in ligne:
                db = ligne.split()[2][4:-1]
                id = ligne.split()[3][7:-1]
                name = ligne.split()[4][6:-3]
                part = open(db + "_id_name.csv", "a")
                line = ','.join([id, name])
                part.write(line + '\n')
                part.close()

        if option.map_db is not None:
            part = open('Interpro_map_db.csv', "w")
            part.write(header_3 + '\n')
            part.close()

            context = ET.iterparse(fichier, events=('start', 'end'))   
            interpro_id = None     
            mon_dic = {}    # Initialiser un dictionnaire pour enregistrer les données {interpro_id_1 : [(db_1, dkey_1), (db_2, dbkey_2), ...], ...} 

            for event, elem in context:
                if event == 'start' and elem.tag == 'interpro' and 'id' in elem.attrib: 
                    interpro_id = elem.attrib['id']

                    mon_dic[interpro_id] = [] 

                elif elem.tag == 'member_list' and interpro_id: 
                    for db_xref in elem.findall('db_xref'):
                        db = db_xref.attrib.get('db')
                        dbkey = db_xref.attrib.get('dbkey') 
                        mon_dic[interpro_id].append((db, dbkey)) 
                            
                    interpro_id = None 

                elem.clear() 

            data = []    

            for interpro_id, db_list in mon_dic.items():
                row = {'INTERPRO_ID': interpro_id}
                for db, dbkey in db_list:
                    if db in row:
                        row[db] = row[db] + '; ' + dbkey
                    else:
                        row[db] = dbkey
                data.append(row)

            df = pd.DataFrame(data)    # Créer un DataFrame à partir des données accumulées

            # Enregistrer le DataFrame dans un fichier CSV
            df.to_csv("Interpro_map_db.csv", index=False)

        
        if option.ec is not None:
            part = open('Interprot_EC.csv', "w")
            part.write(header_4 + '\n')
            part.close()

            context = ET.iterparse(fichier, events=('start', 'end'))  
            interpro_id = None    
            mon_dic = {}    
    
            for event, elem in context:
                if event == 'start' and elem.tag == 'interpro' and 'id' in elem.attrib: 
                    mon_dic[interpro_id] = [] 

                elif elem.tag == 'external_doc_list' and interpro_id: 
            
                    for db_xref in elem.findall('db_xref'):
                        db = db_xref.attrib.get('db') 
                        if db == 'EC':
                            mon_dic[interpro_id].append(db_xref.attrib.get('dbkey'))
                    interpro_id = None
                elem.clear()

            data = []   

            for interpro_id, db_list in mon_dic.items():
                row = {'INTERPRO_ID': interpro_id}
                row['EC'] = ''
                for dbkey in db_list:
                    if row['EC']:
                        row['EC'] += '; ' + dbkey
                    else:
                        row['EC'] = dbkey
                data.append(row)

            df = pd.DataFrame(data) 

            df.to_csv('Interprot_EC.csv', index=False)

#==================================================================================================================
if __name__ == "__main__":
	main()